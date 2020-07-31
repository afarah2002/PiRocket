import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
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
		print(integratedData)

	# for dimension in integratedData_1:
	# 	ts = data_T[3]
	# 	initial = dimension[0]

	return integratedData_1

accel_data = read_data("data/acceleration.txt")
accel_data_transposed = np.array(accel_data).T

angvel_data = read_data("data/attitude.txt")
angvel_data_transposed = np.array(angvel_data).T
orientation = np.array(integrate(angvel_data_transposed)).T
print(len(orientation))

# fig1 = plt.figure()
# ax1 = Axes3D(fig1)
def update_acceleration(i, data):
	# use for position 
	# print(data[:2, :i])
	# print("")
	# line.set_data(data[:2, :i])
	# line.set_3d_properties(data[2, :i]) 
	ax1.clear()
	# must setup the plot again now
	axes1 = plt.gca()
	axes1.set_xlim3d([-10,10])
	axes1.set_ylim3d([-10,10])
	axes1.set_zlim3d([-10,10])
	ax1.set_xlabel('X (m/s2)')
	ax1.set_ylabel('Y (m/s2)')
	ax1.set_zlabel('Z (m/s2)')
	plt.title("3D Acceleration")
	a = Arrow3D([0, data[i][0]], [0, data[i][1]], [0, data[i][2]], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
	ax1.add_artist(a)

fig2 = plt.figure()
ax2 = Axes3D(fig2)
def update_attitude(i, data):
	ax2.clear()
	# must setup the plot again now
	axes2 = plt.gca()
	axes2.set_xlim3d([-5,5])
	axes2.set_ylim3d([-5,5])
	axes2.set_zlim3d([-5,5])
	ax2.set_xlabel('X roll (m)')
	ax2.set_ylabel('Y pitch (m)')
	ax2.set_zlabel('Z yaw (m)')
	plt.title("3D Acceleration")
	r = 5
	x = r*np.sin(np.pi/2 - data[i][1])*np.cos(data[i][0])
	y = r*np.sin(np.pi/2 - data[i][1])*np.sin(data[i][0])
	z = r*np.cos(np.pi/2 - data[i][1])

	# ax2.scatter(x, y, z)
	a = Arrow3D([0, x], [0, y], [0, z], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
	ax2.add_artist(a)

def main():
	
	# ani = FuncAnimation(fig1, update_acceleration, len(accel_data), interval=10, fargs=([accel_data]))
	ani2 = FuncAnimation(fig2, update_attitude, len(orientation), interval=100, fargs=([orientation]))
	plt.show()


if __name__ == '__main__':
	main()