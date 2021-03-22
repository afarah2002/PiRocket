import adafruit_dht
import time

sensorPin = 21
dht_device = adafruit_dht.DHT11(sensorPin)

while True:

	try:
		temperature = dht_device.temperature
		humidity = dht_device.humidity
		print("Temp: ", temperature, "  Humid:", humidity)
		time.sleep(.1)
	except RuntimeError as error:
        	# Errors happen fairly often, DHT's are hard to read, just keep going
        	print(error.args[0])
