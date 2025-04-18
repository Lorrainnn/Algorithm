from shell_sort_common import common

#The A003462 sequence, (3^k - 1) / 2
# in reverse order, starting from the largest value less than n, down to 1.
def shell_sort5(nums: list[int]):
    n = len(nums)
    gaps = []
    
    k = 1
    gap = (3 ** k - 1) // 2
    while gap < n:
        gaps.append(gap)
        k += 1
        gap = (3 ** k - 1) // 2

    gaps.sort(reverse=True)

    common(gaps,nums)




if __name__=="__main__":
    nums = [1,3,5,10,5,2,90,100,34]
    shell_sort5(nums)
    print(nums)