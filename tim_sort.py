def tim_sort(nums: list[int]):

    #for separate into runs
    def extract_runs(nums: list[int]):
        runs = []
        i = 0
        n = len(nums)

        while i < n:
            run_start = i
            i += 1
            #check limit ->last 2
            if i == n:
                runs.append(nums[run_start:i])
                break

            increase = nums[i] >= nums[i - 1]

            while i < n and (
                #ascending
                (increase and nums[i] >= nums[i - 1]) or
                #descending
                (not increase and nums[i] <= nums[i - 1])
            ):
                i += 1
            #find one run
            run = nums[run_start:i]
            if not increase:
                run.reverse()

            runs.append(run)
        return runs
    
    def merge(left, right):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        #append resulting lists
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    
    runs = extract_runs(nums)
    R = []
    i = 0
    #based on lecture ppt: it pushes the first run onto a stack, and 
    #starts processing runs left to right, pushing 
    #each new run onto the stac
    while i<len(runs):
        R.append(runs[i])
        i+=1
        while True:
            if len(R)>=3 and len(R[-1])>len(R[-3]):
                R[-2] = merge(R[-2],R[-3])
                del R[-3]   
            elif len(R)>=2 and len(R[-1])>=len(R[-2]):
                R[-2] = merge(R[-1],R[-2])
                R.pop()
            elif len(R)>=3 and len(R[-1])+len(R[-2])>=len(R[-3]):
                R[-2] = merge(R[-1],R[-2])
                R.pop()
            elif len(R)>=4 and len(R[-2])+len(R[-3])>=len(R[-4]):
                R[-2] = merge(R[-1],R[-2])
                R.pop()
            else:
                break

    while len(R)!= 1:
        R[-2] = merge(R[-1],R[-2])
        R.pop()
    
    nums[:] = R.pop()

if __name__=="__main__":
    nums = [1,3,5,10,5,2,90,100,34]
    tim_sort(nums)
    print(nums)
