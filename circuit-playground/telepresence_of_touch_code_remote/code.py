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

LastTouchPart = {}

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
    if cp.touch_A6 or cp.touch_A7:
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

def do_subscriptions():
    # when we finally connect, need to subscribe
    for topic in MQTTSubscribe:
        mqtt.subscribe(topic)

def handle_mqtt_message():
    # See if there is an incomming message
    # react to it

    topic, mqtt_message = mqtt.receive_message()
    if not mqtt_message:
        return # nothing to do this time

    # FIXME: ignore our own message! initials

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

### Startup

MQTTServer = "mqtt://localhost:1883"

MQTTPublishTo = 'unrvl2020/touch-everyone'
MQTTSubscribe = [ 'unrvl2020/touch-everyone' ]

# your initials
Me='awg'

# pick our color
# (seed the random generator)
random.seed(int(cp.light + cp.temperature * 100 + time.monotonic()*1000));
RemoteColor = random_color() # Random. edit me! what's your color?
LocalColor = RemoteColor
print("My color is", RemoteColor);

## Heartbeat
# We're using "Every":
# will be true "every n seconds", non-blocking time.sleep()
heartbeat = Every(3)
cp.red_led = False # because heartbeat turns it on immediately

## Touch
cp.pixels.brightness = 0.4 # the LEDs are too bright
every_update_touch = Every(0.01) # how often to check touch sensors
OFF = ( 0, 0, 0 )
cp.pixels[0] = RemoteColor;

# MQTT (remote communication)
# MQTT server & topics
mqtt = SerialMQTT(MQTTServer)
mqtt.connect()

# what channels do we want to listen to?
mqtt.subscribe( "unrvl2020/touch-everyone" )
# mqtt.subscribe( "unrvl2020/shake-group1" )

# setup event handling
every_update_remote = Every(3) # how often to send complete state FIXME: drop?

### Loop
print("Free memory before loop",gc.mem_free())

while True:
    # blink the plain LED (next to usb) slowly to indicate that we are running
    if heartbeat():
        #print("heartbeat free mermory", gc.mem_free(), time.monotonic())
        cp.red_led = not cp.red_led # clever "toggle", aka "blink"


    # Add key:value that the remote system should know about,
    # e.g. mqtt_message['touch1'] = LocalColor
    # The remote system has to know what to do with each "key"
    mqtt_message = {} # filled in and will be sent if anything changed

    # we can react locally very fast: 0.01 sec
    if every_update_touch():
        # checks each touch pad, lights the led, adds to mqtt_message
        update_touch( mqtt_message )

    # if anything to send, do it
    if mqtt_message:
        mqtt.publish(MQTTPublishTo, mqtt_message)

    # handle mqtt communication
    other_message, should_reconnect = mqtt.run()
    # we may have to connect (or re-connect)
    if should_reconnect:
        print("## reconnect?", should_reconnect)
        do_subscriptions()

    # just echo any other text that came over the serial
    if other_message:
        print("Not understood:", other_message)

    handle_mqtt_message()
