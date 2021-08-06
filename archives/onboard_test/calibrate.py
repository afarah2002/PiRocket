import numpy as np
from data_logger import DataCollector as DC

def main():
	while True:
		accel_array, angvel_array, temperature, humidity, t1 = DC.collect(3)
		if type(accel_array) == tuple:
			print(accel_array)

if __name__ == '__main__':
	main()
