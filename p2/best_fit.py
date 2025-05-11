
from typing import List

def best_fit(items: List[float], assignment: List[int], free_space: List[float]) -> None:
    """
    Best Fit bin packing algorithm:
    - For each item, scan all existing bins,
      find the bin j with free_space[j] >= size that leaves the smallest remaining space (tightest fit);
    - If no suitable bin is found, open a new bin.
    """
    for i, size in enumerate(items):
        best_j = None
        best_remain = float('inf')  # Initialize to infinity to find the minimal leftover
        for j in range(len(free_space)):
            remain = free_space[j] - size
            if remain >= 0 and remain < best_remain:
                best_remain = remain
                best_j = j
        if best_j is None:
            # Open a new bin
            new_idx = len(free_space)
            assignment[i] = new_idx
            free_space.append(1.0 - size)
        else:
            # Place in the best-fit bin
            assignment[i] = best_j
            free_space[best_j] -= size


def best_fit_decreasing(items: List[float], assignment: List[int], free_space: List[float]) -> None:
    """
    Best Fit Decreasing bin packing algorithm:
    - First, sort items in descending order (while preserving original indices),
    - Then apply the standard best_fit algorithm.
    """
    # Pair items with their original indices and sort by size descending
    indexed = sorted(enumerate(items), key=lambda x: x[1], reverse=True)
    sorted_sizes = [size for _, size in indexed]

    # Prepare temporary containers for the sorted items
    assignment_decr: List[int] = [0] * len(items)
    free_space_decr: List[float] = []

    # Run best fit on the sorted list
    best_fit(sorted_sizes, assignment_decr, free_space_decr)

    # Transfer results back to the original assignment list
    free_space.extend(free_space_decr)
    for sorted_idx, bin_idx in enumerate(assignment_decr):
        original_idx = indexed[sorted_idx][0]
        assignment[original_idx] = bin_idx

