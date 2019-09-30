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
        self.stepper_motor = StepperMotor()
        self.servo_motor = ServoMotor()
        self.pump = Pump()
        self.weight_sensor = WeightSensor()
        self.led = Led()

        print("create MixMakr")
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

        pub.subscribe(self.lissentArrived, 'arrived')
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
            print("All ingredients are done and drink is complete")
            self.processing = False

        self.currentIngredient = self.currentDrink["ingredients"].pop()
        self.stepper_motor.setDestination(self.currentIngredient["position"])

        print(self.currentDrink)
        print(self.currentIngredient)

    def isProcessing(self):
        return self.processing

    def listenPumpComplete(self):
        print("pump compolete")
        self.prepareNextIngredient()

    def listenDispensComplete(self):
        print("dispens complete")
        self.prepareNextIngredient()

    def lissentArrived(self):
        if self.currentIngredient["type"] == "liquor":
            self.servo_motor.startDispens()
        elif self.currentIngredient["type"] == "soda":
            self.pump.startPumpSoda()
