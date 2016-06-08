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

import wazserial
import copy
import time
from threading import Thread
from ransacqp import *
from close_circle import *

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

        self.lined_points = []

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

        self.object = sym.Symulacja()
        self.sensors = wazserial.Dane()

    def showEvent(self, event):
        self.timer = self.startTimer(30)

    def timerEvent(self, event):
        self.update()

    def find_in_tab(self, point):
        if point % 10 > 5:
            return (point - point % 10)/10 + 1
        else:
            return (point - point % 10)/10

    def paintEvent(self, e):
        qp = QtGui.QPainter()
        qp.begin(self)

        a = 4
        X0 = 300
        Y0 = 300



        for sth in self.sensors.points_list:
            list_to_squere = closersPoint(sth, copy.copy(self.sensors.points_list), 60)
            pointed_list = list_from_lastSquare(list_to_squere)
            self.lined_points.extend(pointed_list)

        for point in self.sensors.points_list:
            qp.fillRect(X0 + a*point[0], Y0 - a*point[1], a, a, QtCore.Qt.blue)
        for point in self.sensors.position:
            qp.fillRect(X0 + int(a*point[0]), Y0 - int(a*point[1]), 4, 4, QtCore.Qt.red)

        for point in self.lined_points:
            qp.fillRect(X0 + a*point[0], Y0 - a*point[1], a, a, QtCore.Qt.green)



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

    def keyReleaseEvent(self, e):
        pass

    def drawRobot(self, qp):
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

