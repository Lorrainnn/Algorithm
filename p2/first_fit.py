from dataclasses import dataclass
from zipzip_tree import ZipZipTree, Node, Rank, KeyType
from decimal import Decimal



@dataclass
class FirstFit_Val:
    remain_c: Decimal
    best_remain_c: Decimal

class ZipZipTree_FirstFit(ZipZipTree):
    def __init__(self, capacity: int):
        super().__init__(capacity)


    def insert(self, key: KeyType, val: FirstFit_Val, rank: Rank = None):
        # insert new bin, then update subtree
        super().insert(key, val, rank)
        self.update_tree(key) 

        
    def update_node(self, node: Node):
        # get best from left child, or 0 if none
        if node.left:
            best_left = node.left.val.best_remain_c 
        else:
            best_left = 0

        #right
        if node.right:
            best_right = node.right.val.best_remain_c 
        else:
            best_right = 0

        self_remain = node.val.remain_c
        node.val.best_remain_c = max(self_remain,best_left,best_right)
    

    def update_tree(self, key: KeyType):
        #general updation of tree: find node
        cur = self.root
        path_stack = []

        while cur is not None:
            path_stack.append(cur)
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                break
        
        #bottom-up updation ->similar to bfs?
        while path_stack:
            node = path_stack.pop()
            self.update_node(node)
        
    
    def find_first_fit(self, item_size: float) -> Node:
        #search for the first bin that has enough space
        cur = self.root
        best_fit = None

        while cur is not None:
            left_best = cur.left.val.best_remain_c if cur.left else Decimal(0)
            right_best = cur.right.val.best_remain_c if cur.right else Decimal(0)

            if left_best >= item_size:
                # try left subtree
                cur = cur.left
            elif cur.val.remain_c >= item_size:
                # current bin fits
                best_fit = cur
                break
            elif right_best >= item_size:
                #try right subtree
                cur = cur.right
            else:
                #no fit
                break

        return best_fit        


def first_fit(items: list[float], assignment: list[int], free_space: list[float]):
    tree = ZipZipTree_FirstFit(len(items))
    bin_capacity = Decimal(1.0)
    index = 0 

    for i, item in enumerate(items):
        item = Decimal(str(item))
        best_bin = tree.find_first_fit(item)

        if best_bin is None:
            # no existing bin fits, open a new one
            new_bin_val = FirstFit_Val(remain_c = bin_capacity - item, best_remain_c = bin_capacity - item)
            tree.insert(index, new_bin_val, tree.get_random_rank())
            assignment[i] = index

            new_bin_free_space = bin_capacity - item
            free_space.append(float(new_bin_free_space))

            index += 1
        else:
            # use the found bin
            assignment[i] = best_bin.key
            best_bin.val.remain_c = best_bin.val.remain_c - item

            free_space[best_bin.key] = float(best_bin.val.remain_c)
            tree.update_tree(best_bin.key)


def first_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    sorted_items = sorted(items, reverse=True)
    first_fit(sorted_items, assignment, free_space)

