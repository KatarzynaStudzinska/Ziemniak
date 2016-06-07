# def odczyt():
#     import serial
#     import struct
#     ser = serial.Serial("COM6", 256000)
#     while True:
#         vS = ser.read(48)
#         print (struct.unpack('ffffffffffff', vS))
#
# odczyt()

import matplotlib.pyplot as plt
import math as m
import time
from PyQt4 import QtCore, QtGui
import copy

to = [[300, 300], [300, 303], [300, 307], [302, 312], [300, 313], [301, 320], [300, 322], [300, 326],
             [300, 328], [300, 331], [301, 335], [300, 340], [300, 345],
             [200, 100], [205, 110], [211, 122], [217, 120], [221, 125], [224, 130], [225, 127],
             [224, 130], [225, 132], [231, 132], [237, 135], [238, 135], [244, 138], [245, 137],
             [246, 138], [246, 138], [242, 142], [227, 145], [245, 145], [251, 148], [252, 147],
              [253, 144], [255, 142], [256, 140], [257, 135], [260, 133], [260, 128], [263, 125],
              [265, 124], [270, 122], [273, 120], [277, 116], [277, 107], [279, 118], [280, 108],
      [500,400], [501,401], [504,403], [505,407], [518,411], [510,424], [512,417], [515,420],
      [516,423], [518,425], [521,428], [532,430]]

b = [[200, 100], [205, 110], [211, 122], [217, 120], [221, 125], [224, 130], [225, 127],
                         [224, 130], [225, 132], [231, 132], [237, 135], [238, 135], [244, 138], [245, 137],
                          [246, 138], [246, 138], [242, 142], [227, 145], [245, 145], [251, 148], [252, 147]]



def leastSquares( landmarks):   #zwraca wspolczynniki a i b prostej
    Exy = 0
    Ex = 0
    Ey = 0
    Ex2 = 0
    for sth in landmarks:
            Exy = Exy + sth[0]*sth[1]
            Ex = Ex + sth[0]
            Ey = Ey + sth[1]
            Ex2 = Ex2 + sth[0]**2
    n = len(landmarks)
    a = (n*Exy - Ex*Ey)/(n*Ex2 - Ex**2 + 0.00001)
    b = Ey/n - a*Ex/n
    return [a, b]


def paintLandGroup(landmarks, qp):
    a, b = leastSquares(landmarks)
    first_point = landmarks[0]
    last_point = landmarks[-1]

    if a < m.fabs(0.1):
        qp.plot([first_point[0],last_point[0]] , [first_point[1],  last_point[1]])
        return [[first_point[0],first_point[1]] , [last_point[0], last_point[1]]]#return [first_point, last_point]
    else:
        y0 = a*first_point[0] + b
        y1 = a*last_point[0] + b

        qp.plot([first_point[0], last_point[0]], [y0, y1])
        qp.plot([first_point[0], last_point[0]], [y0, y1])

        return [[first_point[0], y0], [last_point[0], y1]]#[[first_point[0], y0, [last_point[0], y1]]# zwracamy P0, P1



def closersPoint(sth, helpfull_list, max_dist):
                                #w sumie obliczamy dystans od
    sth_list = []
    sth_distance_list = []
    for othersth in helpfull_list:
        distance = m.sqrt((sth[0] - othersth[0])**2 + (sth[1] - othersth[1])**2)
        if len(sth_list) < 20 and distance < max_dist:
            sth_list.append(othersth)
            sth_distance_list.append(distance)
        else:
            if not sth_distance_list == []:
                if distance < max(sth_distance_list):   #jezeli obliczona dlugosc jest mniejsza od najwiekszej z listy

                    index_maximum = sth_distance_list.index(max(sth_distance_list))
                    sth_list.remove(sth_list[index_maximum])
                    sth_distance_list.remove(sth_distance_list[index_maximum])

                    sth_list.append(othersth)
                    sth_distance_list.append(distance)

    for i in sth_list:
        helpfull_list.remove(i)

    return sth_list #zwracamy liste punktow, ktore tworza prosta, tj. takich, ktore sa siebie blisko


def paintBlock(list_of_lines_end, qp):
    group = []
    x = []
    y = []
    for end in list_of_lines_end:
        if len(x) == 0:
            x.append(end[0])
            x.append(end[2])
            y.append(end[1])
            y.append(end[3])
        if m.sqrt((end[0] - x[-1])**2 + (end[1] - y[-1])**2 ) < 100:
            x.append(end[0])
            x.append(end[2])
            y.append(end[1])
            y.append(end[3])
            pass
        else:
            group.append([x, y])
            x = []
            y = []
            x.append(end[0])
            x.append(end[2])
            y.append(end[1])
            y.append(end[3])

    pass

def writeToTab(point): #dziala zle

    if point%10 > 5:
        return (point - point%10)/10 + 1
    else:
        return (point - point%10)/10


def main():
    landmarks1 = []
    for punkt in to:
        landmarks1.append([writeToTab(punkt[0]), writeToTab(punkt[1])])
    landmarks = []
    for punkt in landmarks1:
        landmarks.append([punkt[0]*10, punkt[1]*10])


    lines_end =[] # lista zawierajaca konce obliczonych lini
    helpfull_list = copy.copy(landmarks)#landmarks.copy()
    for sth in landmarks:
        plt.plot(sth[0],   sth[1], '.')
        pass

    for sth in helpfull_list:
        list_to_paint = closersPoint(sth, helpfull_list, 60)
        lines_end.append(paintLandGroup(list_to_paint, plt))
        print(paintLandGroup(list_to_paint, plt))

        first_point, last_point = paintLandGroup(list_to_paint, plt)
        i = 0
        plt.Rectangle((400, 400), 120, 150)
        while first_point[0] + i*10 < last_point[0] and first_point[1] + i*10 < last_point[1]:
            print(i)
            plt.Rectangle((first_point[0] + i*10, first_point[1] + i*10), 60, 60)
            i = i+1




    #plt.plot([list_of_lines_end[0][0], list_of_lines_end[1][0]], [list_of_lines_end[0][1], list_of_lines_end[1][1]], 'r')
    #paintBlock(lines_end, plt)

    plt.show()


if __name__ == "__main__":
    main()