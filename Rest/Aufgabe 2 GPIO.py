import RPi.GPIO as GPIO
import time

led_r = 33
led_g = 35
led_b = 37
switch = 31

GPIO.setmode(GPIO.BOARD)
GPIO.setup(led_r, GPIO.OUT)
GPIO.setup(led_g, GPIO.OUT)
GPIO.setup(led_b, GPIO.OUT)
GPIO.setup(switch, GPIO.IN)

status = 0

for i in range(5):                                                 
    if GPIO.input(switch) == 1:
        status += 1
    
    if status > 3:
        status = 0
    
    if status == 0:
        GPIO.output(led_b, GPIO.LOW)
        GPIO.output(led_r, GPIO.LOW)
        GPIO.output(led_g, GPIO.LOW)
        time.sleep(0.5)

    elif status == 1:
        GPIO.output(led_r, GPIO.HIGH)
        GPIO.output(led_g, GPIO.LOW)
        GPIO.output(led_b, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(led_r, GPIO.LOW)
    
    elif status == 2:
        GPIO.output(led_g, GPIO.HIGH)
        GPIO.output(led_r, GPIO.LOW)
        GPIO.output(led_b, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(led_g, GPIO.LOW)
    
    elif status == 3:
        GPIO.output(led_b, GPIO.HIGH)
        GPIO.output(led_r, GPIO.LOW)
        GPIO.output(led_g, GPIO.LOW)
        time.sleep(0.5)
        GPIO.output(led_b, GPIO.LOW)
    
    else:
        time.sleep(0.5)
    
    print('Switch status = ', GPIO.input(switch))
    print("Zählvariable: ",status)
    

"""
for i in range(10):
    if GPIO.input(switch) == 1:
        GPIO.output(led, GPIO.HIGH)
        time.sleep(0.2)
    GPIO.output(led, GPIO.LOW)
    time.sleep(0.2)
    print('Switch status = ', GPIO.input(switch))
    
GPIO.cleanup()
"""
GPIO.cleanup()
