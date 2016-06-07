# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'GUIKatarzyna.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import math as m
import Symulacja as sym
import numpy as np
import ransac
import wazserial
import copy
import time
from threading import Thread
from ransacqp import *


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class MyWidget(QtGui.QWidget):
    lines_numberx = 80
    lines_numbery = 60

    def __init__(self, parent):
        QtGui.QWidget.__init__(self)
        self.setParent(parent)
        self.show()
        self.trace = []
        self.czekaj = 0

        self.x = 10
        self.y = 680
        self.theta = 0
        self.a = 40
        self.first_step = True
        self.wymiar = 80

        self.landmarks = []
        self.list_of_landmark = []
        self.map = np.zeros((self.wymiar, self.wymiar)) # mapa
        self.zwrot = 0
        for elem in range(self.wymiar - 1):
            self.map[elem][self.wymiar - 1] = 1
            self.map[self.wymiar - 1][elem] = 1
            self.map[0][elem] = 1
            self.map[elem][0] = 1


        #self.keys = [False, False, False, False]
        self.object = sym.Symulacja()
        self.sensors = wazserial.Dane()



    def showEvent(self, event):
        #time.sleep(5.0)
        self.timer = self.startTimer(30)

    def timerEvent(self, event):
        """if self.keys[0]:
            self.theta -= 2
        elif self.keys[1]:
            self.theta += 2
        if self.keys[2]:
            self.x += 2*m.sin(self.theta*m.pi/180)
            self.y -= 2*m.cos(self.theta*m.pi/180)
        elif self.keys[3]:
            self.x -= 2*m.sin(self.theta*m.pi/180)
            self.y += 2*m.cos(self.theta*m.pi/180)"""

        #self.x = self.object.coord[0]
        #self.y = self.object.coord[1]
        way = self.find_way()
        self.x = way[0]
        self.y = way[1]

        #self.sensors.send(100, 100)

        #self.theta = self.object.coord[2]

        #self.trace.append([self.x, self.y])
        #self.list_of_landmark.append()
        #self.list_of_landmark = self.object.points_list #tutaj zapisuje punkty z sensorow
        #self.map[self.object.points_list[-1][0]][self.object.points_list[-1][1]] = 1



        #print(self.map[self.object.points_list[0], self.object.points_list[1]] )
        #print(self.object.points_list[-1][0],self.object.points_list[-1][1], self.object.points_list[-1])
        self.update()

    def find_way(self):

        x = int(self.findInTab(self.x))
        y = int(self.findInTab(self.y))
        #print(self.map[int(x + 1)][int(y)])
       # if self.map[int(x + 1)][int(y)] == 0 and not self.trace.__contains__([int(x + 1), int(y)]):# and self.czekaj > 5:
          #  return [int((x + 1)*10), int(y*10)]




       # else:
        #    return [int((x)*10), int(y*10)]
       # pass

        # if self.map[int(x)][int(y)] == 0 and not self.trace.__contains__([int(x), int(y)]):
        #     return [int((x)*10), int(y*10)]

        if self.zwrot == 0:

            if self.map[x - 1][y] == 0 and not self.trace.__contains__([ x - 1,y]):
                self.zwrot = 270
                #print [int((x-1)*10), int(y*10)]
                return [int((x-1)*10), int(y*10)]

            if self.map[x][y - 1] == 0 and not self.trace.__contains__([x, y - 1]):
                self.zwrot = 0
                #print [int((x) * 10), int((y-1) * 10)]
                return [int((x) * 10), int((y-1) * 10)]


            if self.map[x + 1][y] == 0 and not self.trace.__contains__([ x + 1, y]):
                self.zwrot = 90
                #print [int((x+1) * 10), int(y * 10)]
                return [int((x+1) * 10), int(y * 10)]


            if self.map[x][y+1] == 0 and not self.trace.__contains__([x, y+1]):
                self.zwrot = 180
                #print [int((x)*10), int((y+1)*10)]
                return [int((x)*10), int((y+1)*10)]

        if self.zwrot == 90:

            if self.map[x][y - 1] == 0 and not self.trace.__contains__([x, y - 1]):
                self.zwrot = 0
                #print [int((x) * 10), int((y - 1) * 10)]
                return [int((x) * 10), int((y - 1) * 10)]
            if self.map[x + 1][y] == 0 and not self.trace.__contains__([x + 1, y]):
                self.zwrot = 90
                #print [int((x + 1) * 10), int(y * 10)]
                return [int((x + 1) * 10), int(y * 10)]

            if self.map[x][y + 1] == 0 and not self.trace.__contains__([x, y + 1]):
                self.zwrot = 180
                #print [int((x) * 10), int((y + 1) * 10)]
                return [int((x) * 10), int((y + 1) * 10)]

            if self.map[x-1][y] == 0 and not self.trace.__contains__([x-1, y]):
                self.zwrot = 270
                #print [int((x - 1) * 10), int(y * 10)]
                return [int((x - 1) * 10), int(y * 10)]

        if self.zwrot == 180:


            if self.map[x + 1][y] == 0 and not self.trace.__contains__([x + 1, y]):
                self.zwrot = 90
                #print [int((x + 1) * 10), int(y * 10)]
                return [int((x + 1) * 10), int(y * 10)]

            if self.map[x][y + 1] == 0 and not self.trace.__contains__([x, y + 1]):
                self.zwrot = 180
                #print [int((x) * 10), int((y + 1) * 10)]
                return [int((x) * 10), int((y + 1) * 10)]

            if self.map[x - 1][y] == 0 and not self.trace.__contains__([x - 1, y]):
                self.zwrot = 270
                #print [int((x - 1) * 10), int(y * 10)]
                return [int((x - 1) * 10), int(y * 10)]

            if self.map[x][y - 1] == 0 and not self.trace.__contains__([x, y - 1]):
                self.zwrot = 0
                #print [int((x) * 10), int((y - 1) * 10)]
                return [int((x) * 10), int((y - 1) * 10)]

        if self.zwrot == 270:



            if self.map[x][y + 1] == 0 and not self.trace.__contains__([x, y + 1]):
                self.zwrot = 180
                #print [int((x) * 10), int((y + 1) * 10)]
                return [int((x) * 10), int((y + 1) * 10)]

            if self.map[x - 1][y] == 0 and not self.trace.__contains__([x - 1, y]):
                self.zwrot = 270
                #print [int((x - 1) * 10), int(y * 10)]
                return [int((x - 1) * 10), int(y * 10)]

            if self.map[x][y - 1] == 0 and not self.trace.__contains__([x, y - 1]):
                self.zwrot = 0
                #print [int((x) * 10), int((y - 1) * 10)]
                return [int((x) * 10), int((y - 1) * 10)]

            if self.map[x + 1][y] == 0 and not self.trace.__contains__([x + 1, y]):
                self.zwrot = 90
                #print [int((x + 1) * 10), int(y * 10)]
                return [int((x + 1) * 10), int(y * 10)]


    def findInTab(self, point):

        if point % 10 > 5:
            return (point - point % 10)/10 + 1
        else:
            return (point - point % 10)/10

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)
        a = 4#15
        X0 = 300
        Y0 = 300
        lines_end = []
        helpfull_list = copy.copy(self.sensors.points_list)
        self.najmniejsze_kwadraty(self.sensors.points_list, qp, a, X0, Y0)
        # for sth in self.sensors.points_list:
        #     list_to_paint = closersPoint(sth, copy.copy(self.sensors.points_list), 35)
        #     print(list_to_paint)
        #     lines_end.append(paintLandGroup(list_to_paint, qp, a, X0, Y0))
        #
        # for para in lines_end:
        #     end_to_paint = closersPoint(sth, copy.copy(self.sensors.points_list), 50)
        #     paintLandGroup(end_to_paint, qp, a, X0, Y0)
        #     # first = para[0]
        #     # last = para[1]
        #
        #     pass



        for (point, index) in zip(self.sensors.points_list, range(len(self.sensors.points_list))):
            qp.fillRect(X0 + a*point[0], Y0 - a*point[1], a, a, QtCore.Qt.blue)
        for point in self.sensors.position:
            qp.fillRect(X0 + int(a*point[0]), Y0 - int(a*point[1]), 4, 4, QtCore.Qt.red)

        qp.end()

    def najmniejsze_kwadraty(self, points, qp, scale, x0, y0):
        n = len(points)
        if n > 3:
            x = 0
            y = 0
            xx = 0
            xy = 0
            ymin = 99999999999999999999999
            ymax = -99999999999999999999999
            for point in points:
                if point[1] < ymin:
                    ymin = point[1]
                if point[1] > ymax:
                    ymax = point[1]
                x += point[0]
                y += point[1]
                xx += point[0]**2
                xy += point[0]*point[1]
            xsr = x/n
            ysr = y/n
            a = (n*xy - x*y) / (n*xx - x**2)
            b = ysr - a*xsr
            qp.drawLine(x0 + scale*(ymin - b)/a, y0 - scale*ymin, x0 + scale*(ymax - b)/a, y0 - scale*ymax)



    def keyPressEvent(self, e):
        pass
        """if e.key() == QtCore.Qt.Key_Left:
            self.keys[0] = True
        elif e.key() == QtCore.Qt.Key_Right:
            self.keys[1] = True
        if e.key() == QtCore.Qt.Key_Up:
            self.keys[2] = True
        elif e.key() == QtCore.Qt.Key_Down:
            self.keys[3] = True"""

    def keyReleaseEvent(self, e):
        pass
        """if e.key() == QtCore.Qt.Key_Left:
            self.keys[0] = False
        elif e.key() == QtCore.Qt.Key_Right:
            self.keys[1] = False
        if e.key() == QtCore.Qt.Key_Up:
            self.keys[2] = False
        elif e.key() == QtCore.Qt.Key_Down:
            self.keys[3] = False"""


    def drawRobot(self, qp):
        #qp.setPen(QtCore.Qt.blue)
        for i in self.trace:
            qp.drawPoint(i[0], i[1])
        qp.setBrush(QtCore.Qt.red)
        qp.translate(self.x, self.y)
        qp.rotate(self.theta)
        #needle = QtGui.QPolygon([QtCore.QPoint(30, 0), QtCore.QPoint(-30, 0), QtCore.QPoint(0, 200)])
        #qp.drawPolygon(needle)
        qp.drawPolygon(QtCore.QPoint(0, -self.a*m.sqrt(3)/3), QtCore.QPoint(-self.a/2, self.a*m.sqrt(3)/6), QtCore.QPoint(self.a/2, self.a*m.sqrt(3)/6))


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        from win32api import GetSystemMetrics
        Form.resize(GetSystemMetrics(0), GetSystemMetrics(1))
        self.widget = MyWidget(Form)
        self.widget.setGeometry(QtCore.QRect(2, 2, GetSystemMetrics(0) + 2, GetSystemMetrics(1) + 2))
        self.widget.setObjectName(_fromUtf8("widget"))

        self.widget.setFocus()
        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Form", None))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    Form = QtGui.QWidget()
    ui = Ui_Form()
    ui.setupUi(Form)
    Form.show()
    sys.exit(app.exec_())

