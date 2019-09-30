from time import sleep
# import RPi.GPIO as GPIO
# import pigpio
from pubsub import pub

#pi = pigpio.pi()

class Pump:
    PIN = 5
    start_pump_soda = False

    def __init__(self):
        #pi.set_PWM_frequency(self.PIN, 50)
        print("create pump")
        pub.subscribe(self.listenGlassRemoved, 'glass-removed')

    def __del__(self):
        self.stop()

    def run(self):
        while True:
            if self.start_pump_soda:
                print("start soda")
                self.pumpSoda()
                self.start_pump_soda = False
                pub.sendMessage('pump-complete')
            sleep(2)

    def pump(self):
        #pi.set_PWM_dutycycle(self.PIN, 95)
        print("pump")

    def stop(self):
        #pi.set_PWM_dutycycle(self.PIN, 0)
        print("stop pump")

    def startPumpSoda(self):
        self.start_pump_soda = True

    def pumpSoda(self):
        self.pump()
        sleep(30)
        self.stop()

    def listenGlassRemoved(self):
        if self.start_pump_soda:
            self.stop()
