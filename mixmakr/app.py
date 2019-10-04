from time import sleep
# import RPi.GPIO as GPIO
from pubsub import pub
from dotenv import load_dotenv
from mixmakr.mix_makr import MixMakr
from mixmakr.order_manager import OrderManager
from threading import Thread
import os

class App:
    enable_pin = 16

    def run(self):
        self.setup()
        self.loop()

    def setup(self):
        print("Create App")
        load_dotenv()

        pub.subscribe(self.notify, pub.ALL_TOPICS)

        self.order_manager = OrderManager()
        self.mix_makr = MixMakr()

        order_manager_thread = Thread(target = self.order_manager.run, daemon = True)
        order_manager_thread.start()

        # GPIO.setmode(GPIO.BCM)
        # GPIO.setup(self.enable_pin, GPIO.OUT)

    def loop(self):
        order = {}

        try:
            while True:
                if (self.mix_makr.isProcessing() == False) and bool(order):
                    pub.sendMessage('order-creating', status='creating')
                    self.mix_makr.processDrink(order["drink"])
                    order = {}
                elif self.mix_makr.isProcessing() == False:
                    order = self.getNewOrder()

                if (self.order_manager.cancel):
                    print(self.order_manager.cancel)
                    self.mix_makr.stop()
                    self.order_manager.cancel = False

                sleep(0.1)

            print("Done making orders")
        except KeyboardInterrupt:
            #GPIO.output(enable_pin, True)
            print ("\nCtrl-C pressed.")

    def notify(self, topicObj=pub.AUTO_TOPIC, **msgData):
        status = False

        if bool(msgData) and msgData['status']:
            status = msgData['status']

        self.order_manager.queueUpdateOrder(topicObj.getName(), status)
        print('topic "%s": %s' % (topicObj.getName(), msgData))

    def getNewOrder(self):
        return self.order_manager.getLatestOrder()
