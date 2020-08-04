import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from pytransform3d.plot_utils import Frame
from pytransform3d.rotations import *
import numpy as np
from scipy import integrate as it

from arrow_generator import Arrow3D

def read_data(file):
	'''
	Arg: txt file as str
	Function: Takes in file, returns list of data lists 
	File format: time is final string, makes n-sized
				 list of n-elements before 
	'''
	xs = []
	ys = []
	zs = []

	with open(file, 'r') as file:
		full_data = []
		for line in file:
			instance = []
			for element in line.split():
				instance.append(float(element))
			full_data.append(instance)
		return full_data

def integrate(data_T):
	'''
	Arg: transposed data - xs, ys, zs, ts are all in their
		 own lists; ts are always the last element
	Function: integrates to position and/or velocity for
			  both linear and angular data
	'''

	integratedData_1 = []
	integratedData_2 = []

	for dimension in data_T[0:3]:
		ts = data_T[3]
		initial = dimension[0]
		integratedData = it.cumtrapz(np.array(dimension), np.array(ts), initial=initial)
		integratedData_1.append(integratedData)

	for dimension in integratedData_1[0:3]:
		ts = data_T[3]
		initial = dimension[0]
		integratedData = it.cumtrapz(np.array(dimension), np.array(ts), initial=initial)
		integratedData_2.append(integratedData)

	return np.array(integratedData_1).T, np.array(integratedData_2).T

accel_data = read_data("data/acceleration.txt")
accel_data_transposed = np.array(accel_data).T
velocity_data, position_data = integrate(accel_data_transposed)

angvelData = read_data("data/attitude.txt")
angvelDataTransposed = np.array(angvelData).T
orientationData = np.array(integrate(angvelDataTransposed)[0]) # [0] index is to get the first result returned


# setup figure with 3 subplots
fig = plt.figure()
fig.tight_layout(pad=3.0)
ax1 = fig.add_subplot(131, projection='3d') # acceleration
ax2 = fig.add_subplot(132, projection='3d') # position
ax3 = fig.add_subplot(133, projection='3d') # orientation


def update(i, acceleration, position, orientation, frame):

	# ax1 = acceleration
	ax1.clear() # wipe previous arrows
	ax1.set_xlim3d([-10,10])
	ax1.set_ylim3d([-10,10])
	ax1.set_zlim3d([-10,10])
	ax1.set_xlabel('X (m/s2)')
	ax1.set_ylabel('Y (m/s2)')
	ax1.set_zlabel('Z (m/s2)')
	ax1.set_title("3D Acceleration")

	acc_x = acceleration[i][0]
	acc_y = acceleration[i][1]
	acc_z = acceleration[i][2]
	a = Arrow3D([0, acc_x], [0, acc_y], [0, acc_z], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
	ax1.add_artist(a)
	
	# ax2 = position
	ax2.clear() # wipe previous points
	ax2.set_xlim3d([-2000,2000])
	ax2.set_ylim3d([-2000,2000])
	ax2.set_zlim3d([-2000,2000])
	ax2.set_xlabel('X (m)')
	ax2.set_ylabel('Y (m)')
	ax2.set_zlabel('Z (m)')
	ax2.set_title("3D Position")

	pos_x = position[i][0]
	pos_y = position[i][1]
	pos_z = position[i][2]
	ax2.scatter(pos_x, pos_y, pos_z)


	# ax3 = orientation 
	ax3.set_xlim((-1, 1))
	ax3.set_ylim((-1, 1))
	ax3.set_zlim((-1, 1))
	ax3.set_xlabel("X")
	ax3.set_ylabel("Y")
	ax3.set_zlabel("Z")
	ax3.set_title("Orientation")

	roll = orientation[i][0]
	pitch = orientation[i][1]
	yaw = orientation[i][2]
	euler = [roll, pitch, yaw]
	R = matrix_from_euler_xyz(euler)
	A2B = np.eye(4)
	A2B[:3, :3] = R
	frame.set_data(A2B)
	return frame

def main():

	frame = Frame(np.eye(4), label="rotating frame", s=0.5)
	frame.add_frame(ax3)

	ani = FuncAnimation(
		fig, update, len(accel_data), interval=25, fargs=(accel_data, position_data, orientationData, frame), blit=False)
	plt.show()


if __name__ == '__main__':
	main()




# def update_attitude(i, data):
# 	ax2.clear()
# 	# must setup the plot again now
# 	axes2 = plt.gca()
# 	axes2.set_xlim3d([-5,5])
# 	axes2.set_ylim3d([-5,5])
# 	axes2.set_zlim3d([-5,5])
# 	ax2.set_xlabel('X roll (m)')
# 	ax2.set_ylabel('Y pitch (m)')
# 	ax2.set_zlabel('Z yaw (m)')
# 	plt.title("3D Acceleration")
# 	r = 5
# 	x = r*np.sin(np.pi/2 - data[i][1])*np.cos(data[i][0])
# 	y = r*np.sin(np.pi/2 - data[i][1])*np.sin(data[i][0])
# 	z = r*np.cos(np.pi/2 - data[i][1])

# 	# ax2.scatter(x, y, z)
# 	a = Arrow3D([0, x], [0, y], [0, z], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
# 	ax2.add_artist(a)