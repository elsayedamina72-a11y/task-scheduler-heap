"""Task Scheduler: an OS-style scheduler that always runs the highest-priority task first."""
from dataclasses import dataclass

from max_heap import MaxHeap


@dataclass
class Task:
    name: str
    priority: int   # bigger number = more important
    duration: int   # how long the task runs (time units)


class Scheduler:
    """Priority scheduler on top of a max-heap.

    Heap entries are (priority, -arrival_number, task). The arrival number is unique, so ties on
    priority are served first-come-first-served and Task objects are never compared.
    """

    def __init__(self):
        self._heap = MaxHeap()
        self._arrivals = 0

    def __len__(self):
        return len(self._heap)

    def add(self, task):
        """INSERT a task. O(log n)."""
        self._heap.insert((task.priority, -self._arrivals, task))
        self._arrivals += 1

    def next_task(self):
        """EXTRACT-MAX: remove and return the highest-priority task. O(log n)."""
        return self._heap.extract_max()[2]

    def run_all(self):
        """Run every task to completion (non-preemptive).

        Returns a list of (task, start_time, finish_time) in execution order.
        """
        clock = 0
        schedule = []
        while len(self) > 0:
            task = self.next_task()
            schedule.append((task, clock, clock + task.duration))
            clock += task.duration
        return schedule


def average_wait(schedule):
    """Average time tasks waited before starting (all tasks arrive at time 0)."""
    return sum(start for _, start, _ in schedule) / len(schedule)


if __name__ == "__main__":
    tasks = [
        Task("backup", 2, 8),
        Task("email sync", 3, 2),
        Task("system update", 1, 10),
        Task("video call", 9, 4),
        Task("virus scan", 4, 6),
        Task("print report", 3, 3),
        Task("kernel interrupt", 10, 1),
    ]

    sched = Scheduler()
    for t in tasks:
        sched.add(t)
    result = sched.run_all()

    print(f"{'order':<6}{'task':<18}{'priority':>9}{'duration':>10}{'start':>7}{'finish':>8}")
    for i, (t, start, finish) in enumerate(result, 1):
        print(f"{i:<6}{t.name:<18}{t.priority:>9}{t.duration:>10}{start:>7}{finish:>8}")

    # Compare with plain first-come-first-served order
    clock, fcfs_waits = 0, []
    for t in tasks:
        fcfs_waits.append(clock)
        clock += t.duration
    print(f"\nAverage wait, priority scheduler : {average_wait(result):.2f}")
    print(f"Average wait, first-come-first-served: {sum(fcfs_waits) / len(fcfs_waits):.2f}")
    high = [start for t, start, _ in result if t.priority >= 9]
    print(f"Start times of the 2 most urgent tasks: {high} (they run first)")
