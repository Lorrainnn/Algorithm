from shell_sort_common import common

#  The original Shell sequence, [n/2^k ], ..., 1, for k=1,2,...,log n, 
#  where [*] denotes the floor function.
def shell_sort1(nums: list[int]):
    n = len(nums)
    gap = n // 2
    gaps = []

    #all gaps
    while gap>0:
        gaps.append(gap)
        gap //= 2

    # boundry check if without gap = 1
    if 1 not in gaps:
        gaps.append(1)

    common(gaps,nums)




if __name__=="__main__":
    nums = [1,3,5,10,5,2,90,100,34]
    shell_sort1(nums)
    print(nums)
    