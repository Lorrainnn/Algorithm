import time
import numpy as np
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from data_generate import generate_uniform_random_permutation, generate_almost_sorted_permutation, generate_two_alternating_runs_permutation
from insertion_sort import insertion_sort
from tim_sort import tim_sort
from shell_sort1 import shell_sort1
from shell_sort2 import shell_sort2
from shell_sort3 import shell_sort3
from shell_sort4 import shell_sort4
from shell_sort5 import shell_sort5
from skip_list import skip_list_sort
import time
import csv
import numpy as np


def run_and_save_experiment(sort_function, sort_name, generate_data_function, distribution_name, sizes, runs_per_size=5, filename="results.csv"):
    
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='') as file:
        writer = csv.writer(file)
     
        if not file_exists:
            writer.writerow(['Sort Algorithm', 'Distribution', 'Input Size', 'Average Time (seconds)'])
        
        for n in sizes:
            times = []
            for _ in range(runs_per_size):
                data = generate_data_function(n)
                data_copy = data.copy()
                start = time.perf_counter()
                sort_function(data_copy)
                end = time.perf_counter()
                times.append(end - start)
            
            avg_time = np.mean(times)
            writer.writerow([sort_name, distribution_name, n, avg_time])
            print(f"{sort_name} on {distribution_name} size {n}: {avg_time:.6f} sec")


sizes = [10, 100, 500, 1000, 2500, 5000, 10000]
runs_per_size = 8
output_file = "sorting_experiment_results.csv"


run_and_save_experiment(skip_list_sort, "skip_list_sort", generate_uniform_random_permutation, "Random", sizes, runs_per_size, output_file)
run_and_save_experiment(skip_list_sort, "skip_list_sort", generate_almost_sorted_permutation, "Almost Sorted", sizes, runs_per_size, output_file)
run_and_save_experiment(skip_list_sort, "skip_list_sort", generate_two_alternating_runs_permutation, "Two Alternating Runs", sizes, runs_per_size, output_file)


