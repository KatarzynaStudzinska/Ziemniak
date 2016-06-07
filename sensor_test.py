import serial
from ctypes import *
import struct
import time
from threading import Thread
from math import sin, cos, pi
ser = serial.Serial("COM5", 9600)

time.sleep(2)
def odczyt():

    x = ser.read(1)
    if x == b's':
        data = ser.read(56)
        return (struct.unpack('ffffffffffffff', data))

while(1):
    x, y, p0, p00, p1, p11, p2, p22, p3, p33, p4, p44, p5, p55 = odczyt()
    print (p2, " Wiwat K atalonia ", p4)