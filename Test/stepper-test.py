from time import sleep
import RPi.GPIO as GPIO
import pigpio

DIR = 20     # Direction GPIO Pin
STEP = 21    # Step GPIO Pin
EN = 16      # Enable pin
CCW = 0      # Counterclockwise rotation
CW = 1       # Clockwise rotation
SENSOR1 = 26 # Sensor start
SENSOR2 = 19 # Sensor end

GPIO.setmode(GPIO.BCM)

def pressed(pin):
    if pin == 26:
        pi.write(DIR, CCW)
    elif pin == 19:
        pi.write(DIR, CW)

    print("OLA ", pin)

GPIO.setup(SENSOR1, GPIO.IN)
GPIO.add_event_detect(SENSOR1, GPIO.FALLING, callback=pressed, bouncetime=100)
GPIO.setup(SENSOR2, GPIO.IN)
GPIO.add_event_detect(SENSOR2, GPIO.FALLING, callback=pressed, bouncetime=100)

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(DIR, pigpio.OUTPUT)
pi.set_mode(STEP, pigpio.OUTPUT)
pi.set_mode(EN, pigpio.OUTPUT)
pi.write(EN, 1)

MODE = (14, 15, 18) # Microstep Resolution GPIO Pins
RESOLUTION = {'Full': (0, 0, 0),
              'Half': (1, 0, 0),
              '1/4': (0, 1, 0),
              '1/8': (1, 1, 0),
              '1/16': (0, 0, 1),
              '1/32': (1, 0, 1)}
for i in range(3):
    pi.write(MODE[i], RESOLUTION['Full'][i])

# Set duty cycle and frequency
pi.set_PWM_frequency(STEP, 500) # 500 pulses per second
pi.set_PWM_dutycycle(STEP, 128)  # PWM 1/2 On 1/2 Offs

def drive():
    pi.write(DIR, CCW) # Set default direction
    pi.write(EN, 0)
def stopDrive():
    pi.write(EN, 1)
    pi.set_PWM_dutycycle(STEP, 0)

try:
    print("start")
    drive()
    input()
except KeyboardInterrupt:
    print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
    stopDrive()
    GPIO.cleanup()
