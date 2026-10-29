"""Unit tests. Run with:  python -m unittest -v"""
import random
import unittest

from max_heap import MaxHeap, heap_sort
from scheduler import Scheduler, Task, average_wait


class TestMaxHeap(unittest.TestCase):
    def test_empty_heap(self):
        h = MaxHeap()
        self.assertTrue(h.is_empty())
        self.assertEqual(len(h), 0)
        with self.assertRaises(IndexError):
            h.extract_max()
        with self.assertRaises(IndexError):
            h.peek()

    def test_single_item(self):
        h = MaxHeap()
        h.insert(5)
        self.assertEqual(h.peek(), 5)
        self.assertEqual(h.extract_max(), 5)
        self.assertTrue(h.is_empty())

    def test_insert_keeps_heap_property(self):
        h = MaxHeap()
        for x in [3, 9, 1, 7, 7, 5, 12, 0]:
            h.insert(x)
            self.assertTrue(h.is_valid())
        self.assertEqual(h.peek(), 12)

    def test_extract_returns_descending_order(self):
        h = MaxHeap()
        data = [4, 10, 3, 5, 1, 10, 8]
        for x in data:
            h.insert(x)
        out = []
        while not h.is_empty():
            out.append(h.extract_max())
            self.assertTrue(h.is_valid())
        self.assertEqual(out, sorted(data, reverse=True))

    def test_build_max_heap(self):
        rng = random.Random(1)
        data = [rng.randint(-50, 50) for _ in range(100)]
        h = MaxHeap(data)
        self.assertTrue(h.is_valid())
        self.assertEqual(h.peek(), max(data))
        self.assertEqual(len(h), 100)

    def test_textbook_example(self):
        # CLRS example array for BUILD-MAX-HEAP
        h = MaxHeap([4, 1, 3, 2, 16, 9, 10, 14, 8, 7])
        self.assertEqual(h.data, [16, 14, 10, 8, 7, 9, 3, 2, 4, 1])

    def test_random_operations_against_reference(self):
        rng = random.Random(2)
        h, ref = MaxHeap(), []
        for _ in range(2000):
            if ref and rng.random() < 0.4:
                self.assertEqual(h.extract_max(), max(ref))
                ref.remove(max(ref))
            else:
                x = rng.randint(0, 100)
                h.insert(x)
                ref.append(x)
            self.assertEqual(len(h), len(ref))
        self.assertTrue(h.is_valid())


class TestHeapSort(unittest.TestCase):
    def test_matches_sorted(self):
        rng = random.Random(3)
        for _ in range(50):
            data = [rng.randint(-100, 100) for _ in range(rng.randint(0, 150))]
            self.assertEqual(heap_sort(data), sorted(data))

    def test_special_inputs(self):
        for data in ([], [1], [2, 1], list(range(50)), list(range(50, 0, -1)), [5] * 20):
            self.assertEqual(heap_sort(data), sorted(data))

    def test_input_not_modified(self):
        data = [3, 1, 2]
        heap_sort(data)
        self.assertEqual(data, [3, 1, 2])


class TestScheduler(unittest.TestCase):
    def test_runs_highest_priority_first(self):
        s = Scheduler()
        for name, p in [("a", 2), ("b", 9), ("c", 5)]:
            s.add(Task(name, p, 1))
        self.assertEqual([s.next_task().name for _ in range(3)], ["b", "c", "a"])

    def test_equal_priorities_are_first_come_first_served(self):
        s = Scheduler()
        for name in ["first", "second", "third"]:
            s.add(Task(name, 5, 1))
        self.assertEqual([s.next_task().name for _ in range(3)], ["first", "second", "third"])

    def test_empty_scheduler(self):
        with self.assertRaises(IndexError):
            Scheduler().next_task()

    def test_run_all_times(self):
        s = Scheduler()
        s.add(Task("low", 1, 5))
        s.add(Task("high", 9, 3))
        result = s.run_all()
        self.assertEqual([(t.name, a, b) for t, a, b in result], [("high", 0, 3), ("low", 3, 8)])
        self.assertEqual(average_wait(result), 1.5)

    def test_interleaved_add_and_next(self):
        s = Scheduler()
        s.add(Task("a", 1, 1))
        s.add(Task("b", 3, 1))
        self.assertEqual(s.next_task().name, "b")
        s.add(Task("c", 2, 1))
        self.assertEqual(s.next_task().name, "c")
        self.assertEqual(s.next_task().name, "a")


if __name__ == "__main__":
    unittest.main()
