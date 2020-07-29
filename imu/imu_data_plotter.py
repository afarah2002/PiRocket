import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from arrow_generator import Arrow3D


##IMU imports##
import adafruit_lsm6ds
from adafruit_extended_bus import ExtendedI2C as I2C
##IMU SETUP##
i2c = I2C(3)
imu = adafruit_lsm6ds.LSM6DS33(i2c)


class PlotIMUData(object):

	def generate_data(i):
		accel_array =  imu.acceleration
		angvel_array = imu.gyro

		return accel_array, angvel_array

def main():
	fig = plt.figure()
	ax = p3.Axes3D(fig)

	ax.set_xlim3d([-50, 50])
	ax.set_xlabel('X')

	ax.set_ylim3d([-50, 50])
	ax.set_ylabel('Y')

	ax.set_zlim3d([-50, 50])
	ax.set_zlabel('Z')

	ax.view_init(25, 10)

	while True:
		a, g = PlotIMUData.generate_data()
		arrow = Arrow3D([0, a[0]], [0, a[1]], [0, a[2]])
		ax.add_artist(arrow)
		plt.draw()
		plt.show()
		time.sleep(1)
