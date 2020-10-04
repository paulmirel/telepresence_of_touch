# Plot the values of the temperature sensor. Click the "Plotter" button to show the plotted data.
# Adapted from:
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/temperature

import time
from adafruit_circuitplayground import cp

while True:
    print("Temperature C:", cp.temperature)
    print("Temperature F:", cp.temperature * 1.8 + 32)
    print((cp.temperature, cp.temperature * 1.8 + 32))
    time.sleep(0.1)
