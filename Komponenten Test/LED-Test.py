# Programm zum Testen der LED

import time
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#+----------+
#| LED Pins |
#+----------+
RED_PIN = 11
GREEN_PIN = 13
BLUE_PIN = 15

GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

try:
    while True:
        # Rot an
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        time.sleep(1)

        # Grün an
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        GPIO.output(BLUE_PIN, GPIO.LOW)
        time.sleep(1)

        # Blau an
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        GPIO.output(BLUE_PIN, GPIO.HIGH)
        time.sleep(1)

except KeyboardInterrupt:
    # Sauberes Beenden: Setzt alle Pins zurück
    GPIO.cleanup()
    print("\nTest beendet.")