from mixmakr.stepper_motor import StepperMotor
from mixmakr.servo_motor import ServoMotor
from mixmakr.pump import Pump
from mixmakr.weight_sensor import WeightSensor
from mixmakr.led import Led
from time import sleep
from threading import Thread
from pubsub import pub

class MixMakr:
    currentDrink = {}
    currentIngredient = {}
    processing = False

    def __init__(self):
        print("Create MixMakr")
        self.stepper_motor = StepperMotor()
        self.servo_motor = ServoMotor()
        self.pump = Pump()
        self.weight_sensor = WeightSensor()
        self.led = Led()
        self.setup()

    def setup(self):
        led_thread = Thread(target = self.led.run, daemon = True)
        led_thread.start()

        weight_sensor_thread = Thread(target = self.weight_sensor.run, daemon = True)
        weight_sensor_thread.start()

        servo_motor_thread = Thread(target = self.servo_motor.run, daemon = True)
        servo_motor_thread.start()

        pump_thread = Thread(target = self.pump.run, daemon = True)
        pump_thread.start()

        pub.subscribe(self.lissentArrived, 'stepper-arrived')
        pub.subscribe(self.listenPumpComplete, 'pump-complete')
        pub.subscribe(self.listenDispensComplete, 'dispens-complete')


    def processDrink(self, drink):
        if (self.processing):
            return False

        self.processing = True
        self.currentDrink = drink
        self.prepareNextIngredient()

    def prepareNextIngredient(self):
        if not self.currentDrink["ingredients"]:
            pub.sendMessage('order-completed', status='completed')
            self.processing = False

        self.currentIngredient = self.currentDrink["ingredients"].pop()
        self.stepper_motor.setDestination(self.currentIngredient["position"])

        # if glass is all ready placed check route
        if self.weight_sensor.glass_placed:
            self.stepper_motor.check_route()

        print(self.currentDrink)
        print(self.currentIngredient)

    def isProcessing(self):
        return False
        return self.processing

    def listenPumpComplete(self):
        self.prepareNextIngredient()

    def listenDispensComplete(self):
        self.prepareNextIngredient()

    def lissentArrived(self):
        if self.currentIngredient["type"] == "liquor":
            self.servo_motor.startDispens()
        elif self.currentIngredient["type"] == "soda":
            self.pump.startPumpSoda()
