# Bibliotheken importieren
import RPi.GPIO as GPIO
import dht11
import time

#Zaehlvariable 
i = 0

#+----------------+
#| Pin Belegungen |
#+----------------+

# Display
LCD_RS = 40
LCD_E = 37
LCD_DATA4 = 38
LCD_DATA5 = 35
LCD_DATA6 = 36
LCD_DATA7 = 33

# Knopf
BUTTON_PIN = 22

# LED
RED_PIN = 13
GREEN_PIN = 11
BLUE_PIN = 15

# Sensor
TEMP_PIN = dht11.DHT11(pin=12)


#+-------------+
#| GPIO Config |
#+-------------+

# Allgemein
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD) # Benutzt physische Pin-Nummerierung

# Display
LCD_WIDTH = 16
LCD_LINE_1 = 0x80
LCD_LINE_2 = 0xC0
LCD_CHR = GPIO.HIGH
LCD_CMD = GPIO.LOW
E_PULSE = 0.0005
E_DELAY = 0.0005

# Display Setup
GPIO.setup(LCD_E, GPIO.OUT)
GPIO.setup(LCD_RS, GPIO.OUT)
GPIO.setup(LCD_DATA4, GPIO.OUT)
GPIO.setup(LCD_DATA5, GPIO.OUT)
GPIO.setup(LCD_DATA6, GPIO.OUT)
GPIO.setup(LCD_DATA7, GPIO.OUT)

# LED Setup
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

# Knopf Setup
GPIO.setup(BUTTON_PIN, GPIO.IN)


#+-----------------------+
#| Funktionen definieren |
#+-----------------------+

# Display
def lcd_send_byte(bits, mode):                        # Sendet die Infos ans Display
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

def lcd_message(message):                             # Formatiert und sendet den Text an das Display
    message = message.ljust(LCD_WIDTH," ")  
    for i in range(LCD_WIDTH):
      lcd_send_byte(ord(message[i]),LCD_CHR)

def ausgabe_temp_C(temC, humid):                      # Gibt die Temperatur (in Celsius) und Luftfeuchtigkeit (engl. Humid aus Platzgruenden) auf dem Display aus
  lcd_send_byte(LCD_LINE_1, LCD_CMD)
  lcd_message(f"Temp: {temC:.1f} C")
  lcd_send_byte(LCD_LINE_2, LCD_CMD)
  lcd_message(f"Humid: {humid:.1f} %")

def ausgabe_temp_F(temC, humid):                      # Gibt die Temperatur (in Fahrenheit) und Luftfeuchtigkeit (engl. Humid aus Platzgruenden) auf dem Display aus
  temF = (temC * 1.8 + 32)
  lcd_send_byte(LCD_LINE_1, LCD_CMD)
  lcd_message(f"Temp: {temF:.1f} F")
  lcd_send_byte(LCD_LINE_2, LCD_CMD)
  lcd_message(f"Humid: {humid:.1f} %")

# Display initiieren 
display_init()

#+-----------+
#| Main Code |
#+-----------+

try:
   while True:                                        # Schleife, die sich endlos wiederholt aber durch KeyboardInterrupt (also strg + C) unterbrochen werden kann
      result = TEMP_PIN.read()
      if result.is_valid():
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:        # Laesst den Knopf mithilfe der Zaehlvariable als Toggle arbeiten
          i = 1 - i
        if i == 0:
         ausgabe_temp_C(result.temperature, result.humidity)
        else:
          ausgabe_temp_F(result.temperature, result.humidity)
        if result.temperature < 20:
          GPIO.output(RED_PIN, GPIO.LOW)
          GPIO.output(BLUE_PIN, GPIO.HIGH)
          GPIO.output(GREEN_PIN, GPIO.LOW)
        elif result.temperature > 24:
          GPIO.output(RED_PIN, GPIO.HIGH)
          GPIO.output(BLUE_PIN, GPIO.LOW)
          GPIO.output(GREEN_PIN, GPIO.LOW)
        else:
          GPIO.output(RED_PIN, GPIO.LOW)
          GPIO.output(BLUE_PIN, GPIO.LOW)
          GPIO.output(GREEN_PIN, GPIO.HIGH)
        time.sleep(0.1)

except KeyboardInterrupt:                             # Unterbricht die Schleife und bereinigt das GPIO-Setup
  time.sleep(0.5)
  lcd_send_byte(LCD_LINE_1, LCD_CMD)
  lcd_message(f"Programm")
  lcd_send_byte(LCD_LINE_2, LCD_CMD)
  lcd_message(f"Beendet")
  time.sleep(2)
  GPIO.output(RED_PIN, GPIO.LOW)
  GPIO.output(BLUE_PIN, GPIO.LOW)
  GPIO.output(GREEN_PIN, GPIO.LOW)
  GPIO.cleanup()
