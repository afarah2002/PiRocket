import matplotlib.pyplot as plt
import numpy as np

class Atmosphere(object):

	def __init__(self, file):
		

		with open(file, 'r') as file:
			full_data = []
			for line in file:
				instance = []
				for element in line.split():
					if element == 'None':
						instance.append(None)
					else:
						instance.append(float(element))

				full_data.append(instance)
		full_data = np.array(full_data).T
		print(full_data)

		self.temp = full_data[0].astype(np.double)
		self.temp_mask = np.isfinite(self.temp)

		self.humid = full_data[1].astype(np.double)
		self.humid_mask = np.isfinite(self.humid)

		self.time_t = full_data[2][self.temp_mask]
		self.time_h = full_data[2][self.humid_mask]

	def plot(self):
		fig = plt.figure("Temperature (C) and Humidity (%)")

		ax1 = fig.add_subplot(111)
		ax2 = ax1.twinx()
		ax1.set_xlim((0,40))
		ax1.set_xlabel("Time")
		ax1.plot(self.time_t, self.temp[self.temp_mask], 'r-')
		ax1.set_ylabel("Temperature (C)", color='r')
		ax2.plot(self.time_h, self.humid[self.humid_mask], 'b-')
		ax2.set_ylabel("Humidity (%)", color='b')
		ax1.set_title("Temperature (C) and Humidity (%)")
		ax1.grid()
		plt.show()

if __name__ == '__main__':
	atmosphere_file = 'data/atmosphere.txt'
	ATMO = Atmosphere(atmosphere_file)
	ATMO
	ATMO.plot()