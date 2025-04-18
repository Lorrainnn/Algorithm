from shell_sort_common import common

#if n=100-> it would be [96, 64, 48, 36, 32, 27, 24, 18, 16, 12, 9, 8, 6, 4, 3, 2, 1]
#The A003586 sequence, 2^p*3^q, ordered from the largest such number less than n down to 1.
def shell_sort4(nums: list[int]):
    n = len(nums)
    gaps = set()

    p = 0
    while 2**p < n:
        q = 0  
        while (2 ** p) * (3 ** q) < n:
            gaps.add((2 ** p) * (3 ** q))
            q+=1
        p+=1
    
    # boundry check if without gap = 1
    gaps.add(1)
    
    gaps = sorted(gaps, reverse=True)
   

    common(gaps,nums)

if __name__=="__main__":
    nums = [1,3,5,10,5,2,90,100,34]
    shell_sort4(nums)
    print(nums)