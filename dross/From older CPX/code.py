from adafruit_circuitplayground.express import cpx
import time

cpx.pixels.brightness = 0.04

while True:
    if cpx.touch_A1:
        cpx.pixels.fill ((255,0,0))
    time.sleep(3.0)
    cpx.pixels.fill ((0,255,0))
    time.sleep(3.0)
