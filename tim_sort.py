
from insertion_sort import insertion_sort
def tim_sort(nums: list[int]):

    MIN_RUN = 32


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
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

    n = len(nums)
    runs = []

    # Step 1: Break the array into runs and sort them with insertion sort
    i = 0
    while i < n:
        run_end = min(i + MIN_RUN - 1, n - 1)
        insertion_sort(nums, i, run_end)
        runs.append((i, run_end))
        i = run_end + 1

    # Step 2: Merge runs on stack (simulate the merging rules in your image)
    size = MIN_RUN
    while size < n:
        for start in range(0, n, size * 2):
            mid = min(n - 1, start + size - 1)
            end = min(n - 1, start + size * 2 - 1)
            if mid < end:
                merged = merge(nums[start:mid + 1], nums[mid + 1:end + 1])
                nums[start:start + len(merged)] = merged
        size *= 2

    return nums

