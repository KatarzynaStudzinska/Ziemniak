from ransac import leastSquares
import math
import matplotlib.pyplot as plt

point_list = [[3, 0], [3, 2], [3, 3], [3.2, 3], [3, 10]] #[[10, 100], [12, 110], [14, 120], [16, 130], [17, 140]]

def list_from_lastSquare(point_list):
    a, b = leastSquares(point_list)

    solid_point_list = []
    print(a, b)

    start_point = point_list[0]
    last_point = point_list[-1]


    if a < math.fabs(0.1):
        y_range = range(start_point[1], last_point[1])
        xx = start_point[0]
        for y in y_range:
            solid_point_list.append([xx, y])
    else:
        x_range = range(start_point[0], last_point[0])
        for x in x_range:
            solid_point_list.append([x, a*x + b])
    return solid_point_list



if __name__ == "__main__":
    solid_point_list = list_from_lastSquare(point_list)
    plt.plot([i[0] for i in solid_point_list],[i[1] for i in solid_point_list], 'x')
    plt.show()