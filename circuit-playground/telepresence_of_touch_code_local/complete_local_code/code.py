# Telepresence of Touch for the CircuitPlayground
# https://github.com/paulmirel/telepresence_of_touch
# telepresence_of_touch_code_local
# Paul Mirel and Alan Grover
# Maryland Institute College of Art (MICA)
# 20200928

import time
import supervisor
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.6
light_color = ( 255, 0, 0 )
OFF = ( 0, 0, 0 )

LastTouched = [False, False, False, False] # 4 entries for 4 quadrants

while True:
    # Quandrant 0 local
    if cp.touch_A4:
        if not LastTouched[ 0 ]: # if the touch is different than it last was.
            cp.pixels[ 1 ] = light_color
            print( "01" )
            LastTouched[ 0 ] = True # touch detected, remember that
    elif LastTouched[ 0 ]:
        cp.pixels[ 1 ] = OFF
        print( "00" )
        LastTouched[ 0 ] = False # no touch detected, remember that.

    # Quandrant 1 local
    if cp.touch_A6:
        if not LastTouched[ 1 ]: # if the touch is different than it last was.
            cp.pixels[ 3 ] = light_color
            print( "11" )
            LastTouched[ 1 ] = True # touch detected, remember that
    elif LastTouched[ 1 ]:
        cp.pixels[ 3 ] = OFF
        print( "10" )
        LastTouched[ 1 ] = False # no touch detected, remember that.

    # Quandrant 2 local
    if cp.touch_A1:
        if not LastTouched[ 2 ]: # if the touch is different than it last was.
            cp.pixels[ 6 ] = light_color
            print( "21" )
            LastTouched[ 2 ] = True # touch detected, remember that
    elif LastTouched[ 2 ]:
        cp.pixels[ 6 ] = OFF
        print( "20" )
        LastTouched[ 2 ] = False # no touch detected, remember that.

    # Quandrant 3 local
    if cp.touch_A3:
        if not LastTouched[ 3 ]: # if the touch is different than it last was.
            cp.pixels[ 8 ] = light_color
            print( "31" )
            LastTouched[ 3 ] = True # touch detected, remember that
    elif LastTouched[ 3 ]:
        cp.pixels[ 8 ] = OFF
        print( "30" )
        LastTouched[ 3 ] = False # no touch detected, remember that.

    # telepresence check
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        # Sometimes Windows sends an extra (or missing) newline
        # strip them off the input to ignore them
        print("Received: {}".format(value))

    # Quandrant 0 telepresent
        if value == "01":
            cp.pixels[ 0 ] = light_color
        if value == "00":
            cp.pixels[ 0 ] = OFF

    # Quandrant 1 telepresent
        if value == "11":
            cp.pixels[ 4 ] = light_color
        if value == "10":
            cp.pixels[ 4 ] = OFF

    # Quandrant 2 telepresent
        if value == "21":
            cp.pixels[ 5 ] = light_color
        if value == "20":
            cp.pixels[ 5 ] = OFF

    # Quandrant 3 telepresent
        if value == "31":
            cp.pixels[ 9 ] = light_color
        if value == "30":
            cp.pixels[ 9 ] = OFF

    time.sleep( 0.1 ) #pause to be able to hear a ctrl-c