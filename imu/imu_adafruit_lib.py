import time
import adafruit_lsm6ds
from adafruit_extended_bus import ExtendedI2C as I2C

i2c = I2C(3)
sox = adafruit_lsm6ds.LSM6DS33(i2c)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(sox.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s"%(sox.gyro))
    print("")
    time.sleep(0.5)
