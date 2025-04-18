import math
from shell_sort_common import common

#The sequence, 2[n/2^(k+1)]+1, for k=1,2,...,log n, where [*] denotes the floor function.
def shell_sort2(nums: list[int]):
    n = len(nums)
    k=1
    gaps = set()

    #all gaps
    while k <= int(math.log2(n)):
        gap = 2 * (n // (2 ** (k + 1))) + 1
        if gap < n:
            gaps.add(gap)
        k += 1

    # boundry check if without gap = 1
    gaps.add(1)

    common(gaps,nums)


if __name__=="__main__":
    nums = [1,3,5,10,5,2,90,100,34,11]
    shell_sort2(nums)
    print(nums)
    