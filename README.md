# Task Scheduler with a Max-Heap

Mini project for CS314 *Heap Sort*. It builds a max-heap from scratch, uses it for an OS-style priority
scheduler (INSERT and EXTRACT-MAX), and measures it against simpler priority-queue strategies.

## Files
| File | What it is |
|---|---|
| `max_heap.py` | Max-heap (INSERT, EXTRACT-MAX, BUILD-MAX-HEAP, MAX-HEAPIFY) and heap sort |
| `scheduler.py` | `Task` and `Scheduler` classes, plus a demo (`python scheduler.py`) |
| `test_heap.py` | 15 unit tests |
| `benchmark.py` | Runs both experiments, writes the CSV files and plots |
| `results.csv`, `build_results.csv` | Raw timings |
| `queue_plot.png`, `build_plot.png` | Figures |
| `report.pdf` | 2-page report |
| `reflection.md` | What surprised me and what I would do next |
| `DEMO.md` | Script for the 5-minute demo |

## How to run
```
pip install matplotlib
python -m unittest -v      # tests
python scheduler.py        # scheduler demo
python benchmark.py        # experiments (about 30 seconds)
```

## How the scheduler works
Each task has a name, a priority (bigger = more important) and a duration. The scheduler stores
`(priority, -arrival_number, task)` in the max-heap, so the most important task always comes out first and
tasks with equal priority run first-come-first-served.

## Key results
| n tasks | our heap | unsorted list | sorted list | `heapq` (C) |
|---|---|---|---|---|
| 10,000 | 21.6 ms | 819.7 ms | 6.9 ms | 3.3 ms |
| 30,000 | 82.1 ms | 7.89 s | 59.1 ms | 15.0 ms |
| 100,000 | 408.8 ms | skipped (quadratic) | 556.8 ms | 63.4 ms |

- The unsorted list is quadratic: about 96x slower than the heap at n = 30,000.
- The sorted list beats our heap for small n, but loses at n = 100,000.
- Building a heap with BUILD-MAX-HEAP is 7x faster than inserting ascending data one by one (n = 300,000).

Times depend on the machine, but the shape of the curves does not.
