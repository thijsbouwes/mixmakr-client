from time import sleep
# import RPi.GPIO as GPIO
from pubsub import pub
from dotenv import load_dotenv
from mixmakr.mix_makr import MixMakr
from mixmakr.order_manager import OrderManager
import os

enable_pin = 16
order_manager = OrderManager()

def run():
    setup()
    loop()

def setup():
    print("Create App")
    load_dotenv()
    pub.subscribe(snoop, pub.ALL_TOPICS)
    order_manager.setup()

    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(enable_pin, GPIO.OUT)

def loop():
    mix_makr = MixMakr()

    try:
        while True:
            order = order_manager.getLatestOrder()
            print(order)

            if (mix_makr.isProcessing() == False) and bool(order):
                pub.sendMessage('order-creating', status='creating')
                mix_makr.processDrink(order["drink"])

            print("loop..")
            sleep(1)

        print("Done making orders")
    except KeyboardInterrupt:
        #GPIO.output(enable_pin, True)
        print ("\nCtrl-C pressed.")

def snoop(topicObj=pub.AUTO_TOPIC, **msgData):
    status = False

    if bool(msgData) and msgData['status']:
        status = msgData['status']

    order_manager.updateOrder(topicObj.getName(), status)

    print('topic "%s": %s' % (topicObj.getName(), msgData))
