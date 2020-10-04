# Use the Circuit Playground's little speaker to play sounds.
# Map the capacative touch pads to frequency values.
# Here we use start_tone and stop_tone to leave the note playing as long as we're touching a pad.
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/start-and-stop-tone
from adafruit_circuitplayground import cp

# Note frequencies from https://pages.mtu.edu/~suits/notefreqs.html
C4 = 261.63
D4 = 293.66
E4 = 329.63
F4 = 349.23
G4 = 392.00
A4 = 440.00
B4 = 493.88


while True:
    if cp.touch_A1:
        cp.start_tone(C4)
    elif cp.touch_A2:
        cp.start_tone(D4)
    elif cp.touch_A3:
        cp.start_tone(E4)
    elif cp.touch_A4:
        cp.start_tone(F4)
    elif cp.touch_A5:
        cp.start_tone(G4)
    elif cp.touch_A6:
        cp.start_tone(A4)
    elif cp.touch_TX:
        cp.start_tone(B4)
    else:
        cp.stop_tone()
