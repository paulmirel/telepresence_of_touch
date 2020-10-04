# Plot the values of the accelerometer. Click the "Plotter" button to show the plotted data.
# Adapted from:
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/acceleration

import time
from adafruit_circuitplayground import cp

while True:
    x, y, z = cp.acceleration
    print((x, y, z))

    time.sleep(0.1)
