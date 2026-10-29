"""A max-heap built from scratch (0-based array), plus heap sort."""


class MaxHeap:
    """Binary max-heap stored in a Python list.

    parent(i) = (i - 1) // 2, left(i) = 2i + 1, right(i) = 2i + 2
    """

    def __init__(self, items=None):
        self.data = []
        if items is not None:
            self.build_max_heap(items)

    def __len__(self):
        return len(self.data)

    def is_empty(self):
        return not self.data

    def peek(self):
        """Return the largest item without removing it. O(1)."""
        if not self.data:
            raise IndexError("peek from an empty heap")
        return self.data[0]

    def insert(self, item):
        """INSERT: add at the end, then sift up. O(log n)."""
        self.data.append(item)
        self._sift_up(len(self.data) - 1)

    def extract_max(self):
        """EXTRACT-MAX: remove and return the largest item. O(log n)."""
        if not self.data:
            raise IndexError("extract_max from an empty heap")
        top = self.data[0]
        last = self.data.pop()
        if self.data:
            self.data[0] = last
            self._max_heapify(0)
        return top

    def build_max_heap(self, items):
        """BUILD-MAX-HEAP: heapify an arbitrary list in O(n)."""
        self.data = list(items)
        for i in range(len(self.data) // 2 - 1, -1, -1):
            self._max_heapify(i)

    def _sift_up(self, i):
        data = self.data
        while i > 0:
            parent = (i - 1) // 2
            if data[parent] >= data[i]:
                break
            data[parent], data[i] = data[i], data[parent]
            i = parent

    def _max_heapify(self, i, size=None):
        """Sift item i down until the max-heap property holds below it."""
        data = self.data
        n = len(data) if size is None else size
        while True:
            left, right = 2 * i + 1, 2 * i + 2
            largest = i
            if left < n and data[left] > data[largest]:
                largest = left
            if right < n and data[right] > data[largest]:
                largest = right
            if largest == i:
                return
            data[i], data[largest] = data[largest], data[i]
            i = largest

    def is_valid(self):
        """Check the max-heap property for every parent/child pair."""
        return all(self.data[(i - 1) // 2] >= self.data[i] for i in range(1, len(self.data)))


def heap_sort(items):
    """Return a sorted (ascending) copy of items using heap sort. O(n log n)."""
    heap = MaxHeap(items)
    data = heap.data
    for end in range(len(data) - 1, 0, -1):
        data[0], data[end] = data[end], data[0]  # move current max to its final place
        heap._max_heapify(0, end)                 # restore heap on the shrunk prefix
    return data
