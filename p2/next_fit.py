# Example file: next_fit.py

# explanations for member functions are provided in requirements.py

def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
	bin_capacity = 1.0
	index = 0
	free_space.append(bin_capacity)

	for i,item in enumerate(items):
		if free_space[index] >= item - 1e-12:
			assignment[i] = index
			free_space[index] -= item
		else:
			index += 1
			free_space.append(bin_capacity - item)
			assignment[i] = index



