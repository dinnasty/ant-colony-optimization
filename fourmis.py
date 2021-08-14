import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
from utils import *

''' Updates pheromones : shorter path = more pheromones '''
def update_pheromones(path, path_length, pheromone_matrix):

	for i in range(0, len(pheromone_matrix)):
		pt1 = path[i-1]
		pt2 = path[i]

		pheromone_matrix[pt1][pt2] += 1/path_length

''' Calculate the probability of the ant to go to a given possible next point '''
def gen_probas(last_point, pt_left, pheromone_matrix, distance_matrix, a, b):
	probas = []
	total = 0
	for p in pt_left:
		ro = 1 / distance_matrix[last_point][p]
		delta = pheromone_matrix[last_point][p]
		proba = ro ** a * delta ** b

		probas.append(proba)
		total += proba
	probas = [proba / total for proba in probas] # On divise par la somme des probabilités pour obtenir un SCE (somme des probabilités = 1)
	return probas

''' Next point chosen by the ant given the probabilities '''
def next_point(last_point, points_left, pheromone_matrix, distance_matrix, a, b):
	batch = gen_probas(last_point, points_left, pheromone_matrix, distance_matrix, a, b)
	return npr.choice(points_left, 1, p=batch)[0]

''' Ant behavior : chooses points one by one and randomly while taking into account distance and pheromone levels. Stores in memory the points it hasn't yet been to.
	Path length is calculated during the ant's travel, uses the precalculated distances.
	a and b are parameters modifying the impact of distance or pheromones in the ant's behavior '''
def fourmi(points, pheromone_matrix, distance_matrix, a, b):
	nb_points = len(points)
	path = [0] # path is build in this list. path list example : [0, 6, 4, 2, 3, 5, 1] (paths are closed : the last point is linked to the first)
	points_left = list(points)
	path_length = 0
	for i in range(nb_points):
		n_p = next_point(path[-1], points_left, pheromone_matrix, distance_matrix, a, b)

		del points_left[points_left.index(n_p)]

		path_length += distance_matrix[path[-1]][n_p]
		
		path.append(n_p)
	return path, path_length

''' Simulate nb_gen generations of ants and returns the best path found, with a = 4 et b = 1.
	two graphs : [length of path per generation] and [length of best found path before the nth generation]'''
def generations(points, nb_gen, distance_matrix):
	nb_points = len(points)
	pheromone_matrix = np.ones((nb_points, nb_points))

	best_path = []
	best_path_length = 100000000

	length_graph = []
	best_length_graph = []

	for i in range(nb_gen):

		path, path_length = fourmi(list(range(1,nb_points)), pheromone_matrix, distance_matrix, 4, 1)

		if path_length < best_path_length:
			best_path_length = path_length
			best_path        = path

		length_graph.append(path_length)
		best_length_graph.append(best_path_length)

		update_pheromones(path,      path_length,      pheromone_matrix)
		update_pheromones(best_path, best_path_length, pheromone_matrix)

	return best_path, pheromone_matrix, distance_matrix, length_graph, best_length_graph

''' main function that calls generations() with tests parameters and plots useful graphs '''
def main():
	nb_points = 20
	nb_gen = 1000
	points = gen_points(nb_points)
	distance_matrix = create_distance_matrix(points)
	
	path, pheromone_matrix, _, length_graph, best_length_graph = generations(points, nb_gen, distance_matrix)
	
	plt.subplot(1, 2, 1)

	display_path(path, points)
	plot_points(points)
	plt.title("Best path")

	plt.subplot(1, 2, 2)

	plt.plot(list(range(nb_gen)), length_graph, label='Path length')
	plt.plot(list(range(nb_gen)), best_length_graph, label='Best length')

	plt.legend()
	plt.title("Path length evolution during the different generations")
	plt.show()

main()
