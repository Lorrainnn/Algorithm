import random
from graph import Graph

def generate_Bara(n,d=5):
    """
    Input: Number of vertices n
    """
    M = [None] * (2 * n * d)


    for v in range(n):
        for i in range(d):
            M[2*(v*d+i)] = v  
            r = random.randint(0, 2*(v*d+i))
            M[2*(v*d+i) + 1] = M[r]   
            
    E = set()
    for i in range(0, 2 * n * d):
        E.add((M[2*i], M[2*i]))

    return Graph(n, E)