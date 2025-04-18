from shell_sort_common import common

#The A003462 sequence, (3^k - 1) / 2
# in reverse order, starting from the largest value less than n, down to 1.
def shell_sort5(nums: list[int]):
    n = len(nums)
    gaps = set()
    
    k = 1
    gap = (3 ** k - 1) // 2
    while gap < n:
        gaps.add(gap)
        k += 1
        gap = (3 ** k - 1) // 2
    
    # boundry check if without gap = 1
    gaps.add(1)

    gaps = sorted(gaps, reverse=True)

    common(gaps,nums)




if __name__=="__main__":
    nums = [1,3,5,10,5,2,90,100,34]
    shell_sort5(nums)
    print(nums)