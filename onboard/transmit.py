from flask import Flask, render_template, request

import os
import sys
import time

import read_sensors.dht11
import read_sensors.imu

app = Flask(__name__)


@app.route("/")
def collect_data():

	raw_acc, raw_ang_vel = read_sensors.imu.ReadIMU().read()
	raw_temp, raw_hum = read_sensors.dht11.ReadDHT11().read()
	# elapsed_time = time.time() - t0

	data_pack = [raw_acc, raw_ang_vel,
				 raw_temp, raw_hum,
				 ]

	return str(data_pack[0][0])
	#return render_template('index.html', **data_pack)




if __name__ == '__main__':
	t0 = time.time()
	while True:
		app.run(host='192.168.1.222', port=1024, debug=True)
		# data_pack = collect_data()
		# print(data_pack[4])

