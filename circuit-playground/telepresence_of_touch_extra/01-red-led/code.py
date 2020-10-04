# The Circuit Playground has a small red led next to the USB port. This script turns on the led.
# Hey, we have to start somewhere :-)
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/red-led

from adafruit_circuitplayground import cp

while True:
    cp.red_led = True
