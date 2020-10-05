# telepresence_of_touch
# Paul Mirel and Alan Grover for MICA Maryland Institute College of Art
# 20200909
#
# "cp" api docs: https://circuitpython.readthedocs.io/projects/circuitplayground/en/latest/api.html
# circuitpython api docs: https://circuitpython.readthedocs.io/en/latest/shared-bindings/index.html
#
# If you see 
#       MemoryError: memory allocation failed
# then just re-send the code.py, or reset the CPE

import time
import random
import gc

gc.collect()
from adafruit_circuitplayground import cp
gc.collect()
from every import Every
gc.collect()
from mqtt_serial import SerialMQTT
gc.collect()

###
## Constants!

# your initials
Me='ANON' # EDIT ME with your initials or something short

MyColor = None # random, or edit this with your color (cf. "My color is (181, 74, 0)")
LocalColor = None # will be MyColor unless you change it in setup()
RemoteColor = None # will be MyColor unless you change it in setup()

MQTTServer = "mqtt://f557f2ed:e8f599a52aae3773@broker.shiftr.io"

# Send touch messages to topic:
MQTTPublishTo = 'unrvl2020/touch-everyone' # # "unrvl2020/shake-group1"
# Listen for touch messages in topic(s):
MQTTSubscribe = [ 
    MQTTPublishTo,
    # more than 1...
    ]

## HeartBeat
# We're using "Every":
# will be true "every n seconds", non-blocking time.sleep()
# to "flash" the built-in LED
HeartBeat = Every(3)

# Touch constants
EveryUpdateTouch = Every(0.01) # how often to check touch sensors
OFF = ( 0, 0, 0 ) # convenient off value for LEDs

Mqtt=None # will hold the SerialMQTT object
LastTouchPart = {} # so we can tell if we need to send more touch data
FirstTime = True # for initial message

def setup():
    global MyColor, RemoteColor, LocalColor, Mqtt

    # (seed the random generator)
    random.seed(int(cp.light + cp.temperature * 100 + time.monotonic()*1000));

    # pick our color if it is still None
    if not MyColor:
        MyColor = random_color() # Random if you didn't set it
    print("My color is", MyColor);

    LocalColor = RemoteColor = MyColor

    # because HeartBeat turns it on immediately
    cp.red_led = False 

    ## Touch setup
    cp.pixels.brightness = 0.4 # the LEDs are too bright
    cp.pixels[0] = RemoteColor; # Show our color

    # MQTT (remote communication)
    # MQTT server & topics
    Mqtt = SerialMQTT(MQTTServer)
    for topic in MQTTSubscribe:
        Mqtt.subscribe(topic)

def loop():
    global FirstTime

    # blink the plain LED (next to usb) slowly to indicate that we are running
    if HeartBeat():
        #print("HeartBeat free mermory", gc.mem_free(), time.monotonic())
        cp.red_led = not cp.red_led # clever "toggle", aka "blink"

    # Should we show some indication on the CPX that we are connected?

    # Add key:value that the remote system should know about,
    # e.g. mqtt_message['touch1'] = LocalColor
    # The remote system has to know what to do with each "key"
    mqtt_message = {} # filled in and will be sent if anything changed

    # We could check for other things, like shake, buttons, etc
    # and add to mqtt_message
    # (or make a different message for a differnt topic)

    # we can react locally very fast: 0.01 sec
    if EveryUpdateTouch():
        # checks each touch pad, lights the led, adds to mqtt_message
        update_touch( mqtt_message )

    # if anything to send, do it
    if mqtt_message:
        mqtt_message['from'] = Me # add our initials
        Mqtt.publish(MQTTPublishTo, mqtt_message)

    # handle mqtt communication
    other_message, topic, mqtt_incoming_message = Mqtt.receive_message()
    if mqtt_incoming_message:
        handle_mqtt_message(topic, mqtt_incoming_message)
    elif other_message:
        print("Not understood:", other_message)

    # We can send a message(s) once, as soon as we connect
    if Mqtt.is_connected() and FirstTime:
        Mqtt.publish(MQTTPublishTo, { "from" : Me, "message" : "hello"} )
        FirstTime = False # we did it, not first-time anymore

def update_touch(mqtt_message):
    # fill in the message to correspond to our touch
    global LastTouchPart

    # just our part
    # might be a bunch of entries like
    # { touch" : { 1 : [0,255,0], 2: [255,0,0], 3:[0,0,0] }
    touch_part = {}

    # We use the odd pixels for signalling local-touch
    # (we'll use the even for remote touch)

    # (fixme: what possible ways are there to "factor" this repetition?)
    # touch near pixel 1, between A4 and A5
    # use -or- for greater sensitivity to touch, use -and- for more localized sensitivity to touch
    if cp.touch_A4 or cp.touch_A5: 
        cp.pixels[ 1 ] = LocalColor
        touch_part[1] = LocalColor # we'll send our color
    else:
        cp.pixels[ 1 ] = OFF
        touch_part[1] = OFF

    # touch near pixel 3, between A6 and A7
    if cp.touch_A6 or cp.touch_TX: # aka A7 (bluefruit calls it TX)
        cp.pixels[ 3 ] = LocalColor
        touch_part[2] = LocalColor
    else:
        cp.pixels[ 3 ] = OFF
        touch_part[2] = OFF

    # touch near pixel 6, between A0 and A1
    if cp.touch_A1: # cp.touch_A0 is not available in the cp library
        cp.pixels[ 6 ] = LocalColor
        touch_part[3] = LocalColor
    else:
        cp.pixels[ 6 ] = OFF
        touch_part[3] = OFF

    # touch near pixel 8, between A2 and A3
    if cp.touch_A2 or cp.touch_A3:
        cp.pixels[ 8 ] = LocalColor
        touch_part[4] = LocalColor
    else:
        cp.pixels[ 8 ] = OFF
        touch_part[4] = OFF

    # add our initials

    # we don't want to send anything if nothing has changed
    if touch_part != LastTouchPart:
        mqtt_message['touch'] = touch_part
        LastTouchPart = touch_part # remember for next time
    gc.collect()

def random_color():
    # pick a random color, but near the rim of the color wheel (high saturation/value)
    rg_or_b = random.uniform(1,3.99);
    if rg_or_b >= 3:
        blue = int(255 * (rg_or_b - 3))
        green = 255 - blue
        red = 0
    elif rg_or_b >= 2:
        green = int(255 * (rg_or_b - 2))
        blue = 255 - green
        red = 0
    else:
        red = int(255 * (rg_or_b - 1))
        green = 255 - red
        blue = 0
    return (red,green,blue)

def handle_mqtt_message(topic, mqtt_message):
    # See if there is an incomming message
    # react to it

    # ignore our own message!
    if 'from' in mqtt_message and mqtt_message['from'] == Me:
        return

    print("MSG ", mqtt_message)

    # We could make decisions about what to do based on the topic...

    # A "touch" message looks like:
    # { touch" : { 1 : [0,255,0], 2: [255,0,0], 3:[0,0,0] }
    # i.e. which "touch" and the requested color
    if "touch" in mqtt_message:
        value = mqtt_message["touch"]

        # make sure it's a dict!
        if ( not isinstance(value, dict) ):
            print("debugmqtt: 'touch' wasn't an dict:",value)
            return

        # we could make decisions based on the value['from']
    
        # But, just show the touch

        print("Touch! ")
        remote_to_local = [ 0, 2, 4, 6, 8 ] # map of touch number to local led number (unused)

        for which, color in value.items():
            print('remote', which, 'to', remote_to_local[which],color)
            if color == (0,0,0):
                cp.pixels[ remote_to_local[which] ] = OFF
            elif isinstance(color,tuple) or isinstance(color,list):
                cp.pixels[ remote_to_local[which] ] = RemoteColor # ignore their color
            else:
                print("debugmqtt: expected the 'color' to be a tuple/list, saw", color.__class__.__name__,color)

### 
setup()

print("Free memory before loop",gc.mem_free())

while True:
    loop()

