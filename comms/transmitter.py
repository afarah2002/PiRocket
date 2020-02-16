#!/usr/bin/env python2

import serial
from subprocess import Popen, PIPE
import time

connectCommand = "sudo rfcomm listen 08:AE:D6:97:B2:52"
running_procs = [Popen(connectCommand.split(), stdout=PIPE, stderr=PIPE)]

class Transmitter(object):
	def __init__(self, channel):
		while running_procs:
			for proc in running_procs:
				retcode = proc.poll()
				time.sleep(1)
				running_procs.remove(proc)
				break
		self.ser = serial.Serial(channel, baudrate=9600, timeout = 1)
		print(self.ser.name)
	def sendData(self, data):
		self.ser.write(data)
		#self.ser.close()

if __name__ == '__main__':
	channel = "/dev/rfcomm8"
	TR = Transmitter(channel)
	TR
	counter = 0
	while True:
		counter += 1
		time.sleep(1)
		TR.sendData(str(counter)+"\n")
