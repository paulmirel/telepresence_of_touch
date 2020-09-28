import time
from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.6
light_color = ( 255, 0, 0 ) #( red, green, blue ) each 0-255
OFF = ( 0, 0, 0 )

while True:
    if cp.touch_A4:
        cp.pixels[ 1 ] = light_color
    else:
        cp.pixels[ 1 ] = OFF
    time.sleep( 0.1 )



