#----------imports----------#
from ctypes import c_short
import smbus
import time
import math
import picamera
import numpy as np
from multiprocessing import Process, Pipe



#----------code starts here!----------#

#set up the bus and address

#ENABLE THE GYROS HERE!!!
class IMUAttitudeDetermination(object):

	#turn on all of the sensors via the control registers, sets variables for each register
	def __init__(self, address):
		self.address = address
		self.bus = smbus.SMBus(3)
		#define address (look at the data sheet)

		#print the who am i register set to 69h
		whoami = self.bus.read_byte_data(address, 0x0f)

		#turns on linear acceeration sensor
		self.bus.write_byte_data(address, 0x10,0x18)

		#enables the x y and z sensors
		self.bus.write_byte_data(address, 0x18, 0x38)

		#enables the gyro
		self.bus.write_byte_data(address, 0x11, 0x82)

		#LOW------------------------------
		#GYRO code 
		self.rx_addressL = 0x22
		self.ry_addressL = 0x24
		self.rz_addressL = 0x26

		#LINEAR ACCELERATOR code
		self.lx_addressL = 0x28
		self.ly_addressL = 0x2a
		self.lz_addressL = 0x2c
		#---------------------------------
		#HIGH-----------------------------
		#GYRO code 
		self.rx_addressH = 0x23
		self.ry_addressH = 0x25
		self.rz_addressH = 0x27

		#LINEAR ACCELERATOR code
		self.lx_addressH = 0x29
		self.ly_addressH = 0x2b
		self.lz_addressH = 0x2d
		#---------------------------------

	def readLinearAccelerators(self):
		lxL = self.bus.read_byte_data(self.address,self.lx_addressL)
		lyL = self.bus.read_byte_data(self.address,self.ly_addressL)
		lzL = self.bus.read_byte_data(self.address,self.lz_addressL)
		lxH = self.bus.read_byte_data(self.address,self.lx_addressH)
		lyH = self.bus.read_byte_data(self.address,self.ly_addressH)
		lzH = self.bus.read_byte_data(self.address,self.lz_addressH)

		self.lxCombined = (lxL | lxH <<8)
		self.lyCombined = (lyL | lyH <<8)
		self.lzCombined = (lzL | lzH <<8)

		print("Attitude:", [self.lxCombined, self.lyCombined, self.lzCombined])

		return self.lxCombined, self.lyCombined, self.lzCombined

	def readGyros(self):
		# rxL = self.bus.read_byte_data(self.address,self.rx_addressL)
		# ryL = self.bus.read_byte_data(self.address,self.ry_addressL)
		# rzL = self.bus.read_byte_data(self.address,self.rz_addressL)
		startTime = time.time()



		self.rxH = int(self.bus.read_byte_data(self.address,self.rx_addressH)*360/255) 
		if self.rxH > 180:
			self.rxH -= 360

		self.ryH = int(self.bus.read_byte_data(self.address,self.ry_addressH)*360/255)  
		if self.ryH > 180:
			self.ryH -= 360
		
		self.rzH = int(self.bus.read_byte_data(self.address,self.rz_addressH)*360/255) 
		if self.rzH > 180:
			self.rzH -= 360

		print("Orientation:", [self.rxH, self.ryH, self.rzH])
		print "\n"

		return [self.rxH, self.ryH, self.rzH]
	def sendAttitude(self):
		lx = self.lx
		ly = self.ly
		lz = self.lz
		rx = self.rx
		ry = self.ry
		rz = self.rz

		info_list = [lx, ly, lz, rx, ry, rz]

		# print(" LX: ", self.lx, "\n", "LY: ", self.ly, "\n", "LZ: ", self.lz,"\n", "RX: ", self.rx,"\n", "RY: ", self.ry, "\n", "RZ: ", self.rz, "\n")
		return info_list

	def convertUnits(self):
		# lxReal = (self.lxCombined if self.lxCombined < 32768 else self.lxCombined - 65536)*.244/1000
		# lyReal = (self.lxCombined if self.lyCombined < 32768 else self.lyCombined - 65536)*.244/1000
		# lzReal = (self.lxCombined if self.lzCombined < 32768 else self.lzCombined - 65536)*.244/1000
		lxReal = (c_short(self.lxCombined).value)*.244/1000
		lyReal = (c_short(self.lyCombined).value)*.244/1000
		lzReal = (c_short(self.lzCombined).value)*.244/1000
		# rxReal = self.rxAngle
		# ryReal = self.ryAngle
		# rzReal = self.rzAngle
		print(" LX: ", lxReal,  " g ", "\n", "LY: ", lyReal,  " g ", "\n", "LZ: ", lzReal, " g ", "\n")# "RX: ", rxReal, " dps ", "\n", "RY: ", ryReal, " dps ", "\n", "RZ: ", rzReal, " dps ", "\n")
		time.sleep(0.03)
		return [lxReal, lyReal, lzReal]



def main():
	while True:
		imu = IMUAttitudeDetermination(0x6A)#<------ place the address you find here!!!!!!!
		imu.readLinearAccelerators()
		imu.readGyros()


if __name__ == '__main__':
	main()