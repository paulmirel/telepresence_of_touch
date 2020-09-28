import time
import supervisor
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.6
light_color = ( 255, 0, 0 )
OFF = ( 0, 0, 0 )

LastTouched = [False, False, False, False] # 4 entries for 4 quadrants
while True:
    if cp.touch_A4 and not LastTouched[ 0 ]: # if the touch is different than it last was.
        cp.pixels[ 1 ] = light_color
        print( "01" )
        LastTouched[ 0 ] = True # touch detected, remember that
    elif LastTouched[ 0 ]:
        cp.pixels[ 1 ] = OFF
        print( "00" )
        LastTouched[ 0 ] = False # no touch detected, remember that.

    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        # Sometimes Windows sends an extra (or missing) newline
        # strip them off the input to ignore them
        print("Received: {}".format(value))
        if value == "01":
            cp.pixels[ 0 ] = light_color
        if value == "00":
            cp.pixels[ 0 ] = OFF
    time.sleep( 0.1 ) #pause to be able to hear a ctrl-c

