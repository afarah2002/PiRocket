import queue
import itertools
import matplotlib.animation as animation
import multiprocessing
import threading
import time

import comms.communicate as communicate
# import groundstation.pc_threads as pc_threads
# import groundstation.gui_module.utils as gui_utils
# import groundstation.gui_module.framework as gui_framework


def build_pi_client(pi_IP):
	while True:
		time.sleep(1.)
		try:
			pi_client = communicate.Client(pi_IP, port=50007)
			if pi_client:
				break
		except ConnectionRefusedError:
			print("No Pi yet...")
	print("Pi found")
	return pi_client

def build_pc_server(pc_IP):
	pc_server = communicate.Server(pc_IP, port=50007)
	return pc_server

def main():

	# Comms
	pi_IP = "192.168.1.222"
	pi_client = build_pi_client(pi_IP)
	pc_IP = "192.168.1.192"
	pc_server = build_pc_server(pc_IP)

	# Queues
	main_data_queue = queue.Queue()
	'''
	Main data includes
	 - Raw IMU data (XYZ lin acc, RPY ang vel)
	 - Temperature 
	 - Humidity
	 
	'''