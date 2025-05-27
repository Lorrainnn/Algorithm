import math
import random
from graph import Graph
from requirements import *
import matplotlib.pyplot as plt

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
    for i in range(0, 2 * n * d):
        E.add((M[2*i], M[2*i]))

    return Graph(n, E)

def get_random_graph(student_id: str, n: int) -> Graph:
    odd = int(student_id[-1]) % 2 == 1
    return generate_Erdos(n) if odd else generate_Bara(n)


if __name__=="__main__":
    Ns = [1000, 10000, 100000]
    TRIALS = 3
    random.seed(42)
    student_id = '1'
    # ------------------ Plot avg diameter / clustering ------------------

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


    plt.figure(figsize=(10, 4))

    plt.subplot(1, 2, 1)
    plt.semilogx(Ns, diameters, marker='o')
    plt.title("Average Diameter vs n")
    plt.xlabel("n (log scale)")
    plt.ylabel("Avg Diameter")

    plt.subplot(1, 2, 2)
    plt.semilogx(Ns, clustering, marker='o', color='orange')
    plt.title("Avg Clustering Coefficient vs n")
    plt.xlabel("n (log scale)")
    plt.ylabel("Avg Clustering")

    plt.tight_layout()
    plt.savefig("fig_diameter_clustering.png")
    plt.close()

    # ------------------ Plot degree distribution ------------------

    for n in Ns:
        g = get_random_graph(student_id, n)
        dist = get_degree_distribution(g)
        degrees = list(dist.keys())
        counts = [dist[d] for d in degrees]

        # Save lin-lin and log-log
        plt.figure(figsize=(10, 4))

        plt.subplot(1, 2, 1)
        plt.scatter(degrees, counts, s=10)
        plt.title(f"Degree Dist (lin-lin), n={n}")
        plt.xlabel("Degree")
        plt.ylabel("Count")

        plt.subplot(1, 2, 2)
        plt.loglog(degrees, counts, marker='o', linestyle='none')
        plt.title(f"Degree Dist (log-log), n={n}")
        plt.xlabel("log(Degree)")
        plt.ylabel("log(Count)")

        plt.tight_layout()
        plt.savefig(f"fig_degdist_n{n}.png")
        plt.close()