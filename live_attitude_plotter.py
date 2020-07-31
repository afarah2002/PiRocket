import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from pytransform3d.plot_utils import Frame
from pytransform3d.rotations import *
from scipy import integrate as it

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

	return integratedData_1

angvelData = read_data("data/attitude.txt")
angvelDataTransposed = np.array(angvelData).T
orientationData = np.array(integrate(angvelDataTransposed)).T
# print(len(orientationData))

# ax = plot_basis(R=np.eye(3), ax_s=2)
# # axis = 0
# # angle = np.pi / 2

# # p = np.array([1.0, 1.0, 1.0])
# # euler = [0, 0, 0]
# # euler[axis] = angle
# # R = matrix_from_euler_xyz(euler)

def update_frame(i, data, frame):
    # angle = 2.0 * np.pi * (step + 1) / n_frames
    roll = data[i][0]
    pitch = data[i][1]
    yaw = data[i][2]
    euler = [roll, pitch, yaw]
    R = matrix_from_euler_xyz(euler)
    A2B = np.eye(4)
    A2B[:3, :3] = R
    frame.set_data(A2B)
    return frame


if __name__ == "__main__":
    n_frames = 50

    fig = plt.figure(figsize=(5, 5))

    ax = fig.add_subplot(111, projection="3d")
    ax.set_xlim((-1, 1))
    ax.set_ylim((-1, 1))
    ax.set_zlim((-1, 1))
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    frame = Frame(np.eye(4), label="rotating frame", s=0.5)
    frame.add_frame(ax)

    anim = FuncAnimation(
        fig, update_frame, len(orientationData), fargs=(orientationData, frame), interval=100,
        blit=False)

    plt.show()
