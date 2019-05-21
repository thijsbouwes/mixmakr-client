
#!/usr/bin/env python
#Dit is alleen een stukje testcode om een SG90 servo te laten draaien

from __future__ import division         # importeer de GPIO bibliotheek.
import RPi.GPIO as GPIO                 # Importeer de time biblotheek voor tijdfuncties.
import time
import sys
#import constant

OFFSET = 30.0                           # Dit is een offset waarde voor de SG90 servo

# Zet de pinmode op Broadcom SOC.
GPIO.setmode(GPIO.BCM)

# Zet waarschuwingen uit.
#GPIO.setwarnings(False)

GPIO.setup(4, GPIO.OUT)                 # Zet de GPIO pin als uitgang.
servopin = GPIO.PWM(4, 50)              # Configureer de pin voor PWM met een frequentie van 50Hz.
servopin.start(0)                       # Start PWM op de GPIO pin met een duty-cycle van 6%

if len(sys.argv) > 1:
  waarde = int(sys.argv[1])

# Een MAP functie om eenvoudig verhoudingen tussen getallen te creeren.
def arduino_map(x, in_min, in_max, out_min, out_max):
  return (x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min

# Gebruik de MAP functie om eenvoudig verhoudingen tussen getallen te creeren.
# De waarden met 10 vermenigvuldigen voor betere precisie.
pwmwaarde = arduino_map(waarde, 0, 180, (2.5 * 10), (11.5 * 10))

# Print de gegevens naar de console.
print "Hoek:", waarde, "| PWM:", pwmwaarde / 10

pwmwaarde += OFFSET
servopin.ChangeDutyCycle(pwmwaarde / 10)
time.sleep(.5)

#nette opruiming van het programma
servopin.stop()
GPIO.cleanup()
