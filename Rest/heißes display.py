import time
import board
import adafruit_dht
import RPi.GPIO as GPIO

# -----------------------------------------------------------
# 1. DER WICHTIGE RESET (Behebt deinen Fehler!)
# -----------------------------------------------------------
# Wir löschen alle alten Einstellungen, bevor wir starten.
try:
    GPIO.cleanup()
except:
    pass

# Jetzt stellen wir unseren Modus ein (BOARD = Pin Nummern 1-40)
#GPIO.setmode(GPIO.BOARD)
#GPIO.setwarnings(False)

# -----------------------------------------------------------
# 2. EINSTELLUNGEN (Deine Pins)
# -----------------------------------------------------------

# Display Pins
PIN_LCD_RS = 31
PIN_LCD_E  = 32
PIN_LCD_D4 = 33
PIN_LCD_D5 = 35
PIN_LCD_D6 = 36
PIN_LCD_D7 = 37

# LED Pins
PIN_ROT   = 15
PIN_GRUEN = 16
PIN_BLAU  = 18

# Knopf Pin
PIN_KNOPF = 12

# Sensor Einstellungen
# Der Sensor ist speziell. Er braucht "board.D4" (Das ist Pin 7)
try:
    mein_sensor = adafruit_dht.DHT11(board.D4)
except:
    print("Sensor nicht gefunden!")
    mein_sensor = None

# Grenzwerte
ZU_KALT = 18.0
ZU_HEISS = 25.0

# Merken, ob wir Celsius anzeigen (True = Ja, False = Nein)
zeige_celsius = True

# -----------------------------------------------------------
# 3. EINFACHE FUNKTIONEN
# -----------------------------------------------------------

def hardware_starten():
    print("Starte Hardware...")
    
    # Alle Pins als Ausgang (Strom raus) definieren
    GPIO.setup(PIN_LCD_RS, GPIO.OUT)
    GPIO.setup(PIN_LCD_E,  GPIO.OUT)
    GPIO.setup(PIN_LCD_D4, GPIO.OUT)
    GPIO.setup(PIN_LCD_D5, GPIO.OUT)
    GPIO.setup(PIN_LCD_D6, GPIO.OUT)
    GPIO.setup(PIN_LCD_D7, GPIO.OUT)
    
    GPIO.setup(PIN_ROT,   GPIO.OUT)
    GPIO.setup(PIN_GRUEN, GPIO.OUT)
    GPIO.setup(PIN_BLAU,  GPIO.OUT)
    
    # Knopf als Eingang (Strom messen). PUD_UP heißt: Pin ist AN, bis man drückt.
    GPIO.setup(PIN_KNOPF, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    # Wenn der Knopf gedrückt wird, rufe die Funktion 'knopf_gedrueckt' auf
    GPIO.add_event_detect(PIN_KNOPF, GPIO.FALLING, callback=knopf_gedrueckt, bouncetime=500)

    # Display startklar machen
    display_starten()

def knopf_gedrueckt(channel):
    # Diese Funktion läuft automatisch, wenn man drückt
    global zeige_celsius
    if zeige_celsius == True:
        zeige_celsius = False
        print("Knopf gedrückt: Wechsle zu Fahrenheit")
    else:
        zeige_celsius = True
        print("Knopf gedrückt: Wechsle zu Celsius")

def licht_machen(temperatur):
    # Erstmal alles ausmachen
    GPIO.output(PIN_ROT, GPIO.LOW)
    GPIO.output(PIN_GRUEN, GPIO.LOW)
    GPIO.output(PIN_BLAU, GPIO.LOW)
    
    # Jetzt die richtige Farbe anmachen
    if temperatur < ZU_KALT:
        GPIO.output(PIN_BLAU, GPIO.HIGH) # Blau an
    elif temperatur > ZU_HEISS:
        GPIO.output(PIN_ROT, GPIO.HIGH)  # Rot an
    else:
        GPIO.output(PIN_GRUEN, GPIO.HIGH) # Grün an

# -----------------------------------------------------------
# 4. HAUPTPROGRAMM (Hier läuft die Schleife)
# -----------------------------------------------------------

if __name__ == '__main__':
    try:
        display_starten()
        text_schreiben("Hallo!", 1) # Zeile 1
        text_schreiben("Geht los...", 2) # Zeile 2
        time.sleep(2)
        
        while True:
            try:
                # 1. Temperatur messen
                temp = mein_sensor.temperature
                feucht = mein_sensor.humidity
                
                # Prüfen ob Daten da sind (manchmal spinnt der Sensor)
                if temp is not None:
                    
                    # 2. LED Farbe setzen
                    licht_machen(temp)
                    
                    # 3. Text für das Display bauen
                    if zeige_celsius == True:
                        anzeige_wert = temp
                        einheit = "C"
                    else:
                        anzeige_wert = (temp * 9/5) + 32
                        einheit = "F"
                    
                    # Text zusammenbauen, z.B. "Temp: 22.5 C"
                    zeile1 = f"Temp: {anzeige_wert:.1f} {einheit}"
                    zeile2 = f"Feucht: {feucht:.1f} %"
                    
                    # 4. Auf Display schreiben
                    text_schreiben(zeile1, 1)
                    text_schreiben(zeile2, 2)
                    
                else:
                    print("Sensor Fehler (keine Daten)")

            except RuntimeError:
                # Das passiert oft beim DHT11, einfach ignorieren und nochmal versuchen
                pass
            
            # 2 Sekunden warten (Der Sensor ist langsam)
            time.sleep(2)
            
    except KeyboardInterrupt:
        print("Programm beendet.")
        GPIO.cleanup() # Wichtig: Aufräumen am Ende!

# -----------------------------------------------------------
# 5. TECHNIK-ECKE (Display Magie)
# Das hier muss man nicht verstehen, das steuert nur den Chip.
# -----------------------------------------------------------

def display_starten():
    lcd_byte_senden(0x33, GPIO.LOW)
    lcd_byte_senden(0x32, GPIO.LOW)
    lcd_byte_senden(0x28, GPIO.LOW)
    lcd_byte_senden(0x0C, GPIO.LOW)
    lcd_byte_senden(0x06, GPIO.LOW)
    lcd_byte_senden(0x01, GPIO.LOW)
    time.sleep(0.0005)

def text_schreiben(text, zeile):
    text = text.ljust(16, " ") # Text auf 16 Zeichen auffüllen
    
    if zeile == 1:
        lcd_byte_senden(0x80, GPIO.LOW) # Adresse Zeile 1
    else:
        lcd_byte_senden(0xC0, GPIO.LOW) # Adresse Zeile 2

    for buchstabe in text:
        lcd_byte_senden(ord(buchstabe), GPIO.HIGH)

def lcd_byte_senden(bits, modus):
    # Pins setzen
    GPIO.output(PIN_LCD_RS, modus)
    
    # Obere Hälfte senden
    GPIO.output(PIN_LCD_D4, GPIO.LOW)
    GPIO.output(PIN_LCD_D5, GPIO.LOW)
    GPIO.output(PIN_LCD_D6, GPIO.LOW)
    GPIO.output(PIN_LCD_D7, GPIO.LOW)
    if bits & 0x10 == 0x10: GPIO.output(PIN_LCD_D4, GPIO.HIGH)
    if bits & 0x20 == 0x20: GPIO.output(PIN_LCD_D5, GPIO.HIGH)
    if bits & 0x40 == 0x40: GPIO.output(PIN_LCD_D6, GPIO.HIGH)
    if bits & 0x80 == 0x80: GPIO.output(PIN_LCD_D7, GPIO.HIGH)
    
    time.sleep(0.0005)
    GPIO.output(PIN_LCD_E, GPIO.HIGH)
    time.sleep(0.0005)
    GPIO.output(PIN_LCD_E, GPIO.LOW)
    time.sleep(0.0005)
    
    # Untere Hälfte senden
    GPIO.output(PIN_LCD_D4, GPIO.LOW)
    GPIO.output(PIN_LCD_D5, GPIO.LOW)
    GPIO.output(PIN_LCD_D6, GPIO.LOW)
    GPIO.output(PIN_LCD_D7, GPIO.LOW)
    if bits&0x01==0x01: GPIO.output(PIN_LCD_D4, GPIO.HIGH)
    if bits&0x02==0x02: GPIO.output(PIN_LCD_D5, GPIO.HIGH)
    if bits&0x04==0x04: GPIO.output(PIN_LCD_D6, GPIO.HIGH)
    if bits&0x08==0x08: GPIO.output(PIN_LCD_D7, GPIO.HIGH)
    
    time.sleep(0.0005)
    GPIO.output(PIN_LCD_E, GPIO.HIGH)
    time.sleep(0.0005)
    GPIO.output(PIN_LCD_E, GPIO.LOW)
    time.sleep(0.0005)