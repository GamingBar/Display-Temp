import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

GPIO.setwarnings(False)

RED_PIN = 13
GREEN_PIN = 11

GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

try:
    while True:
        # Rot an
        GPIO.output(RED_PIN, GPIO.HIGH)
        GPIO.output(GREEN_PIN, GPIO.LOW)
        time.sleep(1)

        # Grün an
        GPIO.output(RED_PIN, GPIO.LOW)
        GPIO.output(GREEN_PIN, GPIO.HIGH)
        time.sleep(1)

except KeyboardInterrupt:
    # Sauberes Beenden: Setzt alle Pins zurück
    GPIO.cleanup()
    print("\nProgramm beendet.")