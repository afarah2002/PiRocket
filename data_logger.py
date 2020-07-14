import numpy as np
import math
import time
import scipy
import datetime
##IMU imports##
import adafruit_lsm6ds
from adafruit_extended_bus import ExtendedI2C as I2C
#DHT imports
import adafruit_dht

global dht_device 
dht_device = adafruit_dht.DHT11(25)
class DataCollector():

	def collect(i2c_bus):
		# collect imu data
		try:
			i2c = I2C(3)
			imu = adafruit_lsm6ds.LSM6DS33(i2c)
			accel_array =  imu.acceleration
			angvel_array = imu.gyro
		except RuntimeError as error:
			accel_array = (None, None, None)
			angvel_array = (None, None, None)
		# collect dht data
		
		try:
			temperature = dht_device.temperature
			humidity = dht_device.humidity
		except RuntimeError as error:
        		# Errors happen fairly often, DHT's are hard to read, just keep going
			temperature = None
			humidity = None
			print(error.args[0])
		t1 = time.time()

		return accel_array, angvel_array, temperature, humidity, t1

	def save(accel, angvel, temp, humid, t0, t1):
		try:
			print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(accel))
			print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s"%(angvel))
		except TypeError as error:
			print("Check IMU wiring!!!")
		print("Temp: ", temp, "  Humid:", humid)
		elapsed_time = t1 - t0
		print("Elapsed time:", elapsed_time)
		print("")		 

class DataProcessor:

	def getRawData(self):
		i2c = I2C(3)
		imu = adafruit_lsm6ds.LSM6DS33(i2c)
		accel_array =  np.array(imu.acceleration)
		angvel_array = np.array(imu.gyro)
		
		print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(imu.acceleration))
		#print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s"%(imu.gyro))
		return accel_array, angvel_array

	def calcAttitude(self, acc, pos0, vel0, dt):
		# adjust acceleration for gravity (z-axis)
		acc_adj = np.add(acc, [0,0,9.8])
		# calculate velocity
		velocity = np.add(np.multiply(acc_adj, dt), vel0)
		position = np.add(np.multiply(velocity, dt), pos0)
		
		return position, velocity
	
	def calcOrientation(self, ang_vel0, ori0, dt):
		orientation = np.add(np.multiply(ang_vel0, dt), ori0)
		return orientation

#def main():
	# setting initial states, integration constants
	#pos0, vel0, ori0 = [0,0,0], [0,0,0], [0,0,0]
	
	#while True: 
		#dt = 0.1
		#DP = DataProcessor()
		#acc, ang_vel = DP.getRawData()
		#pos, vel = DP.calcAttitude(acc, pos0, vel0, dt)
		#ori = DP.calcOrientation(ang_vel, ori0, dt)
		# update initial states 
		#pos0, vel0 = pos, vel
		#ori0 = ori
		#time.sleep(dt)
		#print("Position: X:%.2f, Y: %.2f, Z: %.2f m"%(tuple(pos0)))
		#print("")
		
def main(t0):
	while True:
		accel, angvel, temp, humid, t1 = DataCollector.collect(3)
		DataCollector.save(accel, angvel, temp, humid, t0, t1)
		

if __name__ == '__main__':
	t0 = time.time()
	main(t0)
