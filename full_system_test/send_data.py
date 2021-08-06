import socket
import sys
from time import sleep
import random
from struct import pack
import pickle

sys.path.append("/home/pi/Documents/PiRocket")
import onboard.read_sensors.dht11 as dht11
import onboard.read_sensors.imu as imu


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

host, port = '192.168.1.192', 65000
server_address = (host, port)

# Generate some random start values
x, y, z = random.random(), random.random(), random.random()
raw_temp, raw_hum = 0., 0.

# Send a few messages
for i in range(100):

    # Pack three 32-bit floats into message and send
    raw_acc, raw_ang_vel = imu.ReadIMU().read()
    raw_temp, raw_hum = dht11.ReadDHT11().read()

    float_data_pack = (raw_temp,
                       raw_hum)
    acc_pack = pickle.dumps(raw_acc)
    ang_vel_pack = pickle.dumps(raw_ang_vel)

    try:
        message = pack('2f', raw_temp, raw_hum)
        sock.sendto(message, server_address)
    except:
        message = pack('2f', 0., 0.)
        sock.sendto(message, server_address)

    sleep(.1)


