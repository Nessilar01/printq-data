import csv
import json
import os
from types import SimpleNamespace

from core.pricing import quote_price
from core.queue_engine import (
    frequency_count, linear_search, manual_delete, manual_insert, merge_sort, search_for_minimum,
)

HERE = os.path.dirname(os.path.abspath(__file__))


def load_printers(path):
    printers = []
    with open(path, newline="") as f:
        for row in csv.DictReader(f):
            printers.append(SimpleNamespace(name=row["printer"], remaining=int(row["remaining_min"]), queue=[]))
    return printers


def load_jobs(path):
    jobs = []
    with open(path, newline="") as f:
        for i, row in enumerate(csv.DictReader(f), start=1):
            jobs.append(SimpleNamespace(
                id=i, file_name=row["file_name"], material=row["material"],
                duration_min=int(row["duration_min"]), price=0, printer=None,
            ))
    return jobs


def backlog(printer):
    total = printer.remaining
    for job in printer.queue:
        total += job.duration_min
    return total


def show_board(printers, title):
    print(f"\n{title}")
    for p in printers:
        names = ", ".join(f"{j.file_name} ({j.duration_min})" for j in p.queue) or "-"
        print(f"  {p.name}  running {p.remaining:>3} min left | backlog {backlog(p):>4} | {names}")


def main():
    printers = load_printers(os.path.join(HERE, "sample_data", "printers.csv"))
    jobs = load_jobs(os.path.join(HERE, "sample_data", "sample_jobs.csv"))
    results = {}

    print("STEP 1  Quote every job   price = duration x 3 THB + material surcharge")
    for job in jobs:
        job.price = quote_price(job.duration_min, job.material)
    for job in jobs[:4]:
        print(f"  {job.file_name:<15} {job.duration_min:>3} min {job.material:<4} -> {job.price} THB")
    print(f"  ... {len(jobs)} jobs, total {sum(j.price for j in jobs)} THB")

    print("\nSTEP 2  Assign each job: Search-for-Minimum picks the printer, Manual Insert places it")
    for job in jobs:
        loads = [backlog(p) for p in printers]
        best = search_for_minimum(loads)
        position = manual_insert(printers[best].queue, job)
        job.printer = printers[best].name
        print(f"  {job.file_name:<15} loads={loads} -> {printers[best].name}, queue slot {position + 1}")
    show_board(printers, "Queue board after all 20 orders (each queue is shortest-job-first):")

    print("\nSTEP 3  Material report (Frequency Count)")
    counts = frequency_count(jobs)
    revenue = {m: sum(j.price for j in jobs if j.material == m) for m in counts}
    for m in counts:
        print(f"  {m:<5} {counts[m]:>2} jobs   {revenue[m]:>5} THB")
    results["material_counts"] = counts
    results["material_revenue"] = revenue

    print("\nSTEP 4  Search by name (Linear Search), then cancel with Manual Delete")
    for target in ("ATREX_Mount", "Camera_Mount", "No_Such_File"):
        hit = None
        for p in printers:
            idx = linear_search(p.queue, target)
            if idx >= 0:
                hit = (p, idx)
                break
        print(f"  search {target!r:<16} -> " + (f"{hit[0].name}, index {hit[1]}" if hit else "-1 (not found)"))
        if hit and target == "Camera_Mount":
            removed = manual_delete(hit[0].queue, hit[1])
            print(f"  cancelled {removed.file_name} ({removed.duration_min} min) from {hit[0].name}; queue closed up")
            jobs = [j for j in jobs if j is not removed]

    print("\nSTEP 5  Owner re-slices Lidar_Plate (60 -> 150 min): queue is rebuilt with Merge Sort")
    for p in printers:
        idx = linear_search(p.queue, "Lidar_Plate")
        if idx >= 0:
            before = [j.duration_min for j in p.queue]
            p.queue[idx].duration_min = 150
            p.queue = merge_sort(p.queue)
            print(f"  {p.name} before {before}")
            print(f"  {p.name} after  {[j.duration_min for j in p.queue]}")
    for job in jobs:
        job.price = quote_price(job.duration_min, job.material)

    print("\nSTEP 6  Run the farm to completion (the head of a queue is removed with Manual Delete)")
    schedule = []
    sjf_waits = {}
    for p in printers:
        clock = p.remaining

        arrival_order = [j for j in jobs if j.printer == p.name]
        while len(p.queue) > 0:
            job = manual_delete(p.queue, 0)
            schedule.append(dict(printer=p.name, job=job.file_name, material=job.material,
                                 start=clock, end=clock + job.duration_min))
            sjf_waits[job.id] = clock
            clock += job.duration_min
        p.finish = clock

        fifo_clock = p.remaining
        for job in arrival_order:
            job.fifo_wait = fifo_clock
            fifo_clock += job.duration_min
    n = len(jobs)
    sjf_avg = sum(sjf_waits.values()) / n
    fifo_avg = sum(j.fifo_wait for j in jobs) / n
    sjf_max = max(sjf_waits.values())
    fifo_max = max(j.fifo_wait for j in jobs)
    longest = max(jobs, key=lambda j: j.duration_min)
    for p in printers:
        print(f"  {p.name} finishes at minute {p.finish}")
    print(f"  farm makespan: {max(p.finish for p in printers)} min")
    print(f"  average wait before start  SJF: {sjf_avg:.1f} min   FIFO: {fifo_avg:.1f} min")
    print(f"  longest wait               SJF: {sjf_max} min   FIFO: {fifo_max} min")
    print(f"  longest job {longest.file_name} ({longest.duration_min} min) waits SJF {sjf_waits[longest.id]} min / FIFO {longest.fifo_wait} min")

    results.update(
        printers=[dict(name=p.name, remaining=p.remaining, finish=p.finish) for p in printers],
        schedule=schedule,
        sjf_avg_wait=round(sjf_avg, 1), fifo_avg_wait=round(fifo_avg, 1),
        sjf_max_wait=sjf_max, fifo_max_wait=fifo_max,
        makespan=max(p.finish for p in printers),
        jobs_printed=n, total_price=sum(j.price for j in jobs),
        longest_job=dict(name=longest.file_name, duration=longest.duration_min,
                         sjf_wait=sjf_waits[longest.id], fifo_wait=longest.fifo_wait),
    )
    os.makedirs(os.path.join(HERE, "output"), exist_ok=True)
    with open(os.path.join(HERE, "output", "results.json"), "w") as f:
        json.dump(results, f, indent=1)


if __name__ == "__main__":
    main()
