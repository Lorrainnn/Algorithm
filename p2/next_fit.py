# Example file: next_fit.py

# explanations for member functions are provided in requirements.py

def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
    current_bin = -1
    current_free_space = 0.0

    for i, size in enumerate(items):
        # new bin
        if current_bin < 0 or size > current_free_space:
            current_bin += 1
            assignment[i] = current_bin
        
            free_space.append(1.0 - size)
            current_free_space = free_space[current_bin]
        else:
            #use existing olf bin
            assignment[i] = current_bin
            free_space[current_bin] -= size
            current_free_space = free_space[current_bin]



