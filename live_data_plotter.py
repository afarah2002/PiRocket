import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

def read_data(file):
	'''
	Arg: txt file as str
	Function: Takes in file, returns list of data lists 
	File format: time is final string, makes n-sized
				 list of n-elements before 
	'''

	with open(file, 'r') as file:
		full_data = []
		for line in file:
			instance = []
			for element in line.split():
				instance.append(float(element))
			full_data.append(instance)
		return full_data

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
data = read_data("data/acceleration.txt")

def init():
	axes = plt.gca()
	axes.set_xlim([-10,10])
	axes.set_ylim([-10,10])
	axes.set_zlim([-10,10])
	ax.set_xlabel('X (m/s2)')
	ax.set_ylabel('Y (m/s2)')
	ax.set_zlabel('Z (m/s2)')
	plt.title("3D Acceleration")

	return ax

def animate(i):
	ax.scatter(data[i][0], data[i][1], data[i][2])

	return ax

def main():
	
	ani = FuncAnimation(fig, animate, frames=len(data), interval=50, init_func=init)
	plt.show()


if __name__ == '__main__':
	main()