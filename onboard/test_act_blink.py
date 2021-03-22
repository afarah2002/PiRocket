import os
from time import sleep

os.system('sudo su')
os.system('echo heartbeat  >/sys/class/leds/led0/trigger')
