#----------imports----------#
# from imu_ad import IMUAttitudeDetermination 
import imu_ad
import RPi.GPIO
import smbus
import math
import numpy as np
import time

# import scipy.integrate as si
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import operator as op

# from mpl_toolkits.mplot3d import Axes3D

# #Libraries for GUI
# import Tkinter as Tk



#----------code starts here!----------#
fig = plt.figure()
ax1 = fig.add_subplot(1,1,1)
xs = []	
ys = []

class PlotMotion():



	def __init__(self):

		allAngles = [[0,0,0]]

		#Calling functions from imu_ad
		imu = imu_ad.IMUAttitudeDetermination(0x6b)
		imu.readLinearAccelerators()
		deltaAngles = [i*0.45 for i in imu.readGyros()]
		newAngles = list(map(op.add, allAngles[-1],deltaAngles))
		allAngles.append(newAngles)
		print("RX: ", allAngles[-1][0], " dps ", "\n", "RY: ", allAngles[-1][1], " dps ", "\n", "RZ: ", allAngles[-1][2], " dps ", "\n")
		time.sleep(.43)
		self.info_list = imu.convertUnits()
		# print(self.info_list)
	# def animate(self, index):
	# 	self.value = self.info_list[index]
	# 	ys.append(self.value)
	# 	for i in ys:
	# 		xs = list(range(len(ys)))
	# 	ax1.clear()
	# 	ax1.plot(xs,ys)

	# 	return self.value

		

						
def main():
	global fig, ax1, xs, ys
	vals = []
	while True:
		start_time = time.time()
		plot = PlotMotion()
		plot

		# vals.append(plot.val())
		# lx = plot.animate(0)
		# ani = animation.FuncAnimation(fig, plot.animate(0), interval=1000)
		# plt.show()
		# # plt.plot(lx[0], lx[1])
		# # ly = plot.attVal(1) 
		# # lz = plot.attVal(2) 
		# # rx = plot.attVal(3) 
		# # ry = plot.attVal(4) 
		# # rz = plot.attVal(5)
		# # plt.show()
		# # plt.close()

		


if __name__ == '__main__':
	main()

