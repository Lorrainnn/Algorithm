from zipzip_tree import ZipZipTree, Node
from typing import List

class Bin:
    """Represents a bin with remaining capacity."""
    def __init__(self, remaining_capacity: float):
        self.remaining_capacity = remaining_capacity


def best_fit(
    items: List[float],
    assignment: List[int],
    free_space: List[float],
    bin_capacity: float = 1.0
) -> None:
    """
    Best-Fit bin packing:
      - For each item size:
          • Use tree.best_fit(size) to find the tightest-fitting bin node.
          • If None, open a new bin; otherwise update the found bin.
    """
    # Initialize tree with upper bound on bin count
    tree = ZipZipTree(len(items))
    assignment.clear()
    free_space.clear()

    for size in items:
        node = tree.best_fit(size)
        if node is None:
            # open new bin
            bin_id = len(free_space)
            remaining = bin_capacity - size
            free_space.append(remaining)
            assignment.append(bin_id)
            tree.insert(bin_id, Bin(remaining))
        else:
            # use existing bin
            bin_id = node.key
            assignment.append(bin_id)
            remaining = node.val.remaining_capacity - size
            free_space[bin_id] = remaining

            # preserve original rank for rebalance
            orig_rank = node.rank
            tree.remove(bin_id)
            tree.insert(bin_id, Bin(remaining), rank=orig_rank)


def best_fit_decreasing(
    items: List[float],
    assignment: List[int],
    free_space: List[float],
    bin_capacity: float = 1.0
) -> None:
    """
    Best-Fit Decreasing:
      - Sort items in descending order, then apply best_fit logic.
    """
    tree = ZipZipTree(len(items))
    assignment.clear()
    free_space.clear()

    # sort items by size descending (keep original index)
    indexed = sorted(enumerate(items), key=lambda x: x[1], reverse=True)
    temp_assign = [0] * len(items)

    for orig_idx, size in indexed:
        node = tree.best_fit(size)
        if node is None:
            bin_id = len(free_space)
            remaining = bin_capacity - size
            free_space.append(remaining)
            tree.insert(bin_id, Bin(remaining))
        else:
            bin_id = node.key
            remaining = node.val.remaining_capacity - size
            free_space[bin_id] = remaining
            orig_rank = node.rank
            tree.remove(bin_id)
            tree.insert(bin_id, Bin(remaining), rank=orig_rank)
        temp_assign[orig_idx] = bin_id

    # restore assignment in original order
    assignment.extend(temp_assign)
