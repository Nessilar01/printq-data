import json
import math
import os
import random
import time
from types import SimpleNamespace

from core.queue_engine import manual_delete, manual_insert, merge_sort

HERE = os.path.dirname(os.path.abspath(__file__))
rng = random.Random(2026)


def make_jobs(n):
    return [SimpleNamespace(file_name=f"j{i}", duration_min=rng.randint(1, 3000), material="PLA") for i in range(n)]


def count_merge_sort_comparisons(jobs):
    calls = 0

    def key(job):
        nonlocal calls
        calls += 1
        return job.duration_min

    merge_sort(jobs, key=key)
    return calls // 2


def time_insert_delete(n, repeat=2000):
    queue = merge_sort(make_jobs(n))
    t_ins = t_del = 0.0
    for _ in range(repeat):
        job = SimpleNamespace(file_name="x", duration_min=rng.randint(1, 3000), material="PLA")
        t0 = time.perf_counter()
        pos = manual_insert(queue, job)
        t1 = time.perf_counter()
        manual_delete(queue, 0)
        t2 = time.perf_counter()
        t_ins += t1 - t0
        t_del += t2 - t1
    return t_ins / repeat * 1e6, t_del / repeat * 1e6


rows = []
print(f"{'n':>6} {'merge-sort compares':>20} {'n*log2(n)':>10} {'insert us':>10} {'delete-head us':>15}")
for n in (100, 200, 400, 800, 1600, 3200, 6400):
    cmp_ = count_merge_sort_comparisons(make_jobs(n))
    ins, dele = time_insert_delete(n)
    rows.append(dict(n=n, compares=cmp_, nlogn=round(n * math.log2(n)), insert_us=round(ins, 1), delete_us=round(dele, 1)))
    print(f"{n:>6} {cmp_:>20} {round(n * math.log2(n)):>10} {ins:>10.1f} {dele:>15.1f}")
os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
with open(os.path.join(HERE, "output", "bench.json"), "w") as f:
    json.dump(rows, f, indent=1)
