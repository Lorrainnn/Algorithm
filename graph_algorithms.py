# explanations for these functions are provided in requirements.py

# Explanations for graph algorithm functions
#
# get_diameter(): return the approximate graph diameter using a heuristic function.
# Heuristic Idea 2


# get_clustering_coefficient(): return the graph's global clustering coefficient.


# get_degree_distribution(): returns a dictionary representing the degree distribution of the graph.
#                            the keys are the degree, and the values is the number of nodes with that
#                            degree.

from graph import Graph
import random


def get_diameter(graph: Graph) -> int:
	# Heuristic Idea 2
	start = random.choice(graph.get_nodes())
	D_max = float('-inf')
	node, distance = graph.get_maximum_distance(start)

	while distance > D_max:
		D_max = distance
		node, distance = graph.get_maximum_distance(node)
	return D_max


def get_degree_distribution(graph: Graph) -> dict[int, int]:
	all_nodes = graph.get_nodes()
	distribution = {}
	for n in all_nodes:
		distribution[n] = len(graph.get_neighbors(n))
	return distribution


def get_clustering_coefficient(graph: Graph) -> float:
	#denominator
	all_nodes = graph.get_nodes()
	denominator = 0
	for n in all_nodes:
		val  = graph.get_degree(n)
		denominator+=val*(val-1)/2

	#numerator - graph degeneracy

	info = get_degree_distribution(graph)


def compute_degeneracy(graph: Graph):
	#1
	L = []
	HL = set()

	#2
	dv = get_degree_distribution(graph)

	#3 degree bucket
	max_deg = max(dv.values())
	D = [[] for _ in range(max_deg + 1)]
	for v, deg in dv.items():
		D[deg].append(v)
	
	#4
	n = graph.get_num_nodes()
	Nv = {v: [] for v in range(n)}

	#5
	k=0

	#6
	for _ in range(n):

		for i, bucket in enumerate(D):
			if bucket:
				break
		
		k=max(k,i)

		v = D[i].pop()
		L.insert(0, v)
		HL.add(v)

		for w in graph.get_neighbors(v):
			if w not in HL:
				old = dv[w]
				new = dv[w] - 1
				dv[w] = new

                # Move w to the cell of D corresponding to the new value of dw 
                D[old].remove(w)
                if new >= len(D):
                    D.extend([] for _ in range(new - len(D) + 1))
                D[new].append(w)

                # add w to N_v[v]
                N_v[v].append(w)

    return k, L, N_v


	

