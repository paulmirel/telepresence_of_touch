# The Circuit Playground Express and Bluefruit have ten RGB NeoPixel LEDs built in.
# The fill command turns on all the pixels at the same time. The three values are R/G/B.
# Try changing the color.
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/neopixels

from adafruit_circuitplayground import cp

while True:
    cp.pixels.fill((50, 0, 0))
