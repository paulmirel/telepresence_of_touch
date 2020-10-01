# Measure the light level, then light up a number of pixels based on that level.
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/light

import time
from adafruit_circuitplayground import cp

# Because we're turning on a bunch of pixels at the same time, don't automatically turn them on/off, because they would flicker.
cp.pixels.auto_write = False
cp.pixels.brightness = 0.3


def convert_range(v, in_min, in_max, out_min, out_max):
    # Convert first to a value between 0.0 - 1.0
    v = (v - in_min) / (in_max - in_min)
    # Convert this value to output range.
    return out_min + v * (out_max - out_min)


while True:
    # Scale the light input value from 0-320 to NeoPixel value (0-9).
    peak = convert_range(cp.light, 0, 320, 0, 9)

    # Go through all the pixels and turn them on/off, as long as we haven't reached the peak yet.
    for i in range(10):
        if i <= peak:
            cp.pixels[i] = (0, 255, 255)
        else:
            cp.pixels[i] = (0, 0, 0)

    # Because we set auto_write to False, we need to explicitly call "show" to turn on the pixels.
    cp.pixels.show()

    # Wait a bit.
    time.sleep(0.05)
