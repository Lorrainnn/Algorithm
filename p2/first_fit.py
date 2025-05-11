# first_fit.py

from typing import List
from zipzip_tree import ZipZipTree, Rank  # 你可以保留这行以符合作业要求，但下面实现并不使用树

def first_fit(items: List[float], assignment: List[int], free_space: List[float]) -> None:
    """
    First Fit:
      - 对于每个 item，线性扫描现有所有箱子，
        找到第一个 free_space[j] >= size 就放进去；
      - 如果都放不下，就开新箱。
    """
    for i, size in enumerate(items):
        placed = False
        # 试着放进第一个能放下的箱子
        for j in range(len(free_space)):
            if free_space[j] >= size:
                free_space[j] -= size
                assignment[i] = j
                placed = True
                break
        # 如果没有找到，就新开一个箱
        if not placed:
            new_idx = len(free_space)
            assignment[i] = new_idx
            free_space.append(1.0 - size)


def first_fit_decreasing(items: List[float], assignment: List[int], free_space: List[float]) -> None:
    """
    First Fit Decreasing:
      - 先把 items 按 size 降序排序（保留原始索引顺序给 assignment 使用），
      - 然后调用 first_fit。
      - assignment[i] 指的是“排序后第 i 件物品”放进的箱子号。
    """
    # 1) 生成索引列表并按 size 降序
    indexed = sorted(enumerate(items), key=lambda x: x[1], reverse=True)
    # 2) 构造“降序后”的 sizes 列表
    sorted_sizes = [size for _, size in indexed]
    # 3) 创建一个新的 assignment_decr，调用 first_fit
    assignment_decr = [0] * len(items)
    free_space_decr = []
    first_fit(sorted_sizes, assignment_decr, free_space_decr)
    # 4) 将结果写回调用者提供的 free_space 和 assignment
    free_space.extend(free_space_decr)
    for new_i, bin_idx in enumerate(assignment_decr):
        # new_i 对应 sorted_sizes[new_i]，也就是原始 items[indexed[new_i][0]]
        original_i = indexed[new_i][0]
        assignment[original_i] = bin_idx
