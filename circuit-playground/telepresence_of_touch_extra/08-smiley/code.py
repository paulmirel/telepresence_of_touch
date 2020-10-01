from adafruit_circuitplayground import cp

# The NeoPixels are super-bright. Change the global brightness.
cp.pixels.brightness = 0.3

while True:
    # The smiley's eyes
    cp.pixels[0] = (255, 0, 0)
    cp.pixels[9] = (255, 0, 0)

    # The smiley's mouth
    cp.pixels[3] = (255, 0, 255)
    cp.pixels[4] = (255, 0, 255)
    cp.pixels[5] = (255, 0, 255)
    cp.pixels[6] = (255, 0, 255)
