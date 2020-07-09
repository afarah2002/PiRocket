import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from imu_ad import IMUAttitudeDetermination


def generate_data(i, address):
	i += 1
	imu = IMUAttitudeDetermination(address)#<------ place the address you find here!!!!!!!
	pos = imu.readLinearAccelerators()
	ori = imu.readGyros()	

	print(i)

	return i, pos, ori

def animate(i, pos, ori):

	# 3d plot init
	fig = plt.figure()
	ax = p3.Axes3D(fig)

	iterations = len(data)

	# Setting the axes properties
	ax.set_xlim3d([-50, 50])
	ax.set_xlabel('X')

	ax.set_ylim3d([-50, 50])
	ax.set_ylabel('Y')

	ax.set_zlim3d([-50, 50])
	ax.set_zlabel('Z')

	ax.set_title('3D Animated Scatter Example')

	# Provide starting angle for the view.
	ax.view_init(25, 10)



def main():
	# initial iteration
	i = 0
	generate(i, 0x6A)




	
