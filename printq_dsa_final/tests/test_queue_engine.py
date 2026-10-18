import random
from types import SimpleNamespace

import pytest

from core.queue_engine import (
    frequency_count, linear_search, linear_search_by, linear_search_contains, manual_delete, manual_insert,
    merge_sort, search_for_minimum,
)


def job(name="a.stl", minutes=10, material="PLA", ident=0):
    return SimpleNamespace(id=ident, file_name=name, duration_min=minutes, material=material)


def test_merge_sort_orders_by_duration():
    jobs = [job(minutes=m, ident=i) for i, m in enumerate([50, 5, 30, 5, 120, 1])]
    assert [j.duration_min for j in merge_sort(jobs)] == [1, 5, 5, 30, 50, 120]


def test_merge_sort_is_stable_for_equal_durations():
    jobs = [job(minutes=10, ident=1), job(minutes=5, ident=2), job(minutes=10, ident=3), job(minutes=5, ident=4)]
    assert [j.id for j in merge_sort(jobs)] == [2, 4, 1, 3]


def test_merge_sort_does_not_mutate_input_and_handles_edges():
    original = [job(minutes=3), job(minutes=1)]
    merge_sort(original)
    assert [j.duration_min for j in original] == [3, 1]
    assert merge_sort([]) == []
    assert len(merge_sort([job()])) == 1


def test_merge_sort_matches_python_sorted_on_random_data():
    rng = random.Random(1)
    for _ in range(200):
        jobs = [job(minutes=rng.randint(1, 50), ident=i) for i in range(rng.randint(0, 40))]
        assert merge_sort(jobs) == sorted(jobs, key=lambda j: j.duration_min)


def test_linear_search_finds_first_match_case_insensitive():
    jobs = [job("Gear.stl"), job("vase.stl"), job("gear.STL")]
    assert linear_search(jobs, "GEAR.stl") == 0
    assert linear_search(jobs, "vase.stl") == 1
    assert linear_search(jobs, "gear.stl", ignore_case=False) == -1
    assert linear_search(jobs, "missing.stl") == -1
    assert linear_search([], "x") == -1


def test_linear_search_contains_and_by_predicate():
    jobs = [job("phone_stand.stl", ident=1), job("gear.stl", ident=2), job("PHONE_case.stl", ident=3)]
    assert linear_search_contains(jobs, "phone") == [0, 2]
    assert linear_search_contains(jobs, "zzz") == []
    assert linear_search_by(jobs, lambda j: j.id == 2) == 1
    assert linear_search_by(jobs, lambda j: j.id == 99) == -1


def test_frequency_count_reports_zero_for_unused_materials():
    jobs = [job(material="PLA"), job(material="PLA"), job(material="ABS")]
    assert frequency_count(jobs) == {"PLA": 2, "PETG": 0, "ABS": 1}
    assert frequency_count([]) == {"PLA": 0, "PETG": 0, "ABS": 0}


def test_frequency_count_with_custom_key():
    assert frequency_count(["a", "b", "a"], key=lambda s: s, categories=["a", "b", "c"]) == {"a": 2, "b": 1, "c": 0}


def test_search_for_minimum_returns_first_minimum_on_ties():
    assert search_for_minimum([30, 10, 20]) == 1
    assert search_for_minimum([5, 5, 9]) == 0
    assert search_for_minimum([7]) == 0
    with pytest.raises(ValueError):
        search_for_minimum([])


def test_manual_insert_keeps_order_and_places_ties_after_equals():
    queue = [job(minutes=10, ident=1), job(minutes=20, ident=2), job(minutes=30, ident=3)]
    assert manual_insert(queue, job(minutes=20, ident=4)) == 2
    assert manual_insert(queue, job(minutes=5, ident=5)) == 0
    assert manual_insert(queue, job(minutes=99, ident=6)) == len(queue) - 1
    assert [j.id for j in queue] == [5, 1, 2, 4, 3, 6]


def test_manual_insert_into_empty_queue():
    queue = []
    assert manual_insert(queue, job(minutes=7)) == 0 and len(queue) == 1


def test_manual_delete_shifts_left_and_validates_index():
    queue = [job(ident=i) for i in range(4)]
    removed = manual_delete(queue, 1)
    assert removed.id == 1 and [j.id for j in queue] == [0, 2, 3]
    assert manual_delete(queue, 2).id == 3 and manual_delete(queue, 0).id == 0
    for bad in (-1, 5):
        with pytest.raises(IndexError):
            manual_delete(queue, bad)


def test_random_insert_delete_sequence_stays_sorted():
    rng = random.Random(9)
    queue: list = []
    for i in range(300):
        if queue and rng.random() < 0.35:
            manual_delete(queue, rng.randrange(len(queue)))
        else:
            manual_insert(queue, job(minutes=rng.randint(1, 60), ident=i))
        assert [j.duration_min for j in queue] == sorted(j.duration_min for j in queue)
