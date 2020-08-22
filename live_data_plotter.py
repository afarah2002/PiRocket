import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import pyglet
from pyglet.gl import *
from pytransform3d.plot_utils import Frame
from pytransform3d.rotations import *
import ray
from scipy import integrate as it
from threading import Thread
import multiprocessing
import time

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

def calibrate(data_T): # WILL WORK PREMATURELY ONLY WITH ANGVEL
	'''
	Arg: transposed data
	Func: takes each dimension and subtracts the value of the 
		  first element from every recorded value on [1:]
	'''
	calibratedData = []
	ts = data_T[3]
	for dimension in data_T[0:3]:
		calibDim = dimension - np.mean(dimension[0:15])
		calibratedData.append(calibDim)
	calibratedData.append(ts)

	return calibratedData

# most recent test
acc_file_new = "data/acceleration.txt"
angvel_file_new = "data/attitude.txt"

# test 8
test_num = 8
acc_file_old = "old_data/test" + str(test_num) + "/acceleration.txt"
angvel_file_old = "old_data/test" + str(test_num) + "/attitude.txt"


accel_data = read_data(acc_file_new)
print("Number of points:", len(accel_data))
accelDataTransposed = np.multiply(accel_data, np.array([-1,-1,-1,1])).T
# print(np.array(accel_data).T)
accelCalibrated = calibrate(accel_data)
velocityDataTransposed, positionDataTransposed = integrate(accelDataTransposed) 

angvelData = read_data(angvel_file_new)
angvelDataTransposed = np.array(np.multiply(angvelData, np.array([1,1,-1,1]))).T
angvelCalibrated = calibrate(angvelDataTransposed)
orientationData = np.array(integrate(angvelCalibrated)[0]) # [0] index is to get the first result returned

	
fig = plt.figure("Flight Data")
fig.tight_layout()
ax1 = fig.add_subplot(231, projection='3d') # acceleration
ax2 = fig.add_subplot(232, projection='3d') # position
ax3 = fig.add_subplot(233, projection='3d') # orientation

ax4 = fig.add_subplot(223) # acceleration, noise
ax5 = fig.add_subplot(224) # angular velocity, noise


# l, v = ax4.plot(0, -11, accel_data[-1][-1]+1, 11, linewidth=2, color= 'black')
l4 = ax4.axvline(x=0., color='k')
l5 = ax5.axvline(x=0., color='k')


def update(i, acceleration, position, orientation, frame, line4, line5):

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
	# ax1 = acceleration
	ax1.clear() # wipe previous arrows
	ax1.set_xlim3d([-5,5])
	ax1.set_ylim3d([-5,5])
	ax1.set_zlim3d([-5,5])
	ax1.set_xlabel('X (m/s2)')
	ax1.set_ylabel('Y (m/s2)')
	ax1.set_zlabel('Z (m/s2)')
	ax1.set_title("3D Acceleration")

	# acc_array = np.multiply(np.array(acceleration[i][0:3]), np.array([1,1,1]))
	acc_array = acceleration[i][0:3]

	acc_prime = np.dot(acc_array, R)
	# print(np.array(acceleration[i][0:3]))
	print("Original: ", np.round(acc_array, 3), "		", "Primed", np.round(acc_prime, 3))

	acc_x = acc_prime[0]
	acc_y = acc_prime[1]
	acc_z = acc_prime[2]

	a = Arrow3D([0, acc_x], [0, acc_y], [0, acc_z], mutation_scale=20, lw=1, arrowstyle="-|>", color="r")
	ax1.add_artist(a)
	
	# ax2 = position
	ax2.clear() # wipe previous points
	ax2.set_xlim3d([-50,50])
	ax2.set_ylim3d([-50,50])
	ax2.set_zlim3d([-2000,2000])
	ax2.set_xlabel('X (m)')
	ax2.set_ylabel('Y (m)')
	ax2.set_zlabel('Z (m)')
	ax2.set_title("3D Position")

	pos_prime = np.dot(np.array(position[i][0:3]), R)

	pos_x = pos_prime[0]
	pos_y = pos_prime[1]
	pos_z = pos_prime[2]
	ax2.scatter(pos_x, pos_y, pos_z)

	t = acceleration[i][3]

	line4.set_data([t,t], [-11,11])
	line5.set_data([t,t], [-11,11])

	return frame, line4, line5,


def noise(acc, ang_vel):
	# must take transposed data
	# fig, (ax1, ax2) = plt.subplots(2)
	# fig.suptitle('Noise analysis')
	# each plot plots all three axes
	# ax4.clear()
	ax4.set_title('3-Axis Accelerometer')
	ax4.plot(acc[3],acc[0],color='red')
	ax4.plot(acc[3],acc[1],color='green')
	ax4.plot(acc[3],acc[2],color='blue')
	ax4.set_xlim([0,accel_data[-1][-1]+1])
	ax4.set_ylim([-11,11])
	ax4.set_xlabel('Time (s)')
	ax4.set_ylabel('Acceleration (m/s2)')

	ax5.set_title('3-Axis Gyros')
	ax5.plot(ang_vel[3],ang_vel[0],color='red')
	ax5.plot(ang_vel[3],ang_vel[1],color='green')
	ax5.plot(ang_vel[3],ang_vel[2],color='blue')
	ax5.set_xlabel('Time (s)')
	ax5.set_ylabel('Angular velocity (rad/s)')

	# plt.show()


# ray.init()

# @ray.remote
def flight_plotter():

	# print(accelCalibrated)

	noise(accelDataTransposed, angvelCalibrated)

	frame = Frame(np.eye(4), label="rotating frame", s=0.5)
	frame.add_frame(ax3)

	ani = FuncAnimation(
		fig, update, len(accel_data), interval=150, fargs=(accel_data, positionDataTransposed, orientationData, frame, l4, l5), blit=False)
	plt.show()

if __name__ == '__main__':
	flight_plotter()

'''
window = pyglet.window.Window(width=1440, height=960)
window.projection = pyglet.window.Projection3D()
batch = pyglet.graphics.Batch()

@window.event
def on_draw():
	window.clear()
	batch.draw()


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
	glRotatef(1, dx, dy, 0)

def rotate_model(dt, dx, dy, dz):
	# rotate around x
	glRotatef(dx, 1, 0, 0)
	# rotate around y
	glRotatef(dy, 0, 1, 0)
	# rotate around z
	glRotatef(dz, 0, 0, 1)


glEnable(GL_MULTISAMPLE_ARB)
glEnable(GL_DEPTH_TEST)
glEnable(GL_LIGHTING)
glEnable(GL_LIGHT0)

model = pyglet.model.load("rocket.obj", batch=batch)
glTranslatef(0, 0, -3)
# print(len(orientationData))
# @ray.remote
def run():
	for i in orientationData:
		dx = i[0]
		dy = i[1]
		dz = i[2]
		# rotate_model(0, dx, dy, dz)
		print(i)
		pyglet.clock.schedule_interval(rotate_model, 1/120, dx, dy, dz)
		
		pyglet.app.run()

'''
# if __name__ == '__main__':
# 	flight_plotter()
	# run()
	# modeller()
	# p1 = multiprocessing.Process(target=flight_plotter)
	# p2 = multiprocessing.Process(target=run)

	# p1.start()
	# p2.start()
	# Thread(target = flight_plotter).start()
	# Thread(target = modeller).start()

	# p1.join()
	# p2.join()
	# flight_plotter()

	# modeller()
	# ray.get([flight_plotter.remote(), run.remote()])



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