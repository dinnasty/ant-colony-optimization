"""
Repo of functions used in the two other .py files
"""
import random as rnd
import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr

def gen_points(nb_points):		#generates points on the plane
	points = []
	for i in range(nb_points):
		x = rnd.random() * 2 - 1
		y = rnd.random() * 2 - 1
		points.append((x, y))

	return points

def plot_points(points):		#shows a list of points on the plane
	x_list = []
	y_list = []

	for pt in points:
		x_list.append(pt[0])
		y_list.append(pt[1])
	plt.scatter(x_list, y_list)

def display_path(path, points):		#shows the path taken by an ant on the plane
    nb_points = len(points)
    
    x_list = []
    y_list = []

    for i in range(nb_points):
        pt = points[path[i]]
        x_list.append(pt[0])
        y_list.append(pt[1])
    pt = points[path[0]]
    x_list.append(pt[0])
    y_list.append(pt[1])

    plt.plot(x_list, y_list, 'o-')

def dist(pt1, pt2):		#calculates the distance between two points
	dx = pt2[0] - pt1[0]
	dy = pt2[1] - pt1[1]

	distance = np.sqrt(dx*dx + dy*dy)

	return distance

def create_distance_matrix(points):		#creates the distance matrix between all of the points
    nb_points = len(points)
    matrix = np.ones((nb_points, nb_points))

    for i in range(nb_points):
        for j in range(nb_points):
            matrix[i][j] = dist(points[i], points[j])

    return matrix
