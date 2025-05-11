# explanations for member functions are provided in requirements.py
# each file that uses a Zip Tree should import it from this file

from __future__ import annotations
from dataclasses import dataclass

import math
import random
from typing import Optional, TypeVar, Generic, Tuple
from dataclasses import dataclass

KeyType = TypeVar('KeyType')
ValType = TypeVar('ValType')

@dataclass
class Rank:
    geometric_rank: int
    uniform_rank: int

class ZipZipTree(Generic[KeyType, ValType]):
    class _Node:
        def __init__(self, key: KeyType, val: ValType, rank: Rank):
            self.key = key
            self.val = val
            self.rank = rank
            self.left: Optional[ZipZipTree._Node] = None
            self.right: Optional[ZipZipTree._Node] = None

    def __init__(self, capacity: int):
        self.root: Optional[ZipZipTree._Node] = None
        self._size = 0
        self.capacity = capacity

    def get_random_rank(self) -> Rank:
        # get_random_rank(): returns a random node rank, chosen independently from:
#           a geometric distribution of mean 1 and,
#           a uniform distribution of integers from 0 to log(capacity)^3 - 1 (log capacity cubed minus 1).
        # geometric distribution p=1/2
        g = 0
        while random.random() < 0.5:
            g += 1
        # compute uniform bound per call
        max_r = int(math.log(self.capacity) ** 3) - 1
        upper = max(0, max_r)
        u = random.randint(0, upper)
        return Rank(g, u)

    def insert(self, key: KeyType, val: ValType, rank: Rank = None):
        # insert(): inserts item with parameter key, value, and rank into tree.
#           if rank is not provided, a random rank should be selected by using get_random_rank().
        if rank is None:
            rank = self.get_random_rank()
        x = ZipZipTree._Node(key, val, rank)
        # Phase 1: climb until heap order ok
        cur = self.root
        prev = None
        while cur is not None and (
            (x.rank.geometric_rank, x.rank.uniform_rank) < (cur.rank.geometric_rank, cur.rank.uniform_rank)
            or ((x.rank.geometric_rank, x.rank.uniform_rank) == (cur.rank.geometric_rank, cur.rank.uniform_rank)
                and x.key < cur.key)
        ):
     
            prev = cur
            cur = cur.left if x.key < cur.key else cur.right
        # attach x
        if prev is None:
            self.root = x
        elif x.key < prev.key:
            prev.left = x
        else:
            prev.right = x
        # if leaf, done
        if cur is None:
            x.left = x.right = None
            self._size += 1
            return
        # splice subtree
        if x.key < cur.key:
            x.left = cur.left
            x.right = cur
            cur.left = None
        else:
            x.right = cur.right
            x.left = cur
            cur.right = None
        # Phase 2: zip-adjust
        prev = x
        while True:
            fix = prev
            if cur is None:
                break
            if cur.key < x.key:
                # move right
                while cur is not None and cur.key < x.key:
                    prev = cur
                    cur = cur.right
            else:
                # move left
                while cur is not None and cur.key > x.key:
                    prev = cur
                    cur = cur.left
            if cur is None:
                # reattach
                if prev.key < x.key:
                    prev.right = None
                else:
                    prev.left = None
                break
            # reattach cur under fix
            if fix.key < x.key:
                fix.right = cur
            else:
                fix.left = cur
        self._size += 1

    def remove(self, key: KeyType):
        # remove(): removes item with parameter key from tree.
#           you can assume that the item exists in the tree.
        # find node x and its parent
        cur = self.root
        prev = None
        while cur is not None and cur.key != key:
            prev = cur
            cur = cur.left if key < cur.key else cur.right
        if cur is None:
            return  # or raise
        left, right = cur.left, cur.right
        # empty one side
        if left is None or right is None:
            child = left if right is None else right
            if prev is None:
                self.root = child
            elif cur.key < prev.key:
                prev.left = child
            else:
                prev.right = child
        else:
            # zip-merge left and right
            a, b = left, right
            merge_root = None
            # find root of merge
            if (a.rank.geometric_rank, a.rank.uniform_rank) < (b.rank.geometric_rank, b.rank.uniform_rank) \
            or ((a.rank.geometric_rank, a.rank.uniform_rank) == (b.rank.geometric_rank, b.rank.uniform_rank)
        and a.key < b.key):
                merge_root = a
            else:
                merge_root = b

            if merge_root is a:
                # attach b into a.right
                cur_a = a
                while cur_a.right is not None and (
                    (cur_a.right.rank.geometric_rank, cur_a.right.rank.uniform_rank) <
                    (b.rank.geometric_rank, b.rank.uniform_rank)
                ):
                    cur_a = cur_a.right
                cur_a.right = b
            else:
                # attach a into b.left
                cur_b = b
                while cur_b.left is not None and (
                    (cur_b.left.rank.geometric_rank, cur_b.left.rank.uniform_rank) <=
                    (a.rank.geometric_rank, a.rank.uniform_rank)
                ):
                    cur_b = cur_b.left
                cur_b.left = a
            # attach merge_root
            if prev is None:
                self.root = merge_root
            elif key < prev.key:
                prev.left = merge_root
            else:
                prev.right = merge_root
        self._size -= 1

    def find(self, key: KeyType) -> ValType:
        # find(): returns the value of item with parameter key.
#         you can assume that the item exists in the tree.
        cur = self.root
        while cur is not None:
            if key == cur.key:
                return cur.val
            cur = cur.left if key < cur.key else cur.right
       

    def get_size(self) -> int:
        # get_size(): returns the number of nodes in the tree.
        return self._size

    def get_height(self) -> int:
        def _h(n):
            return -1 if n is None else 1 + max(_h(n.left), _h(n.right))
        return _h(self.root)

    def get_depth(self, key: KeyType) -> int:
        cur = self.root
        depth = 0
        while cur is not None:
            if key == cur.key:
                return depth
            elif key < cur.key:
                cur = cur.left
            else:
                cur = cur.right
            depth += 1
        raise KeyError(f"Key {key} not found")

       