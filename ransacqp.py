import math as m

def closersPoint(sth, helpfull_list):
                                #w sumie obliczamy dystans od
    sth_list = []
    sth_distance_list = []
    for othersth in helpfull_list:
        distance = m.sqrt((sth[0] - othersth[0])**2 + (sth[1] - othersth[1])**2)
        if len(sth_list) < 5 and distance < 10:
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


def paintLandGroup(landmarks, qp, aa, X0, Y0):
    a, b = leastSquares(landmarks)
    first_point = landmarks[0]
    last_point = landmarks[-1]

    if a < m.fabs(0.1):
        qp.drawLine(X0 + aa*first_point[0], Y0 +aa*first_point[1], X0 + aa*last_point[0],Y0 + aa*last_point[1])
        return [[first_point[0],first_point[1]] , [last_point[0], last_point[1]]]#return [first_point, last_point]
    else:
        y0 = a*first_point[0] + b
        y1 = a*last_point[0] + b
        qp.drawLine(X0 + aa*first_point[0], Y0 +aa*first_point[1], X0 + aa*last_point[0],Y0 + aa*last_point[1])


        return [[first_point[0], y0], [last_point[0], y1]]#[[first_point[0], y0, [last_point[0], y1]]# zwracamy P0, P1
