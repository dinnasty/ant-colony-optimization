import matplotlib.pyplot as plt
import numpy as np
import numpy.random as npr
from utils import *

''' Met à jour les phéromones : chemin plus court = plus de phéromones '''
def update_pheromones(path, path_length, pheromone_matrix):

	for i in range(0, len(pheromone_matrix)):
		pt1 = path[i-1]
		pt2 = path[i]

		pheromone_matrix[pt1][pt2] += 1/path_length

''' Pour un point donné, connaissant les points qui n\'ont pas encore été parcourus par la fourmi, calcule la probabilité pour chaque points'''
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

''' Point suivant choisi par la fourmi en fonction des probabilités de chaque point'''
def next_point(last_point, points_left, pheromone_matrix, distance_matrix, a, b):
	batch = gen_probas(last_point, points_left, pheromone_matrix, distance_matrix, a, b)
	return npr.choice(points_left, 1, p=batch)[0]

''' Code le comportement de la fourmi : choisit les points un par un au hasard en tenant compte de la distance et des phéromones, en gardant en mémoire les points restants
	De plus, la longueur du chemin est calculée au fur et à mesure de l'avancement de la fourmi, en utilisant des distances précalculées pour accélérer le programme
	a et b sont les paramètres de réglage modifiant l'importance de la distance et des phéromones dans le choix de la fourmi '''
def fourmi(points, pheromone_matrix, distance_matrix, a, b):
	nb_points = len(points)
	path = [0] # le chemin sera construit dans cette liste. exemple de chemin : [0, 6, 4, 2, 3, 5, 1] (remarque : les chemins sont fermés : le dernier point est relié au premier)
	points_left = list(points)
	path_length = 0
	for i in range(nb_points):
		n_p = next_point(path[-1], points_left, pheromone_matrix, distance_matrix, a, b)

		del points_left[points_left.index(n_p)]

		path_length += distance_matrix[path[-1]][n_p]
		
		path.append(n_p)
	return path, path_length

''' Simule nb_gen générations de fourmis, avec a = 4 et b = 1, et renvoie le meilleur chemin.
	Remplit en plus deux graphes : longueur du chemin par génération et longueur du meilleur chemin trouvé jusqu'alors à la n-ième génération'''
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

''' Fonction principale, qui exécute generations() avec des paramètres de test, et affiche les graphes utiles '''
def main():
	nb_points = 20
	nb_gen = 1000
	points = gen_points(nb_points)
	distance_matrix = create_distance_matrix(points)
	
	path, pheromone_matrix, _, length_graph, best_length_graph = generations(points, nb_gen, distance_matrix)
	
	plt.subplot(1, 2, 1)

	display_path(path, points)
	plot_points(points)
	plt.title("Meilleur chemin")

	plt.subplot(1, 2, 2)

	plt.plot(list(range(nb_gen)), length_graph, label='Longueur du chemin')
	plt.plot(list(range(nb_gen)), best_length_graph, label='Meilleur longueur')

	plt.legend()
	plt.title("Evolution de la longueur du chemin au cours des générations")
	plt.show()

main()