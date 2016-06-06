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
        self.position.append([0, 0])
        self.zwrot = 0
        self.xx = 0
        self.yy = 0
        self.x = 0
        self.y = 0
        self.krok_prosto = 100
        self.krok_skret = 250
        self.odl_przeszkoda = 50
        self.czujnik_lewo = 0
        self.czujnik_prosto = 0
        self.czujnik_prawo = 0
        self.czujnik_tyl = 0
        Thread(target=self.joinLandmark, args=()).start()
        #Thread(target=self.send, args=()).start()


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
        #time.sleep(2)
        x = 10*self.position[len(self.position)-1][0]
        y = 10*self.position[len(self.position)-1][1]
        #print("x: " + str(x) + " y: " + str(y))

        #print("odleglosc x: ", str(abs(self.xx - x)),"positionX :", x, "odleglosc y: ", (abs(self.yy - y)), "positionY :", y)

        if(abs(self.xx - x) < 20 and abs(self.yy - y) < 20):
            if self.zwrot == 0:

                if self.czujnik_lewo > self.odl_przeszkoda or self.czujnik_lewo == -6.6:
                    print("zwrot: " + str(self.zwrot) + "lewo")
                    self.zwrot = 270
                    #print [int((x-1)*10), int(y*10)]
                    self.xx = int(x - self.krok_skret)
                    self.yy = int(y)

                elif self.czujnik_prosto > self.odl_przeszkoda or self.czujnik_prosto == -6.6:
                    print("zwrot: " + str(self.zwrot) + "prosto")
                    self.zwrot = 0
                    #print [int((x) * 10), int((y-1) * 10)]
                    self.xx = int(x)
                    self.yy = int(y + self.krok_prosto)

                elif self.czujnik_prawo > self.odl_przeszkoda or self.czujnik_prawo == -6.6:
                    print("zwrot: " + str(self.zwrot) + "prawo")
                    self.zwrot = 90
                    #print [int((x+1) * 10), int(y * 10)]
                    self.xx = int(x + self.krok_skret)
                    self.yy = int(y)

                elif self.czujnik_tyl > self.odl_przeszkoda or self.czujnik_tyl == -6.6:
                    print("zwrot: " + str(self.zwrot) + "tyl")
                    self.zwrot = 180
                    #print [int((x)*10), int((y+1)*10)]
                    self.xx = int(x)
                    self.yy = int(y - self.krok_skret)


            elif self.zwrot == 90:

                if self.czujnik_prosto > self.odl_przeszkoda or self.czujnik_prosto == -6.6:
                    print("zwrot: " + str(self.zwrot) + "prosto")
                    self.zwrot = 0
                    #print [int((x) * 10), int((y-1) * 10)]
                    self.xx = int(x)
                    self.yy = int(y + self.krok_skret)

                elif self.czujnik_prawo > self.odl_przeszkoda or self.czujnik_prawo == -6.6:
                    print("zwrot: " + str(self.zwrot) + "prawo")
                    self.zwrot = 90
                    #print [int((x+1) * 10), int(y * 10)]
                    self.xx = int(x + self.krok_prosto)
                    self.yy = int(y)

                elif self.czujnik_tyl > self.odl_przeszkoda or self.czujnik_tyl == -6.6:
                    print("zwrot: " + str(self.zwrot) + "tyl")
                    self.zwrot = 180
                    #print [int((x)*10), int((y+1)*10)]
                    self.xx = int(x)
                    self.yy = int(y - self.krok_skret)

                elif self.czujnik_lewo > self.odl_przeszkoda or self.czujnik_lewo == -6.6:
                    print("zwrot: " + str(self.zwrot) + "lewo")
                    self.zwrot = 270
                    #print [int((x-1)*10), int(y*10)]
                    self.xx = int(x - self.krok_skret)
                    self.yy = int(y)


            elif self.zwrot == 180:

                if self.czujnik_prawo > self.odl_przeszkoda or self.czujnik_prawo == -6.6:
                    print("zwrot: " + str(self.zwrot) + "prawo")
                    self.zwrot = 90
                    #print [int((x+1) * 10), int(y * 10)]
                    self.xx = int(x + self.krok_skret)
                    self.yy = int(y)

                elif self.czujnik_tyl > self.odl_przeszkoda or self.czujnik_tyl == -6.6:
                    print("zwrot: " + str(self.zwrot) + "tyl")
                    self.zwrot = 180
                    #print [int((x)*10), int((y+1)*10)]
                    self.xx = int(x)
                    self.yy = int(y - self.krok_prosto)

                elif self.czujnik_lewo > self.odl_przeszkoda or self.czujnik_lewo == -6.6:
                    print("zwrot: " + str(self.zwrot) + "lewo")
                    self.zwrot = 270
                    #print [int((x-1)*10), int(y*10)]
                    self.xx = int(x - self.krok_skret)
                    self.yy = int(y)

                elif self.czujnik_prosto > self.odl_przeszkoda or self.czujnik_prosto == -6.6:
                    print("zwrot: " + str(self.zwrot) + "prosto")
                    self.zwrot = 0
                    #print [int((x) * 10), int((y-1) * 10)]
                    self.xx = int(x)
                    self.yy = int(y + self.krok_skret)


            elif self.zwrot == 270:

                if self.czujnik_tyl > self.odl_przeszkoda or self.czujnik_tyl == -6.6:
                    print("zwrot: " + str(self.zwrot) + "tyl")
                    self.zwrot = 180
                    #print [int((x)*10), int((y+1)*10)]
                    self.xx = int(x)
                    self.yy = int(y - self.krok_skret)

                elif self.czujnik_lewo > self.odl_przeszkoda or self.czujnik_lewo == -6.6:
                    print("zwrot: " + str(self.zwrot) + "lewo")
                    self.zwrot = 270
                    #print [int((x-1)*10), int(y*10)]
                    self.xx = int(x - self.krok_prosto)
                    self.yy = int(y)

                elif self.czujnik_prosto > self.odl_przeszkoda or self.czujnik_prosto == -6.6:
                    print("zwrot: " + str(self.zwrot) + "prosto")
                    self.zwrot = 0
                    #print [int((x) * 10), int((y-1) * 10)]
                    self.xx = int(x)
                    self.yy = int(y + self.krok_skret)

                elif self.czujnik_prawo > self.odl_przeszkoda or self.czujnik_prawo == -6.6:
                    print("zwrot: " + str(self.zwrot) + "prawo")
                    self.zwrot = 90
                    #print [int((x+1) * 10), int(y * 10)]
                    self.xx = int(x + self.krok_skret)
                    self.yy = int(y)

            #print(self.xx)
            #print(self.yy)

        ser.write(b's')
        ser.write(struct.pack('f', self.xx))
        ser.write(struct.pack('f', self.yy))
        wiw = self.checksum(struct.pack('f', self.xx), struct.pack('f', self.xx))
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
                x = float(x)/10
                y = float(y)/10
                p0 = self.corect_data(p0, p00)
                p1 = self.corect_data(p1, p11)
                p2 = self.corect_data(p2, p22)
                p3 = self.corect_data(p3, p33)
                p4 = self.corect_data(p4, p44)
                p5 = self.corect_data(p5, p55)
                self.czujnik_lewo = p5
                self.czujnik_prosto = p1
                self.czujnik_prawo = p2
                self.czujnik_tyl = p4
                #print("lewo :" + str(self.czujnik_lewo) + "    prosto :" + str(self.czujnik_prosto) + "    prawo :" + str(self.czujnik_prawo) + "    tyl :" + str(self.czujnik_tyl))

                x0 = int(float(x) + (6.6 + p0) * cos(2.*pi/3))
                y0 = int(float(y) + (6.6 + p0) * sin(2.*pi/3))
                x1 = int(float(x) + (6.6 + p1) * cos(pi/3))
                y1 = int(float(y) + (6.6 + p1) * sin(pi/3))
                x2 = int(float(x) + (6.6 + p2) * cos(0))
                y2 = int(float(y) + (6.6 + p2) * sin(0))
                x3 = int(float(x) + (6.6 + p3) * cos(5.*pi/3))
                y3 = int(float(y) + (6.6 + p3) * sin(5.*pi/3))
                x4 = int(float(x) + (6.6 + p4) * cos(4.*pi/3))
                y4 = int(float(y) + (6.6 + p4) * sin(4.*pi/3))
                x5 = int(float(x) + (6.6 + p5) * cos(pi))
                y5 = int(float(y) + (6.6 + p5) * sin(pi))
                self.position.append([float(x), float(y)])


                if not x0 == int(x) and not y0 == int(y):
                    self.points_list.append([x0, y0])
                if not x1 == int(x) and not y1 == int(y):
                    self.points_list.append([x1, y1])
                if not x2 == int(x) and not y2 == int(y):
                    self.points_list.append([x2, y2])
                if not x3 == int(x) and not y3 == int(y):
                    self.points_list.append([x3, y3])
                if not x4 == int(x) and not y4 == int(y):
                    self.points_list.append([x4, y4])
                if not x5 == int(x) and not y5 == int(y):
                    self.points_list.append([x5, y5])
                #print(self.points_list)
                self.send()
            except:
                pass

# s = b"s"
# c_s = c_char_p(s) # tutaj mamy wskaznik na char?
# bitstart = c_char(b's')#tutaj mam nadzieje, ze mamy chara..
#
#
# k = 0
# floatlist = [200, 200]
# print(floatlist, "floatlist")
# buf = struct.pack('%sf' % len(floatlist), *floatlist)
#
#
#
#
# while (1):
#     x, y, p0, p00, p1, p11, p2, p22, p3, p33, p4, p44, p5, p55 = odczyt()
#
#     print(x, y)

    # print("kk")
    # ser.write(b's') #(b's')
    # #floatlist = [20]
    # #buf = struct.pack('%sf' % len(floatlist), *floatlist)
    # ser.write(b'g')

