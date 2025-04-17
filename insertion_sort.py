# Example file: insertion_sort.py

# Each sorting function should accept a list of integers as the single required
# parameter, as shown below. The input list should be sorted upon completion.
def insertion_sort(nums: list[int]):
	#start from index 1
	for i in range(1,len(nums)):
		val = nums[i]
		j=i-1
		#find correct position: element bigger -> all right shift
		while j>=0 and nums[j] > val:
			nums[j+1]=nums[j]
			j-=1
		nums[j+1]=val
