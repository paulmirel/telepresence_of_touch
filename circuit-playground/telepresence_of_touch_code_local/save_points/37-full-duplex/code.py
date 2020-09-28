import time
import supervisor
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.6
light_color = ( 255, 0, 0 )
OFF = ( 0, 0, 0 )

while True:
    if cp.touch_A4:
        cp.pixels[ 1 ] = light_color
        print( "01" )
    else:
        cp.pixels[ 1 ] = OFF
        print( "00" )

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

