from typing import List

def first_fit(items: List[float], assignment: List[int], free_space: List[float]) -> None:
    """
    First Fit bin packing algorithm:
    - For each item, scan all existing bins in order.
    - Place the item into the first bin with enough free space.
    - If no bin can accommodate the item, open a new bin.

    Params:
    - items: sizes of items to pack (each between 0 and 1).
    - assignment: pre-allocated list; assignment[i] will be set to the bin index for item i.
    - free_space: initially empty; will be appended with the remaining space of each newly opened bin.
    """
    for i, size in enumerate(items):
        placed = False
        # Try to place into the first bin that fits
        for j, space in enumerate(free_space):
            if space >= size:
                free_space[j] -= size
                assignment[i] = j
                placed = True
                break

        # If not placed, open a new bin
        if not placed:
            new_idx = len(free_space)
            assignment[i] = new_idx
            free_space.append(1.0 - size)


def first_fit_decreasing(items: List[float], assignment: List[int], free_space: List[float]) -> None:
    """
    First Fit Decreasing bin packing algorithm:
    - First sort items by size in descending order (preserving original indices for mapping);
    - Then apply the first_fit algorithm to the sorted list;
    - The resulting assignment_decr array indicates, for each sorted item, which bin it was placed into.
    """
    # Pair each item with its original index and sort by size descending
    indexed = sorted(enumerate(items), key=lambda x: x[1], reverse=True)
    sorted_sizes = [size for _, size in indexed]

    # Prepare temporary containers for sorted items
    assignment_decr: List[int] = [0] * len(items)
    free_space_decr: List[float] = []

    # Run first fit on the sorted list
    first_fit(sorted_sizes, assignment_decr, free_space_decr)

    # Transfer results back into the caller's free_space and assignment lists
    free_space.extend(free_space_decr)
    for sorted_idx, bin_idx in enumerate(assignment_decr):
        original_idx = indexed[sorted_idx][0]
        assignment[original_idx] = bin_idx

