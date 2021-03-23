import numpy as np
import time
import adafruit_dht

global dht_device 
dhtPin = 21
dht_device = adafruit_dht.DHT11(dhtPin)

class ReadDHT11(object):

	def read(self):
		try:
			temperature = dht_device.temperature
			humidity = dht_device.humidity
		except RuntimeError as error:
        		# Errors happen fairly often, DHT's are hard to read, just keep going
			temperature = None
			humidity = None
			print(error.args[0])

		#print(temperature, humidity)

		return temperature, humidity

#if __name__ == '__main__':
#	while True:
#		ReadDHT11().read()

