# Programm zum Testen des Knopfes

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#+------------+
#| Button Pin |
#+------------+

BUTTON_PIN = 20     # Pinbelegung
GPIO.setup(BUTTON_PIN, GPIO.IN)

#+------------------+
#| Code und Ausgabe |
#+------------------+
print("-- Status-Monitor ---")

try:
    while True:
        # Den Status des Pins auslesen
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Status: [ GEDRÜCKT ]     ", end="\r")
        else:
            print("Status: [ Nicht gedrückt ]", end="\r")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\Test beendet.")
finally:
    GPIO.cleanup() # Wichtig, um die Pins wieder freizugeben