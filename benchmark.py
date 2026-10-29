"""Experiments for the Task Scheduler project.

Experiment 1: n INSERTs followed by n EXTRACT-MAXs, using four priority-queue strategies:
  - our MaxHeap (pure Python)          O(log n) per operation
  - unsorted list (scan for the max)   O(1) insert, O(n) extract
  - sorted list (bisect.insort)        O(n) insert, O(1) extract
  - heapq (reference, written in C)
Experiment 2: BUILD-MAX-HEAP (O(n)) vs inserting the items one by one (O(n log n) worst case).

Run:  python benchmark.py      Outputs: results.csv, build_results.csv, queue_plot.png, build_plot.png
"""
import bisect
import csv
import heapq
import random
import time

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from max_heap import MaxHeap

SIZES = [1_000, 3_000, 10_000, 30_000, 100_000]
UNSORTED_MAX_N = 30_000   # O(n^2) total: skipped above this size
random.seed(42)


def run_max_heap(prios):
    h = MaxHeap()
    for p in prios:
        h.insert(p)
    out = [h.extract_max() for _ in range(len(prios))]
    return out


def run_unsorted_list(prios):
    q, out = [], []
    for p in prios:
        q.append(p)
    for _ in range(len(prios)):
        m = max(q)
        i = q.index(m)
        q[i] = q[-1]      # delete by swapping with the last element
        q.pop()
        out.append(m)
    return out


def run_sorted_list(prios):
    q, out = [], []
    for p in prios:
        bisect.insort(q, p)
    for _ in range(len(prios)):
        out.append(q.pop())
    return out


def run_heapq(prios):
    q = []
    for p in prios:
        heapq.heappush(q, -p)
    return [-heapq.heappop(q) for _ in range(len(prios))]


STRATEGIES = {
    "our MaxHeap": run_max_heap,
    "unsorted list": run_unsorted_list,
    "sorted list": run_sorted_list,
    "heapq (C)": run_heapq,
}


def best_time(fn, arg, expected):
    runs = 3 if len(arg) <= 10_000 else 1
    best = float("inf")
    for _ in range(runs):
        t = time.perf_counter()
        out = fn(arg)
        best = min(best, time.perf_counter() - t)
    assert out == expected, f"{fn.__name__} returned a wrong order"
    return best


rows = []
print(f"{'n':>8}" + "".join(f"{name:>16}" for name in STRATEGIES))
for n in SIZES:
    prios = [random.randint(0, 10 * n) for _ in range(n)]
    expected = sorted(prios, reverse=True)
    line = f"{n:>8}"
    for name, fn in STRATEGIES.items():
        if name == "unsorted list" and n > UNSORTED_MAX_N:
            line += f"{'skipped':>16}"
            continue
        t = best_time(fn, prios, expected)
        rows.append({"n": n, "strategy": name, "seconds": t})
        line += f"{t:>16.4f}"
    print(line)

with open("results.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["n", "strategy", "seconds"])
    w.writeheader()
    w.writerows(rows)

# ---- Experiment 2: build vs repeated insert ----
build_rows = []
print(f"\n{'n':>8}{'BUILD-MAX-HEAP':>18}{'n x INSERT':>14}{'INSERT (ascending)':>20}")
for n in [1_000, 10_000, 100_000, 300_000]:
    data = [random.randint(0, 10 * n) for _ in range(n)]
    t = time.perf_counter()
    h1 = MaxHeap(data)
    t_build = time.perf_counter() - t
    t = time.perf_counter()
    h2 = MaxHeap()
    for x in data:
        h2.insert(x)
    t_insert = time.perf_counter() - t
    assert h1.is_valid() and h2.is_valid() and h1.peek() == h2.peek() == max(data)
    # worst case for INSERT: ascending input, every new item sifts all the way to the root
    asc = sorted(data)
    t = time.perf_counter()
    h3 = MaxHeap()
    for x in asc:
        h3.insert(x)
    t_asc = time.perf_counter() - t
    assert h3.is_valid()
    build_rows.append({"n": n, "build_max_heap": t_build, "repeated_insert": t_insert,
                       "insert_ascending": t_asc})
    print(f"{n:>8}{t_build:>18.4f}{t_insert:>14.4f}{t_asc:>20.4f}")

with open("build_results.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=["n", "build_max_heap", "repeated_insert", "insert_ascending"])
    w.writeheader()
    w.writerows(build_rows)

# ---- Plots ----
colors = {"our MaxHeap": "green", "unsorted list": "red", "sorted list": "orange", "heapq (C)": "blue"}
plt.figure(figsize=(8, 5))
for name in STRATEGIES:
    pts = [(r["n"], r["seconds"]) for r in rows if r["strategy"] == name]
    plt.plot([p[0] for p in pts], [p[1] for p in pts], marker="o", label=name, color=colors[name])
plt.xscale("log")
plt.yscale("log")
plt.xlabel("number of tasks n")
plt.ylabel("time for n INSERT + n EXTRACT-MAX (s)")
plt.title("Priority queue strategies")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig("queue_plot.png", dpi=150)
plt.close()

plt.figure(figsize=(7, 4.5))
xs = [r["n"] for r in build_rows]
plt.plot(xs, [r["build_max_heap"] for r in build_rows], marker="o", label="BUILD-MAX-HEAP  O(n)", color="green")
plt.plot(xs, [r["repeated_insert"] for r in build_rows], marker="s", label="n x INSERT, random input", color="orange")
plt.plot(xs, [r["insert_ascending"] for r in build_rows], marker="^", label="n x INSERT, ascending input (worst case)", color="red")
plt.xscale("log")
plt.yscale("log")
plt.xlabel("n")
plt.ylabel("time (s)")
plt.title("Building a heap")
plt.legend()
plt.grid(True, which="both", alpha=0.3)
plt.tight_layout()
plt.savefig("build_plot.png", dpi=150)
plt.close()
print("\nSaved results.csv, build_results.csv, queue_plot.png, build_plot.png")
