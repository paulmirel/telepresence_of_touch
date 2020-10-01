# Use the Circuit Playground's little speaker to play tones.
# Upload the code, then press the "A" button.
# https://learn.adafruit.com/circuitpython-made-easy-on-circuit-playground-express/play-tone
from adafruit_circuitplayground import cp

while True:
    # Only play if the A button is pressed.
    if cp.button_a:
        # The first value is the frequency of the tone. The second value is the time, in seconds.
        # Writing notes this way is not very fun. I'll show a different way in the next example.
        cp.play_tone(659, 0.2)
        cp.play_tone(622, 0.2)
        cp.play_tone(659, 0.2)
        cp.play_tone(622, 0.2)
        cp.play_tone(659, 0.2)
        cp.play_tone(494, 0.2)
        cp.play_tone(587, 0.2)
        cp.play_tone(523, 0.2)
        cp.play_tone(440, 0.4)
