import dht11
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
sensor_pin = 7
led_r = 16
led_b = 18

GPIO.setup(led_b, GPIO.OUT)
GPIO.setup(led_r, GPIO.OUT)

sensor = dht11.DHT11(pin=sensor_pin)


try:
    while True:
        result = sensor.read()

        if result.is_valid():
            print(f'Temperature: {result.temperature}°C, Luftfeuchtigkeit: {result.humidity}%')
            GPIO.output(led_r, GPIO.LOW)
            GPIO.output(led_b, GPIO.HIGH)
        else:
            print('Leck Eier')
            GPIO.output(led_b, GPIO.LOW)
            GPIO.output(led_r, GPIO.HIGH)

        time.sleep(2)

except KeyboardInterrupt:
    print("Programm beendet")
finally:
    GPIO.cleanup()