import serial
from ctypes import *
import struct
import time

ser = serial.Serial("COM5", 9600)
time.sleep(3)

while(1):
    x = ser.read(1)
    if x == b's':
        data = ser.read(56)
        print(struct.unpack('ffffffffffffff', data))
