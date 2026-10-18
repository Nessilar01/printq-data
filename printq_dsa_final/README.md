# 3D Printing Job Queue Manager: code and results (Group Mekkhram)

The six DSA algorithms (Merge Sort, Linear Search, Frequency Count, Search-for-Minimum,
Manual Insert, Manual Delete) are in `core/queue_engine.py`. They are the same files the
full web app uses (github.com/Nessilar01/printq-acpapp). This ZIP runs them on CSV files,
with no database and no packages beyond the standard library.

    python dsa_demo.py          # quote, assign, report, search, cancel, re-sort, run the farm
    python bench.py             # Merge Sort comparisons and insert/delete timings
    python -m pytest tests      # 13 unit tests (pip install pytest)

Files
- core/            queue_engine.py, pricing.py, constants.py (copies from the web app, comments and docstrings removed)
- tests/           test_queue_engine.py
- sample_data/     sample_jobs.csv (20 jobs), printers.csv (6 printers)
- output/          demo_output.txt, bench_output.txt, test_output.txt, results.json, bench.json

Needs Python 3.10 or newer.
