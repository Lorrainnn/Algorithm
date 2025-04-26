import random

# Node class for Skip List
class SkipListNode:
    def __init__(self, value, level):
        self.value = value
        self.forward = [None] * (level + 1)

# Skip List class
class SkipList:
    MAX_LEVEL = 16  # Maximum level for this skip list
    P = 0.5         # Probability for random level generation

    def __init__(self):
        self.header = SkipListNode(None, self.MAX_LEVEL)
        self.level = 0

    def random_level(self):
        lvl = 0
        while random.random() < self.P and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, value):
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.header

        for i in reversed(range(self.level + 1)):
            while current.forward[i] and current.forward[i].value < value:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current is None or current.value != value:
            rlevel = self.random_level()

            if rlevel > self.level:
                for i in range(self.level + 1, rlevel + 1):
                    update[i] = self.header
                self.level = rlevel

            new_node = SkipListNode(value, rlevel)
            for i in range(rlevel + 1):
                new_node.forward[i] = update[i].forward[i]
                update[i].forward[i] = new_node

    def traverse(self):
        result = []
        current = self.header.forward[0]
        while current:
            result.append(current.value)
            current = current.forward[0]
        return result

# Skip-List Sort: Insert all elements, then traverse
def skip_list_sort(arr):
    sl = SkipList()
    for val in arr:
        sl.insert(val)
    sorted_arr = sl.traverse()
    for i in range(len(arr)):
        arr[i] = sorted_arr[i]

# Example usage
if __name__ == "__main__":
    data = [random.randint(1, 100) for _ in range(10)]
    print("Before:", data)
    skip_list_sort(data)
    print("After: ", data)
