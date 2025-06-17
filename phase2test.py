import math
import random
from graph import Graph
from requirements import *
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import linregress

def generate_Erdos(n):
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
    for i in range(n * d-1):
        E.add((M[2*i], M[2*i+1]))

    return Graph(n, E)

def get_random_graph(student_id: str, n: int) -> Graph:
    odd = int(student_id[-1]) % 2 == 1
    return generate_Erdos(n) if odd else generate_Bara(n)


if __name__ == "__main__":
    Ns = [1000, 3000, 10000, 30000, 100000]
    TRIALS = 3
    
    student_id = '1'
    # student_id = '2'

    diameters = []
    clustering = []

    for n in Ns:
        diam_sum = 0
        clust_sum = 0
        for _ in range(TRIALS):
            g = get_random_graph(student_id, n)
            diam_sum += get_diameter(g)
            clust_sum += get_clustering_coefficient(g)
        diameters.append(diam_sum / TRIALS)
        clustering.append(clust_sum / TRIALS)

    # 转 numpy
    Ns_np = np.array(Ns)
    log_Ns = np.log(Ns_np)

    # Diameter linear fit on log(N)
    slope_diam, intercept_diam, r_value_diam, _, _ = linregress(log_Ns, diameters)
    fit_diam = intercept_diam + slope_diam * log_Ns

    # Clustering theory curve (for ER)
    theory_clust = (2 * np.log(Ns_np)) / Ns_np

    # Plot
    plt.figure(figsize=(10, 4))

    # Diameter subplot
    plt.subplot(1, 2, 1)
    plt.semilogx(Ns, diameters, marker='o', label='Avg Diameter')
    plt.semilogx(Ns, fit_diam, linestyle='--', color='red',
                 label=f'Best Fit: y = {slope_diam:.2f}·log(n) + {intercept_diam:.2f}, R²={r_value_diam**2:.3f}')
    plt.title("Average Diameter vs n")
    plt.xlabel("n (log scale)")
    plt.ylabel("Avg Diameter")
    plt.legend()
    plt.grid(ls='--', alpha=0.5)

    # Clustering subplot
    plt.subplot(1, 2, 2)
    plt.semilogx(Ns, clustering, marker='o', color='orange', label='Avg Clustering')
    if student_id == '1':
        plt.semilogx(Ns, theory_clust, linestyle='--', color='blue', label='Theory: 2ln(n)/n')
    plt.title("Avg Clustering Coefficient vs n")
    plt.xlabel("n (log scale)")
    plt.ylabel("Avg Clustering")
    plt.legend()
    plt.grid(ls='--', alpha=0.5)

    plt.tight_layout()
    plt.savefig("fig_diameter_clustering.png")
    plt.close()