from time import sleep
# import RPi.GPIO as GPIO
# import pigpio
from pubsub import pub

#pi = pigpio.pi()

class Pump:
    PIN = 5
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
        #pi.set_PWM_dutycycle(self.PIN, 95)

    def stop(self):
        pub.sendMessage('pump-start')
        #pi.set_PWM_dutycycle(self.PIN, 0)

    def startPumpSoda(self):
        self.start_pump_soda = True

    def pumpSoda(self):
        self.pump()
        sleep(3) # 30 seconds
        self.stop()

    def listenGlassRemoved(self):
        if self.start_pump_soda:
            self.stop()
