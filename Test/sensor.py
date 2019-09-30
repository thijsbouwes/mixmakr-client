import RPi.GPIO as GPIO
from time import sleep

SENSOR1 = 26
SENSOR2 = 19
GPIO.setmode(GPIO.BCM)

def pressed(pin):
    print("OLA 1", pin)

GPIO.setup(SENSOR1, GPIO.IN)
GPIO.setup(SENSOR2, GPIO.IN)
GPIO.add_event_detect(SENSOR1, GPIO.FALLING, callback=pressed, bouncetime=100)
GPIO.add_event_detect(SENSOR2, GPIO.FALLING, callback=pressed, bouncetime=100)

try:
    print("start")
    input()
except KeyboardInterrupt:
    GPIO.cleanup()

