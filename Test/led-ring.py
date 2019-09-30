import RPi.GPIO as GPIO
from time import sleep
import board
import neopixel

LED_RING_PIN = board.D10
NUM_LEDS = 16
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(LED_RING_PIN, GPIO.IN)
pixels = neopixel.NeoPixel(LED_RING_PIN, NUM_LEDS, brightness=0.2)

pixels[0] = (255, 0, 0)
pixels[1] = (0, 255, 0)
pixels[2] = (0, 0, 255)

try:
    print("start")
    input()
except KeyboardInterrupt:
    GPIO.cleanup()



