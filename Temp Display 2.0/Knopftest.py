import RPi.GPIO as GPIO
import time

# 1. PIN-Nummerierung festlegen (BCM entspricht den GPIO-Nummern)
GPIO.setmode(GPIO.BOARD)

# 2. HIER DEFINIEREN WIR DIE VARIABLE (Der Fehlerteufel)
# Ersetze die 22 durch den Pin, an dem dein Signal-Kabel steckt
BUTTON_PIN = 22 

# 3. Den Pin als Eingang festlegen
GPIO.setup(BUTTON_PIN, GPIO.IN)

print("--- Status-Monitor (RPi.GPIO) ---")

try:
    while True:
        # Den Status des Pins auslesen
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            print("Status: [ GEDRÜCKT ]     ", end="\r")
        else:
            print("Status: [ Nicht gedrückt ]", end="\r")
        
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nBeendet durch Nutzer.")
finally:
    GPIO.cleanup() # Wichtig, um die Pins wieder freizugeben