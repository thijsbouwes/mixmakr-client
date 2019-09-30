from time import sleep
import pigpio

SERVO_PIN = 12

# Connect to pigpiod daemon
pi = pigpio.pi()

# Set up pins as an output
pi.set_mode(SERVO_PIN, pigpio.OUTPUT)

# Set duty cycle and frequency
def up():
    pi.set_servo_pulsewidth(SERVO_PIN, 1550) # Set default direction
def down():
    pi.set_servo_pulsewidth(SERVO_PIN, 500) # Set default direction

try: 
    while True:
        print("start")
        up()
        sleep(2)
        print("down")
        down()
        sleep(2)
except KeyboardInterrupt:
    print ("\nCtrl-C pressed.  Stopping PIGPIO and exiting...")
    pi.set_servo_pulsewidth(SERVO_PIN, 0)
    #stopDrive()
