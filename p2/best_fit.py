# best_fit.py

from typing import List
from zipzip_tree import ZipZipTree, Rank  # 同上，可留可不留

def best_fit(items: List[float], assignment: List[int], free_space: List[float]) -> None:
    """
    Best Fit:
      - 对于每个 item，线性扫描所有箱子，
        找到 free_space[j] >= size 且 (free_space[j] - size) 最小的箱子放入；
      - 如果没有合适的，就新开箱。
    """
    for i, size in enumerate(items):
        best_j = None
        best_remain = 2.0  # 大于 1.0，作为初始“不可能”为最优
        for j in range(len(free_space)):
            remain = free_space[j] - size
            if remain >= 0 and remain < best_remain:
                best_remain = remain
                best_j = j
        if best_j is None:
            # 新开箱
            new_idx = len(free_space)
            assignment[i] = new_idx
            free_space.append(1.0 - size)
        else:
            # 放入最紧凑箱
            assignment[i] = best_j
            free_space[best_j] -= size


def best_fit_decreasing(items: List[float], assignment: List[int], free_space: List[float]) -> None:
    """
    Best Fit Decreasing:
      - 先对 items 做降序排序（同上保留原索引），
      - 然后调用 best_fit。
    """
    indexed = sorted(enumerate(items), key=lambda x: x[1], reverse=True)
    sorted_sizes = [size for _, size in indexed]
    assignment_decr = [0] * len(items)
    free_space_decr = []
    best_fit(sorted_sizes, assignment_decr, free_space_decr)

    free_space.extend(free_space_decr)
    for new_i, bin_idx in enumerate(assignment_decr):
        original_i = indexed[new_i][0]
        assignment[original_i] = bin_idx
