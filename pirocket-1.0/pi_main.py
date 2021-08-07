import queue
import threading
import time

import comms.communicate as communicate
# import pi.pi_threads as pi_threads

def build_pi_server(pi_IP):
	pi_server = communicate.Server(pi_IP, port=50007)
	return pi_server

def build_pc_client(pc_IP):
	while True:
		time.sleep(1.)
		try:
			pc_client = communicate.Client(pc_IP, port=50007)
			if pc_client:
				break
		except ConnectionRefusedError:
			print("No PC yet...")
	print("PC found")
	return pc_client

def main():

	# Comms
	pi_IP = "192.168.1.222"
	pi_server = communicate.Server(pi_IP, port=50007)
	pc_IP  = "192.168.1.192"
	pc_client = build_pc_client(pc_IP)

	# Queues
	