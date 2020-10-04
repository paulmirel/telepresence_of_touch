# Copy "never-gonna-give-you-up.wav" to the CIRCUITPY disk, next to the code.py file.
# Press the A button to play.
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/play-file
from adafruit_circuitplayground import cp

while True:
    if cp.button_a:
        cp.play_file("never-gonna-give-you-up.wav")
