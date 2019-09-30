from time import sleep
# import pigpio
from pubsub import pub

#pi = pigpio.pi()

class ServoMotor:
    SERVO_PIN = 12
    start_dispens = False

    def __init__(self):
        print("create servo")
        pub.subscribe(self.listenGlassRemoved, 'glass-removed')

    def __del__(self):
        self.stop()

    def run(self):
        while True:
            if self.start_dispens:
                print("start soda")
                self.dispens()
                self.start_dispens = False
                pub.sendMessage('dispens-complete')
            sleep(2)

    def startDispens(self):
        self.start_dispens = True

    def up(self):
        print("up")
        #pi.set_servo_pulsewidth(self.SERVO_PIN, 1300) # 120 degree

    def down(self):
        print("down")
        #pi.set_servo_pulsewidth(self.SERVO_PIN, 2500) # 0 degree

    def dispens(self):
        self.up()
        sleep(3)
        self.down()
        sleep(1.5)

    def stop(self):
        print("stop servo")
        #pi.set_servo_pulsewidth(self.SERVO_PIN, 0) # stop

    def listenGlassRemoved(self):
        if self.start_pump_soda:
            self.stop()
