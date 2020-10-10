# Functions to make a random color, and seed the random function decently
# Usage
#   from unrvl.random_color import seed_the_random, random_color 
#   at setup time:
#       seed_the_random() # decent random seeding
#   When you want a random rgb (high-saturation):
#       someRGB = random_color()

import time
import random
from adafruit_circuitplayground import cp

def seed_the_random():
    # seed the random generator, random.seed(x) doesn't actually change much!
    # But, getting N randoms, if N is noise, works
    seed = cp.light + cp.temperature + time.monotonic()
    seed = (seed - int(seed)) * 100
    random.seed(int(seed))
    for i in range(seed % 100):
        random.random()

def random_color():
    # pick a random color, but near the rim of the color wheel (high saturation/value)
    rg_or_b = random.uniform(1,3.99)
    if rg_or_b >= 3:
        blue = int(255 * (rg_or_b - 3))
        green = 255 - blue
        red = 0
    elif rg_or_b >= 2:
        green = int(255 * (rg_or_b - 2))
        blue = 255 - green
        red = 0
    else:
        red = int(255 * (rg_or_b - 1))
        green = 255 - red
        blue = 0
    return (red,green,blue)
