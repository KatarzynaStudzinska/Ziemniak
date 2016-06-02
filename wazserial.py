import serial
from ctypes import *
import struct
import time
from threading import Thread
from math import sin, cos, pi
ser = serial.Serial("COM5", 9600)



class Dane():
    def __init__(self):
        self.points_list = []
        self.position = []
        Thread(target=self.joinLandmark, args=()).start()
        Thread(target=self.send, args=()).start()
        self.x = 0
        self.y = 0

    def checksum(self, f1, f2):

        all_bytes = []
        for b1 in f1:
            all_bytes.append(ord(b1))
        for b1 in f2:
            all_bytes.append(ord(b1))

        LRC = 0x00
        for k in all_bytes:
            LRC += k & 0xFF
        LRC = (((LRC ^ 0xFF) + 1) & 0xFF)
        return LRC

    def send(self):#, x, y):
        time.sleep(2)
        xx = float(0)#float(x)
        yy = float(500)#float(y)

        ser.write(b's')
        ser.write(struct.pack('f', xx))
        ser.write(struct.pack('f', yy))
        wiw = self.checksum(struct.pack('f', xx), struct.pack('f', xx))
        ser.write(struct.pack('i', wiw))


    def odczyt(self):

        x = ser.read(1)
        if x == b's':
            data = ser.read(56)
            return (struct.unpack('ffffffffffffff', data))

    def corect_data(self, p0, p1):
        if (float(p0) > 5 and float(p0) < 24):
            return float(p0)
        elif (float(p1) > 5 and float(p1) < 24):
            return float(p1)
        else:
            return -6.6
        pass

    def joinLandmark(self):
        while(1):
            try:
                x, y, p0, p00, p1, p11, p2, p22, p3, p33, p4, p44, p5, p55 = self.odczyt()
                print(p0, p1,  p2,  p3,  p4,  p5)
                x = float(x)/10
                y = float(y)/10
                p0 = self.corect_data(p0, p00)
                p1 = self.corect_data(p1, p11)
                p2 = self.corect_data(p2, p22)
                p3 = self.corect_data(p3, p33)
                p4 = self.corect_data(p4, p44)
                p5 = self.corect_data(p5, p55)

                x0 = int(float(x) + (6.6 + p0) * cos(2.*pi/3))
                y0 = int(float(y) + (6.6 + p0) * sin(2.*pi/3))
                x1 = int(float(x) + (6.6 + p1) * cos(pi/3))
                y1 = int(float(y) + (6.6 + p1) * sin(pi/3))
                #x2 = int(float(x) + (6.6 + p2) * cos(0))
                #y2 = int(float(y) + (6.6 + p2) * sin(0))
                x3 = int(float(x) + (6.6 + p3) * cos(5.*pi/3))
                y3 = int(float(y) + (6.6 + p3) * sin(5.*pi/3))
                x4 = int(float(x) + (6.6 + p4) * cos(4.*pi/3))
                y4 = int(float(y) + (6.6 + p4) * sin(4.*pi/3))
                #x5 = int(float(x) + (6.6 + p5) * cos(pi))
                #y5 = int(float(y) + (6.6 + p5) * sin(pi))

                if (x >=0 and x < 10000 and y >=0 and y < 10000):
                    self.position.append([float(x), float(y)])

                # self.points_list.append([x0, y0])
                # self.points_list.append([x1, y1])
                #
                # self.points_list.append([x3, y3])
                # self.points_list.append([x4, y4])


                if not x0 == int(x) and not y0 == int(y):
                    self.points_list.append([x0, y0])
                if not x1 == int(x) and not y1 == int(y):
                    self.points_list.append([x1, y1])
                # if not x2 == int(x) and not y2 == int(y):
                #     self.points_list.append([x2, y2])
                if not x3 == int(x) and not y3 == int(y):
                    self.points_list.append([x3, y3])
                if not x4 == int(x) and not y4 == int(y):
                    self.points_list.append([x4, y4])
                # if not x5 == int(x) and not y5 == int(y):
                #     self.points_list.append([x5, y5])
                #print(self.points_list)
            except:
                pass

