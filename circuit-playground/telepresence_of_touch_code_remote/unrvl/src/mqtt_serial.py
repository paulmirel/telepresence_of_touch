# SerialMQTT
# Meant to talk to a serial-to-mqtt gateway by passing messages on serial.
# 
# usage:
# 
# from unrvl.mqtt_serial import SerialMQTT 
#
# mqtt = SerialMQTT("mqtt://some.host:port")
# mqtt.subscribe(topic) # repeat for every topic of interest
# 
# while(True):
#    mqtt.run()
#
#    if you-have-a-message-to-send:
#      mqtt.publish(topic, mqtt_message)
#
#    other_message, topic, mqtt_incoming_message = mqtt.receive_message()
#    if mqtt_incoming_message:
#        react-somehow-to( topic, mqtt_incoming_message)
#    else
#        react-somehow-to( other_message ) # some text from the serial port

import supervisor
import sys
import time

# _* is local inlined, const() saves ram
_RetryConnect = const(3) # seconds
_State_DISCONNECTED = const(0)
_State_WAIT_FOR_CONNECT = const(1)
_State_CONNECTED = const(2)

class SerialMQTT:

    # :param str broker: MQTT Broker URL or IP Address.
    # :param State state: The protocol state

    def __init__( self, broker ): # just an url
        self.broker = broker # we are pretty stupid
        self.recvbuffer = "" # accumulating message
        self.state = _State_DISCONNECTED
        self.connect_timeout = 0
        self.last_topic = None
        self.subscriptions = []
        print("debugmqtt: will retry connect every",_RetryConnect,"seconds")
        self.connect()

    def connect(self): # assume clean_session, non-blocking
        print("mqtt: connect " + self.broker)
        self.state = _State_WAIT_FOR_CONNECT
        self.connect_timeout = time.monotonic() + _RetryConnect # retry every ...

    def is_connected(self):
        return self.state == _State_CONNECTED

    def subscribe(self, topic): # qos=0
        self.subscriptions.append(topic)
        if self.is_connected():
            print("mqtt: subscribe " + topic)

    def publish(self, topic, message): # qos=0
        if self.state  == _State_CONNECTED:
            print("mqtt: publish " + topic, end = " ")
            if isinstance(message, dict):
                print( message ) # circuitplayground has no ujson, so python-"dump"
            else:
                print( message )
        else:
            #print("debugmqtt not connected tried to publish",topic,message)
            pass

    def receive_message(self):
        # call this often to detect incoming MQTT stuff. 
        # returns:
        #   If incoming serial is not mqtt:
        #       theserialstring, None, None
        #   If nothing interesting:
        #       None, None, None
        #   If incoming message:
        #       None, topic, message

        # fixme: pass in a string that you read, we'll say True if we consume it

        received = None # did we see end-of-line?
        while supervisor.runtime.serial_bytes_available:
            # Consume everything we can (until a full message!)
            # it appears that a sys.stdin takes essentially 0 time to read
            # but, perhaps the baud rate of the host computer has an effect
            # ( I saw about .01 sec per char when I set 115200)
            # (it's serial emulation over usb, oh my!)
            next_char = sys.stdin.read(1) # hmm, utf8?

            # we'll tolerate LF or CR
            if next_char == "\r" or next_char == "\n":
                if self.recvbuffer == "":
                    # ignore it if nothing read so far,
                    # i.e. do the right thing for a CRLF sequence
                    continue
                else:
                    #print("GOT '" + self.recvbuffer + "'")
                    received = True
                    break # there may be more in the serial buffer, but handle this first
            else:
                self.recvbuffer = self.recvbuffer + next_char

        # did we get a message?
        if not received:
            # initial connect depends on the processing side listening, so retry
            if self.state == _State_WAIT_FOR_CONNECT and self.connect_timeout <= time.monotonic():
                # if supervisor.runtime.serial_connected: # doesn't seem to work
                self.connect()

            return [None,None, None]

        # when we get a mqtt message:

        if self.recvbuffer.startswith("mqtt: connected"):
            self.recvbuffer = ""

            # might be a reconnect, so re-subscribe
            for topic in self.subscriptions:
                print("mqtt: subscribe " + topic)

            if self.state >= _State_WAIT_FOR_CONNECT: # we may re-connect
                self.state = _State_CONNECTED
                print("debugmqtt connected")
            else:
                #print("debugmqtt connected, but already @", self.state)
                pass

            return [None, None, None]

        elif self.recvbuffer.startswith("mqtt: message "):
            json = self.recvbuffer[ len("mqtt: message "): ]
            # { "topic":$s, "payload" : string|dict }

            # FIXME: find a minimal json decoder
            # I can't figure out why ujson isn't in circuitpython
            # I looked at https://github.com/simplejson/simplejson,
            #   but it uses several things that aren't in circuitpython
            # might be adaptable (strip out the streaming part?) 
            #   https://github.com/danielyule/naya/blob/master/naya/json.py

            # DANGER: eval is unsafe. 
            # A message sent to you can execute ANY code
            # the attack surface is the CPE (boring), 
            #   the usb-port, which is the usb-hardward/driver level (so vulnerabilities), 
            #   and our "mqtt-serial" protocol, so they could send evil to other people (any mqtt broker!)

            mqtt_packet = None

            try:
                #print("eval'ing",json)
                mqtt_packet = eval(json)
                # bug... hack
                if "payload" in mqtt_packet and isinstance(mqtt_packet["payload"], str):
                    mqtt_packet["payload"] = eval( mqtt_packet["payload"] )
                #print("eval'd",mqtt_packet.__class__.__name__,mqtt_packet)
            except SyntaxError as e:
                print("debugmqtt: bad message, no python-struct:",json)
                print( e )
                self.recvbuffer = ""
                return [None, None, None]

            self.recvbuffer = ""
            if isinstance(mqtt_packet, dict) and 'topic' in mqtt_packet and 'payload' in mqtt_packet:
                return [None, mqtt_packet['topic'], mqtt_packet['payload'] ]
            else:
                print("debugmqtt: was a dict, but expected 'topic' and 'payload':", mqtt_packet)
                return [None, None, None]
            
        # Not an mqtt: message
        else:
            #print("debugmqtt not mqtt:")
            x = self.recvbuffer
            self.recvbuffer = ""
            return [x,None, None]
