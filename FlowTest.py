from __future__ import division         # importeer de GPIO bibliotheek.
import RPi.GPIO as GPIO                 # Importeer de time biblotheek voor tijdfuncties.
import time
import sys

PULSTIME = 2.0                          # dit is de aan/uit tijd van de motor
MOTORPIN_1 = 2                          # dit is de aangesloten pin voor de motor

# Stel de GPIO in
GPIO.setmode(GPIO.BCM)					# use the Broadcom method for naming the GPIO pins
GPIO.setup(MOTORPIN_1, GPIO.OUT)        # set de pin en maak het een output
GPIO.setwarnings(False)					# set de warnings to false


#Make a for loop
#for i in range(0, 5):
while True:
        print "Motor aan"
        GPIO.output(MOTORPIN_1, True)
        time.sleep(PULSTIME)

        print "Motor uit"
        GPIO.output(MOTORPIN_1,False)
        time.sleep(PULSTIME)

        print " "

#nette opruiming van het programma
GPIO.cleanup()
