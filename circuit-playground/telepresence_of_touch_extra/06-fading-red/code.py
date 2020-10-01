# This example uses a variable, called "red", that gradually increases its value, creating a fade-in effect.
# If the value goes above a certain value (50 by default, but you can change that) it resets back to zero.

from adafruit_circuitplayground import cp
import time

red = 0
while True:
    cp.pixels.fill((red, 0, 0))
    red += 1
    if red > 50:
        red = 0
    time.sleep(0.05)
