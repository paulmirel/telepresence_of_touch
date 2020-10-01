# We'll turn on/off the led in an infinite loop, using time.sleep to wait a bit every time.
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/red-led

import time
from adafruit_circuitplayground import cp

while True:
    cp.red_led = True
    time.sleep(0.5)
    cp.red_led = False
    time.sleep(0.5)
