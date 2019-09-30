from time import sleep
# import RPi.GPIO as GPIO
from mixmakr.mix_makr import MixMakr
from mixmakr.order_manager import OrderManager

enable_pin = 16

def run():
    print("Starting app")
    setup()
    loop()

def setup():
    print("Setup")
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(enable_pin, GPIO.OUT)

def loop():
    mix_makr = MixMakr()
    order_manager = OrderManager()

    try:
        print("Start making order")

        while True:
            order = order_manager.getLatestOrder()

            if (mix_makr.isProcessing() == False):
                mix_makr.processDrink(order["drink"])

            sleep(1)

        print("Done making orders")
    except KeyboardInterrupt:
        #GPIO.output(enable_pin, True)
        print ("\nCtrl-C pressed.")
