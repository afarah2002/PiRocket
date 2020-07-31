import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

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

fig = plt.figure()
ax = Axes3D(fig)
data = read_data("data/acceleration.txt")
data_transposed = np.array(data).T
line, = ax.plot(data_transposed[0, 0:1], data_transposed[1, 0:1], data_transposed[2, 0:1])

def update(i, data, line):
	# use for position 
	# print(data[:2, :i])
	# print("")
	# line.set_data(data[:2, :i])
	# line.set_3d_properties(data[2, :i]) 
	ax.clear()
	# must setup the plot again now
	axes = plt.gca()
	axes.set_xlim3d([-10,10])
	axes.set_ylim3d([-10,10])
	axes.set_zlim3d([-10,10])
	ax.set_xlabel('X (m/s2)')
	ax.set_ylabel('Y (m/s2)')
	ax.set_zlabel('Z (m/s2)')
	plt.title("3D Acceleration")
	a = Arrow3D([0, data[i][0]], [0, data[i][1]], [0, data[i][2]], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
	ax.add_artist(a)

	return line

def main():
	
	# ani = FuncAnimation(fig, update, len(data_transposed[0]), interval=10000/69, init_func=init, fargs=(data_transposed, line))
	ani = FuncAnimation(fig, update, len(data), interval=50, fargs=(data, line))
	plt.show()


if __name__ == '__main__':
	main()