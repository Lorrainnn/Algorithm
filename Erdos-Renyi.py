import math
import random
from graph import Graph

def generate_Erdos(n,p):
    """
    Input: 
        number of vertices n
        edge probability 0<p<1
    """
    p = 2 * math.log(n) / n
    E = set()
    v=1
    w=-1
    while v<n:
        r = random.random()             
        gap = math.floor(math.log(1 - r) / math.log(1 - p))
        w=w+1+gap
        while w>=v and v<n:
            w=w-v
            v=v+1
        if v<n:
            E.add((v, w))
    return Graph(n, E)
