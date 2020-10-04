# A bit more complex project that maps the capacitive pads to drum samples.
# Copy the samples in the folder to the CIRCUITPY disk, next to the code.py file.
# https://learn.adafruit.com/adafruit-circuit-playground-bluefruit/playground-drum-machine

from adafruit_circuitplayground import cp

cp.pixels.brightness = 0.3

while True:
    if cp.touch_A1:
        cp.pixels.fill((100, 0, 0))
        cp.play_file('bass_hit_c.wav')
        cp.pixels.fill((0, 0, 0))
    elif cp.touch_A2:
        cp.pixels.fill((0, 100, 0))
        cp.play_file('bd_tek.wav')
        cp.pixels.fill((0, 0, 0))
    elif cp.touch_A3:
        cp.pixels.fill((0, 0, 100))
        cp.play_file('bd_zome.wav')
        cp.pixels.fill((0, 0, 0))
    elif cp.touch_A4:
        cp.pixels.fill((100, 100, 0))
        cp.play_file('drum_cowbell.wav')
        cp.pixels.fill((0, 0, 0))
    elif cp.touch_A5:
        cp.pixels.fill((100, 0, 100))
        cp.play_file('elec_blip2.wav')
        cp.pixels.fill((0, 0, 0))
    elif cp.touch_A6:
        cp.pixels.fill((100, 100, 100))
        cp.play_file('elec_cymbal.wav')
        cp.pixels.fill((0, 0, 0))
    elif cp.touch_TX:
        cp.pixels.fill((0, 50, 100))
        cp.play_file('elec_hi_snare.wav')
        cp.pixels.fill((0, 0, 0))
