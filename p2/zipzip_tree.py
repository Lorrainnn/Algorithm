# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file

from __future__ import annotations

from typing import TypeVar, Optional
from dataclasses import dataclass

import math, random

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

@dataclass(order=True)
class Rank:
    #first geo then uni
    geometric_rank: int
    uniform_rank: int

class Node:
    def __init__(self, key: KeyType, val: ValType, rank: Rank):
        self.key = key
        self.val = val
        self.rank = rank
        self.left: Optional[Node] = None
        self.right: Optional[Node] = None
    
    def __lt__(self, other: Node) -> bool:
        if self.rank != other.rank:
            return self.rank < other.rank
        return self.key < other.key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Node):
            return NotImplemented
        return self.rank == other.rank and self.key == other.key

class ZipZipTree:
    # ZipZipTree(): constructs the zip-zip tree with a specific capacity.
    def __init__(self, capacity: int):
        self.root: Optional[Node] = None
        self.capacity = capacity
        self.size = 0

    def get_random_rank(self) -> Rank:
        # get_random_rank(): returns a random node rank, chosen independently from:
#           a geometric distribution of mean 1 and,
#           a uniform distribution of integers from 0 to log(capacity)^3 - 1 (log capacity cubed minus 1).

        # Geometric ---> mean = 1
        count = 0
        while random.random() < 0.5:
            count += 1
        # Uniform rank
        uniform = random.randint(0, max(0, int(math.log2(self.capacity) ** 3) - 1))
        return Rank(count, uniform)
    
    def best_fit(self, size: float) -> Optional[Node]:
        """Return node whose remaining_capacity >= size but is minimal among those."""
        best: Optional[Node] = None
        def dfs(node: Optional[Node]):
            nonlocal best
            if node is None:
                return
            cap = getattr(node.val, 'remaining_capacity', None)
            if cap is not None and cap >= size:
                if best is None or cap < getattr(best.val, 'remaining_capacity'):
                    best = node
            dfs(node.left)
            dfs(node.right)
        dfs(self.root)
        return best


    #recheck Pseudocode code.. ok
    def insert(self, key: KeyType, val: ValType, rank: Rank = None):
        # insert(): inserts item with parameter key, value, and rank into tree.
#           if rank is not provided, a random rank should be selected by using get_random_rank().
        if rank is None:
            rank = self.get_random_rank()

        new_node = Node(key, val, rank)
        cur = self.root
        prev = None

        
        # Find where to insert --> find node with just higher ranking
        while cur is not None and (
            rank.geometric_rank < cur.rank.geometric_rank
            or (rank.geometric_rank == cur.rank.geometric_rank and rank.uniform_rank < cur.rank.uniform_rank)
            or (rank.geometric_rank == cur.rank.geometric_rank and rank.uniform_rank == cur.rank.uniform_rank and key > cur.key)
        ):
            prev = cur
            if key < cur.key:
                cur = cur.left
            else:
                cur = cur.right

        if prev is None:
            #highest ranking -> should be used as root
            self.root = new_node
        elif new_node.key < prev.key:
            prev.left = new_node
        else:
            prev.right = new_node

        # no push subtree
        if cur is None:
            new_node.left = new_node.right = None
            self.size += 1
            return

        # push subtree
        if key < cur.key:
            new_node.right = cur
        else:
            new_node.left = cur

        prev = new_node

        #Second phase: Reattach (recheck paper)
        while cur is not None:
            fix = prev

            #right find
            if cur.key < key:
                #repeat prev<-cur;cur<-cur.right
                while cur is not None and cur.key <= key:
                    prev = cur
                    cur = cur.right
            #left find
            else:
                while cur is not None and cur.key >= key:
                    #repeat prev<-cur;cur<-cur.left
                    prev = cur
                    cur = cur.left      
            if fix.key > key or (fix.key == new_node.key and prev.key > key):
                fix.left = cur
            else:
                fix.right = cur

        self.size += 1

    def remove(self, key: KeyType):
        # remove(): removes item with parameter key from tree.
#           you can assume that the item exists in the tree.
        if self.root is None:
            return

        cur = self.root
        prev = None

        # find delete node 
        while cur is not None and key != cur.key:
            prev = cur
            if key < cur.key:
                cur = cur.left 
            else:
                cur = cur.right
        #not exist
        if cur is None:
            return  
        #exist
        left = cur.left
        right = cur.right

    
        if left is None:
            cur = right
        elif right is None:
            cur = left
        elif left>right:
            cur = left
        else:
            cur = right

        # update parent's node
        if self.root.key == key:
            self.root = cur
        elif key < prev.key:
            prev.left = cur
        else:
            prev.right = cur

        # zip back
        while left is not None and right is not None:
            if left>right:
                while left is not None and left>right:
                    prev = left
                    left = left.right
                prev.right = right
            else:
                while right is not None and left<right:
                    prev = right
                    right = right.left
                prev.left = left

        self.size -= 1


    def find(self, key: KeyType) -> ValType:
        # find(): returns the value of item with parameter key.
#         you can assume that the item exists in the tree.
        cur = self.root
        while cur is not None:
            if key == cur.key:
                return cur.val
            if key < cur.key:
                #smaller go left
                cur = cur.left 
            else:
                #larger go right
                cur = cur.right
              
        return None

    def get_size(self) -> int:
        # get_size(): returns the number of nodes in the tree.
        return self.size

    def get_height(self) -> int:
        # get_height(): returns the height of the tree.
        return self._get_height_rec(self.root)

    def _get_height_rec(self, node: Optional[Node]) -> int:
        if node is None:
            return -1
        return max(self._get_height_rec(node.left), self._get_height_rec(node.right)) + 1

    def get_depth(self, key: KeyType) -> int:
        # get_depth(): returns the depth of the item with parameter key.
#              you can assume that the item exists in the tree.
        return self._get_depth_rec(self.root, key, 0)

    def _get_depth_rec(self, node: Optional[Node], key: KeyType, depth: int) -> int:
        if node is None:
            return -1
        if key == node.key:
            return depth
        if key < node.key:
            #smaller go left
            return self._get_depth_rec(node.left, key, depth + 1)
        else:
            #larger go right
            return self._get_depth_rec(node.right, key, depth + 1)

	# feel free to define new methods in addition to the above
	# fill in the definitions of each required member function (above),
	# and for any additional member functions you define