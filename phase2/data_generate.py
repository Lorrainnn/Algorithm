import random
import math

def generate_uniform_random_permutation(n):
    arr = list(range(1, n+1))
    random.shuffle(arr)
    return arr

def generate_almost_sorted_permutation(n):
    arr = list(range(1, n+1))
    swaps = int(math.log2(n)) 
    for _ in range(swaps):
        i = random.randint(0, n-1)
        j = random.randint(0, n-1)
        arr[i], arr[j] = arr[j], arr[i]
    return arr

def generate_two_alternating_runs_permutation(n):
    odd = list(range(1, n+1, 2))   
    even = list(range(2, n+1, 2))  
    return odd + even

# 测试一下！
if __name__ == "__main__":
    n = 10 

    print("Random：", generate_uniform_random_permutation(n))
    print("Almost Sort：", generate_almost_sorted_permutation(n))
    print("Two_alternating：", generate_two_alternating_runs_permutation(n))
