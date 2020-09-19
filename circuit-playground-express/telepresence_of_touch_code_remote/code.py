# telepresence_of_touch
# Paul Mirel and Alan Grover for MICA Maryland Institute College of Art
# 20200909
#
# "cp" api docs: https://circuitpython.readthedocs.io/projects/circuitplayground/en/latest/api.html
# circuitpython api docs: https://circuitpython.readthedocs.io/en/latest/shared-bindings/index.html

from adafruit_circuitplayground import cp
import time

from every import Every
from mqtt_serial import SerialMQTT

def do_subscriptions():
    # what topics do we want to listen to?
    for a_channel in MQTTSubscriptions:
        mqtt.subscribe(a_channel)

def do_message(client, topic, message):
    # client is the SerialMQTT instance
    # message is:
    print("mqtt seen:",topic,message)
    
def update_touch(message):
    # fill in the message to correspond to our touch

    # (fixme: what possible ways are there to "factor" this repetition?)
    # touch near pixel 1, between A4 and A5
    # use -or- for greater sensitivity to touch, use -and- for more localized sensitivity to touch
    if cp.touch_A4 or cp.touch_A5: 
        cp.pixels[ 1 ] = light_color
        mqtt_message['touch1'] = light_color # we'll send our color
    else:
        cp.pixels[ 1 ] = OFF
        mqtt_message['touch1'] = OFF

    # touch near pixel 3, between A6 and A7
    if cp.touch_A6 or cp.touch_A7:
        cp.pixels[ 3 ] = light_color
        mqtt_message['touch2'] = light_color
    else:
        cp.pixels[ 3 ] = OFF
        mqtt_message['touch2'] = OFF

    # touch near pixel 6, between A0 and A1
    if cp.touch_A1: # cp.touch_A0 is not available in the cp library
        cp.pixels[ 6 ] = light_color
        mqtt_message['touch3'] = light_color
    else:
        cp.pixels[ 6 ] = OFF
        mqtt_message['touch3'] = OFF

    # touch near pixel 8, between A2 and A3
    if cp.touch_A2 or cp.touch_A3:
        cp.pixels[ 8 ] = light_color
        mqtt_message['touch4'] = light_color
    else:
        cp.pixels[ 8 ] = OFF
        mqtt_message['touch4'] = OFF
# Startup

## Heartbeat
# We're using "Every":
# will be true "every n seconds", non-blocking time.sleep()
heartbeat = Every(3)
cp.red_led = False # because heartbeat turns it on immediately

## Touch
cp.pixels.brightness = 0.4 # the LEDs are too bright
every_update_touch = Every(0.01) # how often to check touch sensors
light_color = ( 255, 0, 0 )
OFF = ( 0, 0, 0 )

# MQTT (remote communication)
# FIXME: factor to a unrvl_mqtt class
mqtt = SerialMQTT("mqtt://localhost:1883")
MQTTSubscriptions = [ 'awgrover/bob' ]
MQTTPublishTo = 'awgrover/touch'

# setup event handling
every_update_remote = Every(3) # how often to send complete state
mqtt.on_connect = do_subscriptions
mqtt.on_message = do_message
# this will trigger do_subscriptions, so, setup before this:
mqtt.connect() # after .on_xxx's
MQTTLastMessage = {}

while True:
    # blink the plain LED (next to usb) slowly to indicate that we are running
    if heartbeat():
        print("heartbeat ", time.monotonic())
        cp.red_led = not cp.red_led # clever "toggle", aka "blink"

    # Add key:value that the remote system should know about,
    # e.g. mqtt_message['touch1'] = light_color
    # The remote system has to know what to do with each "key"
    mqtt_message = {} # will be sent if anything changed

    # we can react locally very fast: 0.01 sec
    if every_update_touch():
        # checks each touch pad, lights the led, adds to mqtt_message
        update_touch( mqtt_message )

    if mqtt.is_connected():
        # Possibly send messages if we are connected

        # We can tell if anything has changed, so update on that
        # has anything changed?
        # if the message is different than the last message we sent
        changes = { k : mqtt_message[k] for k, _ in set(mqtt_message.items()) - set(MQTTLastMessage.items()) }
        if changes:
            print( " ", changes )
            mqtt.publish( MQTTPublishTo, changes)
            MQTTLastMessage = mqtt_message.copy() # remember the last change

        # in case a message got dropped, repeat the last full message 
        # (not just changes)
        # ensures our "changes" messages are synchronized
        if every_update_remote():
            mqtt.publish("awgrover/touch", MQTTLastMessage)

    # handle mqtt events
    other_message = mqtt.run()

    # just echo any other text that came over the serial
    if other_message:
        print("Not understood:", other_message)
