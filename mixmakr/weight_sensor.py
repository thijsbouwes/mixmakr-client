from time import sleep
from threading import Thread
#import Adafruit_GPIO.SPI as SPI
#import Adafruit_MCP3008
from pubsub import pub

class WeightSensor:
    SPI_PORT   = 0
    SPI_DEVICE = 0
    GLASS_PLACED_WEIGHT = 400
    NO_GLASS_PLACED_WEIGHT = 500
    glass_placed = False

    def __init__(self):
        #self.mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(self.SPI_PORT, self.SPI_DEVICE))
        print("create weightsensor")

    def run(self):
        while True:
            self.read()
            print("ADC " + str(self.read()))
            sleep(2)

    def read(self):
        value = 300 #self.mcp.read_adc(0)

        if value > self.NO_GLASS_PLACED_WEIGHT:
            pub.sendMessage('glass-removed')
        elif value < self.GLASS_PLACED_WEIGHT:
            pub.sendMessage('glass-placed')

        return value
