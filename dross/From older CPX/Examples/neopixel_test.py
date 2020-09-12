import time
from adafruit_circuitplayground.express import cpx
cpx.pixels.fill((255, 0, 0))
time.sleep(1.0)
cpx.pixels.fill((0, 255, 0))
time.sleep(1.0)
cpx.pixels.fill((0, 0, 255))
time.sleep(1.0)
