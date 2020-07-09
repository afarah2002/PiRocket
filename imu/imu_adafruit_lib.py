import time
import board
import busio
import adafruit_lsm6ds

i2c = busio.I2C(board.SCL, board.SDA)

sox = adafruit_lsm6ds.LSM6DSOX(i2c)

while True:
    print("Acceleration: X:%.2f, Y: %.2f, Z: %.2f m/s^2"%(sox.acceleration))
    print("Gyro X:%.2f, Y: %.2f, Z: %.2f radians/s"%(sox.gyro))
    print("")
    time.sleep(0.5)