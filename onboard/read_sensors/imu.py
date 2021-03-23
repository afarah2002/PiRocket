import numpy as np
import time
##IMU imports##
import adafruit_lsm6ds
from adafruit_extended_bus import ExtendedI2C as I2C

class ReadIMU(object):

        def read(self):
                try:
                        i2c = I2C(3)
                        imu = adafruit_lsm6ds.LSM6DS33(i2c)
                        accel_array =  imu.acceleration
                        angvel_array = imu.gyro
                except RuntimeError as error:
                        accel_array = (None, None, None)
                        angvel_array = (None, None, None)

		return accel_array, angvel_array

                #print(accel_array, "\n", angvel_array, "\n\n")

# if __name__ == '__main__':
#         while True:
#                 ReadIMU().read()
