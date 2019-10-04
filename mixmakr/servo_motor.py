from time import sleep
# import pigpio
from pubsub import pub

#pi = pigpio.pi()

class ServoMotor:
    SERVO_PIN = 12
    start_dispens = False
    amount = 1

    def __init__(self):
        print("Create Servo")

    def __del__(self):
        self.stop()

    def run(self):
        while True:
            if self.start_dispens:
                for x in range(self.amount):
                    print(x)
                    self.dispens()
                self.start_dispens = False
                pub.sendMessage('dispens-complete')
            sleep(2)

    def startDispens(self, amount):
        if 0 < amount < 4:
            self.amount = amount

        self.start_dispens = True

    def up(self):
        pub.sendMessage('dispens-up')
        #pi.set_servo_pulsewidth(self.SERVO_PIN, 1300) # 120 degree

    def down(self):
        print('dispens-down')
        #pi.set_servo_pulsewidth(self.SERVO_PIN, 2500) # 0 degree

    def dispens(self):
        self.up()
        sleep(3)
        self.down()
        sleep(1.5)

    def stop(self):
        print('dispens-stop')
        #pi.set_servo_pulsewidth(self.SERVO_PIN, 0) # stop
