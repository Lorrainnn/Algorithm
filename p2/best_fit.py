from dataclasses import dataclass
from zipzip_tree import ZipZipTree, Node, Rank, KeyType
from decimal import Decimal


@dataclass
class BestFit_Val:
    remain_c: Decimal
    best_remain_c: Decimal


class ZipZipTree_BestFit(ZipZipTree):
    def __init__(self, capacity: int):
        super().__init__(capacity)
    
    def insert(self, key: KeyType, val: BestFit_Val, rank: Rank = None):
        super().insert(key, val, rank)
        self.update_tree(key)

    #follow same logic in first fit
    def update_node(self_remain, node: Node):
        #get best from left child or 0 if missing
        if node.left:
            best_left = node.left.val.best_remain_c 
        else:
            best_left = 0

        if node.right:
            best_right = node.right.val.best_remain_c 
        else:
            best_right = 0
            
        self_remain = node.val.remain_c

        node.val.best_remain_c = max(self_remain, best_left, best_right)
    

    
    def update_tree(self, key: KeyType):
        cur = self.root
        path_stack = []
        #recheck: ok
        while cur is not None:
            path_stack.append(cur)
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                break
        
        while path_stack:
            node = path_stack.pop()
            self.update_node(node)
    
    #recheck: use queue or stack: ok
    def find_best_fit(self, item_size: Decimal) -> Node:
        best_fit = None
        #best fit definition
        best_cap = Decimal('Infinity')
        path_stack = [self.root]

        while path_stack:
            cur = path_stack.pop()
            if cur:
                if cur.val.remain_c >= item_size and cur.val.remain_c < best_cap:
                    best_fit = cur
                    best_cap = cur.val.remain_c

                # push children that might fit
                if cur.left and cur.left.val.best_remain_c >= item_size:
                    path_stack.append(cur.left)

                if cur.right and cur.right.val.best_remain_c >= item_size:
                    path_stack.append(cur.right)

        return best_fit



def best_fit(items: list[float], assignment: list[int], free_space: list[float]):
    bin_tree = ZipZipTree_BestFit(len(items))
    bin_capacity = Decimal(1.0)
    index = 0 

    for i, item in enumerate(items):
        item = Decimal(str(item))
        # find best-fitting bin
        best_bin = bin_tree.find_best_fit(item)

        if best_bin is None:
            # no fit -> open a new bin
            new_bin_val = BestFit_Val(remain_c=bin_capacity - item, best_remain_c=bin_capacity - item)
            bin_tree.insert(index, new_bin_val, bin_tree.get_random_rank())
            assignment[i] = index

            new_bin_free_space = bin_capacity - item
            free_space.append(float(new_bin_free_space))

            index += 1
        else:
            # place into existing bin
            assignment[i] = best_bin.key
            best_bin.val.remain_c -= item
            free_space[best_bin.key] = float(best_bin.val.remain_c)
            bin_tree.update_tree(best_bin.key)
            


def best_fit_decreasing(items: list[float], assignment: list[int], free_space: list[float]):
    sorted_items = sorted(items, reverse=True)
    best_fit(sorted_items, assignment, free_space)
