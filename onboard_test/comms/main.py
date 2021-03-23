#!/usr/bin/python
import time
from transmitter import Transmitter
import RPi.GPIO as GPIO
import dht11
import datetime


# initialize GPIO
GPIO.setwarnings(True)
GPIO.setmode(GPIO.BCM)

instance = dht11.DHT11(pin=17)

class Run(object):

        def __init__(self):
                channel = "/dev/rfcomm8"
                self.TR = Transmitter(channel)
                self.TR
        def main(self):
                while True:
			#self.TR.sendData("hello")
                        result = instance.read()
                        if result.is_valid():
	                        temp = "Temperature: %-3.1f C" % result.temperature
        	                humid = "Humidity: %-3.1f %%" % result.humidity
                	        self.TR.sendData("\n" + temp + '\n' + humid + "\n")

if __name__ == '__main__':
        Run = Run()
        Run.main()
