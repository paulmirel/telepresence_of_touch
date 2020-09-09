import time
import board
import digitalio

led = digitalio.DigitalInOut(board.A1)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(1.0)
    led.value = False
    time.sleep(1.0)
