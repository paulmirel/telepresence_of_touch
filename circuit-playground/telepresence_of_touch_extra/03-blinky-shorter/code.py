# This is the same example as before, but a bit shorter. It shows a "toggle" coding technique:
# we take the old value of red_led (which is either True or False), flip that state using the "not" keyword,
# then storing that in red_led again.
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/red-led
import time
from adafruit_circuitplayground import cp

while True:
    cp.red_led = not cp.red_led
    time.sleep(0.5)
