import RPi.GPIO as GPIO
import dht11
import time
import datetime
from transmitter import Transmitter

# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

# read data using pin 17
instance = dht11.DHT11(pin=17)

if __name__ == '__main__':
        channel = "/dev/rfcomm8"
        TR = Transmitter(channel)
        TR
	while True:
	    result = instance.read()
	    #print("waiting")
	    if result.is_valid():
	        date = "Last valid input: " + str(datetime.datetime.now())

	        temp = "Temperature: %-3.1f C" % result.temperature
	        humid = "Humidity: %-3.1f %%" % result.humidity
		TR.sendData(temp+"\n")
		TR.sendData(humid+"\n")


