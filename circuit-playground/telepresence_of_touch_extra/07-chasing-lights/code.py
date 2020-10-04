# Create a "chasing lights" effect.
# To create this I've created an "index" variable that gets increased by one each time.
# Instead of turning on always the same pixel I select the pixel dynamically by using cp.pixels[index].
# This selects the pixel pointed to by the current index.
from adafruit_circuitplayground import cp
import time

# Initialize a variable called "index".
# The name is something I can choose myself; I could call it "hamburger" as well but index sounds appropriate.
index = 0

while True:
    # Turn off all the pixels. This turns off the previous highlighted pixel.
    cp.pixels.fill((0, 0, 0))

    # Turn on a single specific pixel as set in the index value.
    # So the first time this is pixel 0, then pixel 1, and so on.
    cp.pixels[index] = (100, 100, 100)

    # Increase the index, and reset it back to zero if it's bigger than 9.
    # Indexes of the NeoPixels go from 0-9, so values larger than 9 would not work.
    index += 1
    if index > 9:
        index = 0

    # Wait for a bit. Play with this value to make the effect go slower or faster.
    time.sleep(0.05)
