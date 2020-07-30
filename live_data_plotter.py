import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

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


def main():
	accel_data = read_data("data/acceleration.txt")
	print(accel_data)



if __name__ == '__main__':
	main()