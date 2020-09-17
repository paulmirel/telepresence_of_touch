"""
SerialMQTT
Meant to talk to a serial-to-mqtt gateway by passing messages on serial.

usage:

from mqtt_serial import SerialMQTT
mqtt = SerialMQTT("mqtt://some.host:port")
mqtt.on_connect = connected # def connected(client, userdata, flags, rc):, do subscribes
mqtt.on_message = message # def message(client, topic, message):
mqtt.connect()

while(True):
    mqtt.run()
"""

import supervisor
import sys

class SerialMQTT:

    """
    :param str broker: MQTT Broker URL or IP Address.
    :param State state: The protocol state
    """
    class State: # enum so we can do >= (no enums in circuitpython, sad)
        DISCONNECTED = 0
        WAIT_FOR_CONNECT = 1
        CONNECTED = 2

    def __init__( self, broker ): # just an url
        self.broker = broker # we are pretty stupid
        self.on_connect = None
        self.on_message = None
        self.recvbuffer = ""
        self.state = self.State.DISCONNECTED

    def connect(self): # assume clean_session, non-blocking
        print("mqtt: connect " + self.broker)
        self.state = self.State.WAIT_FOR_CONNECT

    def is_connected(self):
        return self.state == self.State.CONNECTED

    def subscribe(self, topic): # qos=0
        print("mqtt: subscribe " + topic)

    def publish(self, topic, message): # qos=0
        if self.state  == self.State.CONNECTED:
            print("mqtt: publish " + topic, end = " ")
            if isinstance(message, dict):
                print( message ) # FIXME: ujson.dumps(message) )
            else:
                print( message )
        else:
            print("debugmqtt not connected tried to publish",topic,message)
            


    def run(self):
        """ call this often to detect incoming messages. 
            we return None if we consumed, else the unconsummed line
        """
        # fixme: pass in a string that you read, we'll say True if we consume it

        received = None # did we see end-of-line?
        while supervisor.runtime.serial_bytes_available:
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
                    print("GOT " + self.recvbuffer)
                    received = True
            else:
                self.recvbuffer = self.recvbuffer + next_char

        if not received:
            return None

        # when we get a mqtt message:
        if self.recvbuffer.startswith("mqtt: connected"):
            if self.state >= self.State.WAIT_FOR_CONNECT:
                if self.on_connect:
                    self.on_connect()
                else:
                    print("debugmqtt saw connected, but no on_connect listener")
                self.state = self.State.CONNECTED
            else:
                print("debugmqtt connected, but alread", self.state)
                

            self.recvbuffer = ""
            return None

        if self.recvbuffer.startswith("mqtt: message "):
            json = self.recvbuffer[ len("mqtt: message "): ]
            # { "topic":$s, "payload" : string|dict }
            mqtt_packet = eval(json) # FIXME: not safe. ujson.loads(json)
            if self.on_message:
                self.on_message( self, mqtt_packet['topic'], mqtt_packet['payload'] )
            else:
                print("debugmqtt no on_message:", json)
            
        # Not an mqtt: message
        else:
            print("debugmqtt not mqtt:")
            x = self.recvbuffer
            self.recvbuffer = ""
            return x

        # mqtt_client.on_connect = connected # def connected(client, userdata, flags, rc):
        # mqtt_client.on_message = message # def message(client, topic, message):
