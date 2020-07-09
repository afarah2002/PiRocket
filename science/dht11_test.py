import adafruit_dht
import time

dht_device = adafruit_dht.DHT11(24)

while True:

	try:
		temperature = dht_device.temperature
		humidity = dht_device.humidity
		print("Temp: ", temperature, "  Humid:", humidity)
		time.sleep(.1)
	except RuntimeError as error:
        	# Errors happen fairly often, DHT's are hard to read, just keep going
        	print(error.args[0])
