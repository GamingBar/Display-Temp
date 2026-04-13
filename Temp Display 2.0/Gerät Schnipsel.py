# Code Funktionen für die Geräte

# Pin Config
GPIO.setmode(GPIO.BOARD)


# -------
# Display
# -------

# Pin Belegung:
    LCD_RS = 40
    LCD_E = 37
    LCD_DATA4 = 38
    LCD_DATA5 = 35
    LCD_DATA6 = 36
    LCD_DATA7 = 33

# Code zur Formartierung des Textes:
    LCD_WIDTH = 16        # Zeichen je Zeile
    LCD_LINE_1 = 0x80     # Adresse der ersten Display Zeile
    LCD_LINE_2 = 0xC0     # Adresse der zweiten Display Zeile
    LCD_CHR = GPIO.HIGH
    LCD_CMD = GPIO.LOW
    E_PULSE = 0.0005
    E_DELAY = 0.0005

# def fürs Display:
    def lcd_send_byte(bits, mode):                        # Sendet die Infos ans Display (von 8 zu 4 Bit)
      # Pins auf LOW setzen
      GPIO.output(LCD_RS, mode)
      GPIO.output(LCD_DATA4, GPIO.LOW)
      GPIO.output(LCD_DATA5, GPIO.LOW)
      GPIO.output(LCD_DATA6, GPIO.LOW)
      GPIO.output(LCD_DATA7, GPIO.LOW)
      if bits & 0x10 == 0x10:
        GPIO.output(LCD_DATA4, GPIO.HIGH)
      if bits & 0x20 == 0x20:
        GPIO.output(LCD_DATA5, GPIO.HIGH)
      if bits & 0x40 == 0x40:
        GPIO.output(LCD_DATA6, GPIO.HIGH)
      if bits & 0x80 == 0x80:
        GPIO.output(LCD_DATA7, GPIO.HIGH)
      time.sleep(E_DELAY)    
      GPIO.output(LCD_E, GPIO.HIGH)  
      time.sleep(E_PULSE)
      GPIO.output(LCD_E, GPIO.LOW)  
      time.sleep(E_DELAY)      
      GPIO.output(LCD_DATA4, GPIO.LOW)
      GPIO.output(LCD_DATA5, GPIO.LOW)
      GPIO.output(LCD_DATA6, GPIO.LOW)
      GPIO.output(LCD_DATA7, GPIO.LOW)
      if bits&0x01==0x01:
        GPIO.output(LCD_DATA4, GPIO.HIGH)
      if bits&0x02==0x02:
        GPIO.output(LCD_DATA5, GPIO.HIGH)
      if bits&0x04==0x04:
        GPIO.output(LCD_DATA6, GPIO.HIGH)
      if bits&0x08==0x08:
        GPIO.output(LCD_DATA7, GPIO.HIGH)
      time.sleep(E_DELAY)    
      GPIO.output(LCD_E, GPIO.HIGH)  
      time.sleep(E_PULSE)
      GPIO.output(LCD_E, GPIO.LOW)  
      time.sleep(E_DELAY)
 
    def display_init():                                   # Bereinigt das Display zum Start
        lcd_send_byte(0x33, LCD_CMD)
        lcd_send_byte(0x32, LCD_CMD)
        lcd_send_byte(0x28, LCD_CMD)
        lcd_send_byte(0x0C, LCD_CMD)  
        lcd_send_byte(0x06, LCD_CMD)
        lcd_send_byte(0x01, LCD_CMD)  
 
    def lcd_message(message):                             # Formatiert und sendet den Text an das Display.
        message = message.ljust(LCD_WIDTH," ")  
        for i in range(LCD_WIDTH):
        lcd_send_byte(ord(message[i]),LCD_CHR)

# Vorbereiten des Displays
  if __name__ == '__main__':                            # Steuert den Ablauf zum Textsenden.
    # initialisieren zur Pin und Datenzuordnung
    GPIO.setmode(GPIO.BOARD)
    GPIO.setwarnings(False)
    GPIO.setup(LCD_E, GPIO.OUT)
    GPIO.setup(LCD_RS, GPIO.OUT)
    GPIO.setup(LCD_DATA4, GPIO.OUT)
    GPIO.setup(LCD_DATA5, GPIO.OUT)
    GPIO.setup(LCD_DATA6, GPIO.OUT)
    GPIO.setup(LCD_DATA7, GPIO.OUT)
 
    display_init()                                   # Startet Routine zum Starten und bereinigen des Displays zum Start
 

# Beispiel für Textausgabe:    
    lcd_send_byte(LCD_LINE_1, LCD_CMD)               # Springe in die erste Zeile
    lcd_message("Was geht")                          # Text der ersten Zeile
    lcd_send_byte(LCD_LINE_2, LCD_CMD)               # Springe in die zweite Zeile
    lcd_message("Mein bester")                       # Text der ersten Zeile



#-------
# Knopf
#-------

# Knopf Pins
BUTTON_PIN = 22

# Pin als Eingang festlegen
GPIO.setup(BUTTON_PIN, GPIO.IN)

# Input Code
GPIO.input(BUTTON_PIN) == GPIO.LOW      # Knopf nicht gedrückt
GPIO.input(BUTTON_PIN) == GPIO.HIGH     # Knopf gedrückt



#-----
# LED
#-----

# Pins
GREEN_PIN = 11
RED_PIN = 13

# LEDs auf aus stellen (für Start)
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)

# LEDs als Ausgang verwenden
GPIO.output(RED_PIN, GPIO.HIGH)     # LED an
GPIO.output(GREEN_PIN, GPIO.LOW)    # LED aus