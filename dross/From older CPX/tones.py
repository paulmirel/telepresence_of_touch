from adafruit_circuitplayground.express import cpx
import time

cpx.play_tone(1500, 0.50)
time.sleep(1.0)
cpx.pixels.fill ((0,0,255))
cpx.play_tone(1200, 0.50)
time.sleep(1.0)
cpx.pixels.fill ((0,0,255))
cpx.play_tone(1000, 0.50)
time.sleep(1.0)
cpx.pixels.fill ((0,0,255))
cpx.play_tone(1000, 0.50)
time.sleep(1.0)
cpx.pixels.fill ((0,0,255))
cpx.play_tone(1000, 0.50)
time.sleep(1.0)

