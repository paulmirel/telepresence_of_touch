# telepresence_of_touch
# Paul Mirel and Alan Grover for MICA Maryland Institute College of Art
# 20200909

from adafruit_circuitplayground import cp
import time

import sys
sys.path.append('%PROJECT/lib')
from every import Every

cp.pixels.brightness = 0.6

light_color = ( 255, 0, 0 )
OFF = ( 0, 0, 0 )

every_tenth = Every(0.1)
heartbeat = Every(3)

while True:
    if heartbeat():
        print("heartbeat ", time.monotonic())

    if every_tenth():
        output = ""
        # touch near pixel 1, between A4 and A5
        if cp.touch_A4 or cp.touch_A5: # use -or- for greater sensitivity to touch, use -and- for more localized sensitivity to touch
            cp.pixels[ 1 ] = light_color
            output = output + " 1"
        else:
            cp.pixels[ 1 ] = OFF

        # touch near pixel 3, between A6 and A7
        if cp.touch_A6 or cp.touch_A7: # use -or- for greater sensitivity to touch, use -and- for more localized sensitivity to touch
            cp.pixels[ 3 ] = light_color
            output = output + " 3"
        else:
            cp.pixels[ 3 ] = OFF

        # touch near pixel 6, between A0 and A1
        if cp.touch_A1: # cp.touch_A0 is not available in the cp library
            cp.pixels[ 6 ] = light_color
            output = output + " 6"
        else:
            cp.pixels[ 6 ] = OFF

        # touch near pixel 8, between A2 and A3
        if cp.touch_A2 or cp.touch_A3: # use -or- for greater sensitivity to touch, use -and- for more localized sensitivity to touch
            cp.pixels[ 8 ] = light_color
            output = output + " 8"
        else:
            cp.pixels[ 8 ] = OFF
        if output != "":
            print( "output", output )
