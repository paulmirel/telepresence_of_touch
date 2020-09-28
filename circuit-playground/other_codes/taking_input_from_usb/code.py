import supervisor
import time
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.6

light_color = ( 255, 0, 0 )
OFF = ( 0, 0, 0 )


while True:
    cp.pixels[ 1 ] = light_color
    time.sleep( 0.5 )
    cp.pixels[ 1 ] = OFF
    time.sleep( 0.5 )
    if supervisor.runtime.serial_bytes_available:
        value = input().strip()
        # Sometimes Windows sends an extra (or missing) newline - ignore them
        if value != "":
            print("RX: {}".format(value))
