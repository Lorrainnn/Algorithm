# explanations for member functions are provided in requirements.py
# each file that uses a graph should import it from this file.


# init(): initialize the graph a given number of nodes and given edges.
#         edges are represented as tuples (u, v), where each edge is between node with index u and
#         node with index v. not directional graph
#         the autograder will never add duplicate edges to the graph.
# get_num_nodes(): returns the number of nodes in the graph.
# get_num_edges(): returns the number of edges in the graph.
# get_neighbors(): given a node index, return an iterable type over the collection of its neighbors.
#                  the iterable type can be a list, set, generator, etc.
#                  each neighbor should appear exactly once.


from collections.abc import Iterable

class Graph:
	def __init__(self, num_nodes: int, edges: Iterable[tuple[int, int]]):
		#check boundry?
		if num_nodes<0:
			raise ValueError
		
		self._num_nodes = num_nodes
		self._num_edges = len(edges)
		self.update_ajencency_list(edges)
	
	def update_ajencency_list(self, edges: Iterable[tuple[int, int]]):
		self.ajencency_list = {}
		for u, v in edges:
			self.ajencency_list.setdefault(u, []).append(v)
			self.ajencency_list.setdefault(v, []).append(u)


	def get_num_nodes(self) -> int:
		return self._num_nodes

	def get_num_edges(self) -> int:
		return self._num_edges

	def get_neighbors(self, node: int) -> Iterable[int]:
		if node in self.ajencency_list:
			return self.ajencency_list[node]
		else:
			return []

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define
