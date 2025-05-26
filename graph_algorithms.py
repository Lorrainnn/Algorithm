# explanations for these functions are provided in requirements.py

# Explanations for graph algorithm functions
#
# get_diameter(): return the approximate graph diameter using a heuristic function.
# get_clustering_coefficient(): return the graph's global clustering coefficient.
# get_degree_distribution(): returns a dictionary representing the degree distribution of the graph.
#                            the keys are the degree, and the values is the number of nodes with that
#                            degree.

from graph import Graph

def get_diameter(graph: Graph) -> int:
	raise NotImplementedError


def get_clustering_coefficient(graph: Graph) -> float:
	raise NotImplementedError


def get_degree_distribution(graph: Graph) -> dict[int, int]:
	raise NotImplementedError
