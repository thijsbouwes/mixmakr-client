from time import sleep
# import RPi.GPIO as GPIO
# import pigpio
from pubsub import pub
#pi = pigpio.pi()

class StepperMotor:
    current_position = 0
    current_rotation = 1
    destination = -1
    glass_placed = False

    DIRECTION_PIN = 20
    STEP_PIN = 21
    ENABLE_PIN = 16
    MODE = (14, 15, 4) # microstep resolution pins
    RESOLUTION = {
        'Full': (0, 0, 0),
        'Half': (1, 0, 0),
        '1/4': (0, 1, 0),
        '1/8': (1, 1, 0),
        '1/16': (0, 0, 1),
        '1/32': (1, 0, 1)
    }
    CCW = 0 # Counterclockwise rotation
    CW = 1 # Clockwise rotation
    SENSOR_PINS = [17, 27, 22, 23, 24, 25]

    def __init__(self):
        #GPIO.setmode(GPIO.BCM)
        print("create stepper motor")
        pub.subscribe(self.listenGlassPlaced, 'glass-placed')
        pub.subscribe(self.listenGlassRemoved, 'glass-removed')
        self.setup()

    def __del__(self):
        self.stop()

    def setup(self):
        print("ola")
        # Set up pins as an output
        #pi.set_mode(self.DIRECTION_PIN, pigpio.OUTPUT)
        #pi.set_mode(self.STEP_PIN, pigpio.OUTPUT)
        #pi.set_mode(self.ENABLE_PIN, pigpio.OUTPUT)
        #pi.write(self.ENABLE_PIN, 1)
#        self.setupSensor()

        # Set mode
#        for i in range(3):
#            pi.write(self.MODE[i], self.RESOLUTION['Half'][i])

        # Set duty cycle and frequency
#       pi.set_PWM_frequency(self.STEP_PIN, 500) # 500 pulses per second

  #  def setupSensor(self):
  #      for pin in self.SENSOR_PINS:
  #          GPIO.setup(pin, GPIO.IN)
  #          GPIO.add_event_detect(pin, GPIO.FALLING, callback=self.activeSensor, bouncetime=100)
  #          if (GPIO.input(pin)):
  #             print("Allready  on position " + pin)
  #             self.current_position = pin

    def activeSensor(self, pin):
        self.current_position = self.SENSOR_PINS.index(pin)
        self.check_route()
        print("sensor" + str(self.current_position))

    def drive(self):
        print("drive")

        # pi.set_PWM_dutycycle(self.STEP_PIN, 200)
        # pi.write(self.DIRECTION_PIN, self.current_rotation) # Set default direction
        # pi.write(self.ENABLE_PIN, 0)

    def check_route(self):
        if self.current_position > self.destination:
            self.current_rotation = self.CW
            self.drive()
        elif self.current_position < self.destination:
            self.current_rotation = self.CCW
            self.drive()
        elif self.arrived():
            print("ola - arrived")
            self.stop()
            pub.sendMessage('arrived')

    def setDestination(self, destination):
        self.destination = destination

    def arrived(self):
        return self.current_position == self.destination

    def stop(self):
        print("stop stepper")
        # pi.write(self.ENABLE_PIN, 1)
        # pi.set_PWM_dutycycle(self.STEP_PIN, 0)

    def listenGlassPlaced(self):
        if self.glass_placed == False and self.destination == False:
            self.glass_placed = True
            self.check_route()

    def listenGlassRemoved(self):
        if self.glass_placed:
            self.glass_placed = False
            self.stop()
