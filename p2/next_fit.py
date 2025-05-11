# Example file: next_fit.py

# explanations for member functions are provided in requirements.py

def next_fit(items: list[float], assignment: list[int], free_space: list[float]):
     current_bin = -1
     current_free_space = 0.0
     
     #begin allocate items into box
     for i, size in enumerate(items):
        # open a new bin
        if current_bin < 0 or size > current_free_space:
            current_bin += 1
            assignment[i] = current_bin
            #new bin space
            free_space.append(1.0 - size)
            current_free_space = free_space[current_bin]
            
        # current bin fit
        else:
            assignment[i] = current_bin
            free_space[current_bin] -= size


