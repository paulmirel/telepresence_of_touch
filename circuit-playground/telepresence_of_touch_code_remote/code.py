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
import re
import gc

gc.collect()
from adafruit_circuitplayground import cp

gc.collect()
from every import Every
gc.collect()
from unrvl_mqtt import UnrvlMQTT
gc.collect()

# MQTT server & topics
unrvl_mqtt = UnrvlMQTT("mqtt://localhost:1883")
# what channels do we want to listen to?
unrvl_mqtt.subscribe(
    "unrvl2020/awgrover",
    {
    # what do we want to do with each key:value
    'touch' : do_touch_message
    }
)
MQTTPublishTo = 'awgrover/touch'

LastTouchPart = {}

def update_touch(mqtt_message):
    # fill in the message to correspond to our touch
    global LastTouchPart

    # just our part
    # might be a bunch of entries like
    # { touch" : { 1 : [0,255,0], 2: [255,0,0], 3:[0,0,0] }
    touch_part = {}

    # (fixme: what possible ways are there to "factor" this repetition?)
    # touch near pixel 1, between A4 and A5
    # use -or- for greater sensitivity to touch, use -and- for more localized sensitivity to touch
    if cp.touch_A4 or cp.touch_A5: 
        cp.pixels[ 1 ] = LightColor
        touch_part[1] = LightColor # we'll send our color
    else:
        cp.pixels[ 1 ] = OFF
        touch_part[1] = OFF

    # touch near pixel 3, between A6 and A7
    if cp.touch_A6 or cp.touch_A7:
        cp.pixels[ 3 ] = LightColor
        touch_part[2] = LightColor
    else:
        cp.pixels[ 3 ] = OFF
        touch_part[2] = OFF

    # touch near pixel 6, between A0 and A1
    if cp.touch_A1: # cp.touch_A0 is not available in the cp library
        cp.pixels[ 6 ] = LightColor
        touch_part[3] = LightColor
    else:
        cp.pixels[ 6 ] = OFF
        touch_part[3] = OFF

    # touch near pixel 8, between A2 and A3
    if cp.touch_A2 or cp.touch_A3:
        cp.pixels[ 8 ] = LightColor
        touch_part[4] = LightColor
    else:
        cp.pixels[ 8 ] = OFF
        touch_part[4] = OFF

    # we don't want to send anything if nothing has changed
    if touch_part != LastTouchPart:
        mqtt_message['touch'] = touch_part
        LastTouchPart = touch_part # remember for next time
    gc.collect()

def do_touch_message( topic, key, value, full_message ):
    # value looks like:
    #   { 1: (0,0,0), 4: (255,0,0), ... }
    # i.e. which "touch" and the desired color
    #print("debugmqtt: handled",topic,"|",key,":",value," in ",full_message)
    remote_to_local = [ 0, 0, 2, 5, 7 ] # map of touch # to local led
    for which, color in value.items():
        print('remote', which, color)
        if color == (0,0,0):
            cp.pixels[ remote_to_local[which] ] = OFF
        else:
            cp.pixels[ remote_to_local[which] ] = RemoteColor # ignore their color

### Startup

## Heartbeat
# We're using "Every":
# will be true "every n seconds", non-blocking time.sleep()
heartbeat = Every(3)
cp.red_led = False # because heartbeat turns it on immediately

## Touch
cp.pixels.brightness = 0.4 # the LEDs are too bright
every_update_touch = Every(0.01) # how often to check touch sensors
LightColor = ( 255, 0, 0 )
RemoteColor = ( 0, 60, 60 )
OFF = ( 0, 0, 0 )

# MQTT (remote communication)
unrvl_mqtt.connect()

# setup event handling
every_update_remote = Every(3) # how often to send complete state

### Loop
print("Free memory before loop",gc.mem_free())

while True:
    # blink the plain LED (next to usb) slowly to indicate that we are running
    if heartbeat():
        #print("heartbeat free mermory", gc.mem_free(), time.monotonic())
        cp.red_led = not cp.red_led # clever "toggle", aka "blink"

    # Add key:value that the remote system should know about,
    # e.g. mqtt_message['touch1'] = LightColor
    # The remote system has to know what to do with each "key"
    mqtt_message = {} # will be sent if anything changed

    # we can react locally very fast: 0.01 sec
    if every_update_touch():
        # checks each touch pad, lights the led, adds to mqtt_message
        update_touch( mqtt_message )

    # if anything to send, do it
    if mqtt_message:
        unrvl_mqtt.publish("awgrover/touch", mqtt_message)

    # handle mqtt events
    other_message = unrvl_mqtt.run()

    # just echo any other text that came over the serial
    if other_message:
        print("Not understood:", other_message)
