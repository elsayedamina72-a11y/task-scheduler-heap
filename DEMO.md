# 5-minute demo script

**0:00 - Goal (30 s).** "A scheduler must always run the most important task next. I built a max-heap from scratch and used it as a priority queue."

**0:30 - Heap code (1 min).** Open `max_heap.py`. Show the index formulas, INSERT (sift up) and EXTRACT-MAX (MAX-HEAPIFY down). Mention BUILD-MAX-HEAP is O(n).

**1:30 - Scheduler (1 min).** Run `python scheduler.py`. Point out the urgent tasks run first and equal priorities keep their arrival order.

**2:30 - Tests (30 s).** Run `python -m unittest -v` and show the 15 passing tests.

**3:00 - Experiments (1 min 30 s).** Run `python benchmark.py`, then open `queue_plot.png`. Say: the unsorted list is the steepest (quadratic), the heap grows like n log n, `heapq` is fastest because it is written in C, and a sorted list wins only for small n.

**4:30 - Conclusion (30 s).** A heap gives O(log n) INSERT and EXTRACT-MAX. Next steps: preemption and priority aging.

Tip: record your screen while you follow these steps.
