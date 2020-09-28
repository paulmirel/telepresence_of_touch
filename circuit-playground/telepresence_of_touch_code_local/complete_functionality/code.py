import supervisor
import time
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

    if cp.touch_A6:
        cp.pixels[ 3 ] = light_color
        print( "11" )
    else:
        cp.pixels[ 3 ] = OFF
        print( "10" )

    if cp.touch_A1:
        cp.pixels[ 6 ] = light_color
        print( "21" )
    else:
        cp.pixels[ 6 ] = OFF
        print( "20" )

    if cp.touch_A3:
        cp.pixels[ 8 ] = light_color
        print( "31" )
    else:
        cp.pixels[ 8 ] = OFF
        print( "30" )


    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        # Sometimes Windows sends an extra (or missing) newline - ignore them
        if value != "":
            print("Received: {}".format(value))
            if value == "01":
                cp.pixels[ 0 ] = light_color
            if value == "00":
                cp.pixels[ 0 ] = OFF
            if value == "11":
                cp.pixels[ 4 ] = light_color
            if value == "10":
                cp.pixels[ 4 ] = OFF
            if value == "21":
                cp.pixels[ 5 ] = light_color
            if value == "20":
                cp.pixels[ 5 ] = OFF
            if value == "31":
                cp.pixels[ 9 ] = light_color
            if value == "30":
                cp.pixels[ 9 ] = OFF
    time.sleep( 0.05 )
