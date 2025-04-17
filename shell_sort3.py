import math
from shell_sort_common import common

#The A083318 sequence, 2^k + 1, for k=log n, ..., 3, 2, 1, plus the value 1.
def shell_sort3(nums: list[int]):
    n = len(nums)
    k = int(math.log2(n))
    gaps = []

    #all gaps
    while k >= 1:
        gap = 2 ** k + 1
        if gap < n:
            gaps.append(gap)
        k -= 1

    # boundry check if without gap = 1
    if 1 not in gaps:
        gaps.append(1)

    common(gaps,nums)

if __name__=="__main__":
    nums = [1,3,5,10,5,2,90,100,34]
    shell_sort3(nums)
    print(nums)
