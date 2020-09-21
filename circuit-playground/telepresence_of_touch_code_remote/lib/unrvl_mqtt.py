from mqtt_serial import SerialMQTT

class UnrvlMQTT:
    # json packets, dispatch interface

    def __init__( self, server ):
        self.mqtt = SerialMQTT(server)
        self.subscriptions = {} # { "topic" : { "key" : handler, ...} }
        self.last_message = {}
        self.mqtt.on_connect = self.do_subscriptions
        self.mqtt.on_message = self.do_message

    def connect(self):
        # Can subscribe before connecting
        self.mqtt.connect()

    def subscribe( self, topic, key_pattern_handlers ):
        # on a message, with the key, whose value matches, call:
        #       your_handler( topic, key, value )
        # e.g.
        # unrvl.subscribe( 
        #   "unrvl/awgrover", 
        #   {
        #   re.compile('touch') : do_touch_message,
        #   'push1' : do_push1_message
        #   }
        # )

        if not ( topic in self.subscriptions ):
            self.subscriptions[topic] = {}
        pattern_handlers = self.subscriptions[topic]

        for key,handler in key_pattern_handlers.items(): 
            # we blithely overwrite early key:handler entries
            pattern_handlers[key] = handler

    def publish( self, topic, message):
        if self.mqtt.is_connected():
            self.mqtt.publish(topic, message)

    def run( self ):
        # call often to react to mqtt stuff
        return self.mqtt.run()

    # private
    def do_subscriptions( self ):
        # called on CONNECTED (which is also re-connect)
        # what topics do we want to listen to?
        for topic in list(self.subscriptions):
            self.mqtt.subscribe(topic)

    def do_message(self, client, topic, message):
        # client is mqtt (the SerialMQTT) instance

        # we only know how to handle json
        if not isinstance(message, dict):
            print("debugmqtt: message wasn't json:", message)
            return
        
        key_patterns = self.subscriptions.get(topic)
        if key_patterns:
            # test each key
            for key,value in message.items():
                # against each key pattern
                hit = False
                for a_key_pattern,handler in key_patterns.items():
                    if a_key_pattern == key:
                            hit = True
                            handler(topic, key, value, message)
                if not hit:
                    print("debugmqtt message no key-match/handler:",topic,message)
                    
        else:
            print("debugmqtt message w/o subscriber:",topic,message)
