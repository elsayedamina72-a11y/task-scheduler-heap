# Reflection

**What surprised me**
- A plain sorted list was faster than my heap for up to 30,000 tasks. Its insert is O(n), but the shifting runs in fast C code. Big-O tells how time grows, not who wins at small sizes.
- Python's `heapq`, which uses the same algorithm, was about 6.5 times faster than my heap. Most of the difference is the interpreter, not the idea.
- Inserting random numbers one by one into a heap was only 1.3 times slower than BUILD-MAX-HEAP, because a random item usually sifts up just a step or two. The O(n) versus O(n log n) gap only appeared on ascending input (7 times).

**What I would do next**
- Add task arrival times and preemption, so a new urgent task can interrupt a running one.
- Add priority aging so low-priority tasks do not wait forever (starvation).
- Add increase-key and decrease-key to change a task's priority while it waits.
