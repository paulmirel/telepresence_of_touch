from adafruit_circuitplayground.express import cpx
import time

cpx.pixels.brightness = 0.3

while True:
    x, y, z = cpx.acceleration
    sum_accel = abs(x) + abs(y) + abs(z)
    print((sum_accel, 2))
    if sum_accel < 2:
        cpx.pixels.fill((255,0,0))
        cpx.play_file("yikes.wav")
    else:
        cpx.pixels.fill((0,255,0))
    time.sleep(0.1)


