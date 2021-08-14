import numpy as np
import matplotlib.pyplot as plt
from utils import *


''' Recursively generates the list of all possible paths, starting with 0:
	For each point, adds all paths starting by this point -> calls get_all_path on the set of all points except the chosen point
	fp allows to force the first point to be 0
	Functions calculates the length of the path as well
	-> return the pair (path_i, length_i) with i going from 1 to (n-1)! (number of permutation of the set [1, n-1]'''
def get_all_paths(inds, dists, points, fp = False):
	n = len(inds)
	if(n == 0): return [([], 0)]

	paths = []
	for p in [inds[0]] if fp else inds:
		n_point = list(inds)
		del n_point[n_point.index(p)]

		n_paths = get_all_paths(n_point, dists, points)
		for path in n_paths:
			if(path[0] == []): # Cas limite de la récursion
				d = dists[p, 0]
				paths.append([[p], d])
			else:
				d = dists[p, path[0][0]]
				paths.append([[p] + path[0], d + path[1]])
	return paths

''' Selects the best path'''
def get_best_path(inds, dists, points):
        paths = get_all_paths(inds, dists, points, True)
        best_path = min(paths, key = lambda p: p[1]) # p[1] correction à l'élément length de (path, length)

        return best_path

''' Set of predetermined points for testing'''
points = [(-0.464, -0.48), (-0.106, -0.155), (-0.484, 0.2225), (0.12, -0.66), (0.308, 0.275), (-0.004, 0.5), (0.51, -0.2525), (-0.4, -0.1825), (0.03, -0.135)]
''' Set of 9 random points'''
#points = gen_points(9)

dists = create_distance_matrix(points)

best_path = get_best_path(list(range(9)), dists, points)

display_path(best_path[0], points)
plot_points(points)

plt.title("Meilleur chemin - méthode exhaustive")

plt.show()
