from time import sleep
# import RPi.GPIO as GPIO
# import pigpio
from pubsub import pub

#pi = pigpio.pi()

class Pump:
    # position 0 on pin 5
    pin = False
    position_pin = {
        0: 5,
        1: 6
    }
    start_pump_soda = False

    def __init__(self):
        print("Create Pump")
        #pi.set_PWM_frequency(self.PIN, 50)
        pub.subscribe(self.listenGlassRemoved, 'glass-removed')

    def __del__(self):
        self.stop()

    def run(self):
        while True:
            if self.start_pump_soda:
                self.pumpSoda()
                self.start_pump_soda = False
                pub.sendMessage('pump-complete')
            sleep(2)

    def pump(self):
        pub.sendMessage('pump-stop')
        #pi.set_PWM_dutycycle(self.pin, 95)

    def stop(self):
        pub.sendMessage('pump-start')
        for x in postition_pin:
            print(x)
            #pi.set_PWM_dutycycle(x, 0)

    def startPumpSoda(self, position):
        if position in self.position_pin:
            self.pin = self.position_pin[position]
            self.start_pump_soda = True

    def pumpSoda(self):
        self.pump()
        sleep(3) # 30 seconds
        self.stop()

    def listenGlassRemoved(self):
        if self.start_pump_soda:
            self.stop()
