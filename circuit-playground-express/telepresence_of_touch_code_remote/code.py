# telepresence_of_touch
# Paul Mirel and Alan Grover for MICA Maryland Institute College of Art
# 20200909
#
# "cp" api docs: https://circuitpython.readthedocs.io/projects/circuitplayground/en/latest/api.html
# circuitpython api docs: https://circuitpython.readthedocs.io/en/latest/shared-bindings/index.html

from adafruit_circuitplayground import cp
import time

import sys
sys.path.append('%PROJECT/lib')
from every import Every
from mqtt_serial import SerialMQTT

cp.pixels.brightness = 0.6

light_color = ( 255, 0, 0 )
OFF = ( 0, 0, 0 )
mqtt = SerialMQTT("mqtt://localhost:1883")

every_hundreth = Every(0.01)
heartbeat = Every(3)
every_update_remote = Every(0.3)

# startup
cp.red_led = False # because heartbeat turns it on immediately
mqtt.connect()

last_message = {}
message = {}

while True:
    if heartbeat():
        print("heartbeat ", time.monotonic())
        cp.red_led = not cp.red_led

    # we can react locally very fast: 0.01 sec
    if every_hundreth():

        # touch near pixel 1, between A4 and A5
        # use -or- for greater sensitivity to touch, use -and- for more localized sensitivity to touch
        if cp.touch_A4 or cp.touch_A5: 
            cp.pixels[ 1 ] = light_color
            message['touch1'] = light_color # we'll send our color
        else:
            cp.pixels[ 1 ] = OFF
            message['touch1'] = OFF

        # touch near pixel 3, between A6 and A7
        if cp.touch_A6 or cp.touch_A7:
            cp.pixels[ 3 ] = light_color
            message['touch2'] = light_color
        else:
            cp.pixels[ 3 ] = OFF
            message['touch2'] = OFF

        # touch near pixel 6, between A0 and A1
        if cp.touch_A1: # cp.touch_A0 is not available in the cp library
            cp.pixels[ 6 ] = light_color
            message['touch3'] = light_color
        else:
            cp.pixels[ 6 ] = OFF
            message['touch3'] = OFF

        # touch near pixel 8, between A2 and A3
        if cp.touch_A2 or cp.touch_A3: # use -or- for greater sensitivity to touch, use -and- for more localized sensitivity to touch
            cp.pixels[ 8 ] = light_color
            message['touch4'] = light_color
        else:
            cp.pixels[ 8 ] = OFF
            message['touch4'] = OFF

    # We don't need to update the remote as often, maybe 3/sec
    if every_update_remote():
        # has anything changed?
        # if the message is different than the last message we sent
        changes = { k : message[k] for k, _ in set(message.items()) - set(last_message.items()) }
        if changes:
            print( " ", changes )
            last_message = message.copy() # remember the last change


    other_message = mqtt.run()
    if other_message:
        print(other_message)
