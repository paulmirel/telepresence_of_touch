# Get the output of the light meter and print it in a format that can also be plotted.
# Click on the "Plot" button to show a graph of the light level over time.
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/light

import time
from adafruit_circuitplayground import cp

while True:
    # To plot a value, you need a specific format, which in Python is called a tuple.
    # If you have just one value to plot, you need this weird double bracket-and-a-comma format.
    print((cp.light,))
    time.sleep(0.1)
