from collections.abc import Callable, Sequence
from typing import Any, TypeVar

from core.constants import MATERIALS

T = TypeVar("T")


def by_duration(job: Any) -> int:
    return job.duration_min


def merge_sort(items: Sequence[T], key: Callable[[T], Any] = by_duration) -> list[T]:
    n = len(items)
    if n <= 1:
        return list(items)
    mid = n // 2
    left = merge_sort(items[:mid], key)
    right = merge_sort(items[mid:], key)
    return _merge(left, right, key)


def _merge(left: list[T], right: list[T], key: Callable[[T], Any]) -> list[T]:
    out: list[T] = []
    i = j = 0
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            out.append(left[i])
            i += 1
        else:
            out.append(right[j])
            j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out


def linear_search(items: Sequence[Any], name: str, *, ignore_case: bool = True) -> int:
    target = name.lower() if ignore_case else name
    for index in range(len(items)):
        candidate = items[index].file_name
        if (candidate.lower() if ignore_case else candidate) == target:
            return index
    return -1


def linear_search_contains(items: Sequence[Any], needle: str) -> list[int]:
    needle = needle.lower()
    return [i for i in range(len(items)) if needle in items[i].file_name.lower()]


def linear_search_by(items: Sequence[T], predicate: Callable[[T], bool]) -> int:
    for index in range(len(items)):
        if predicate(items[index]):
            return index
    return -1


def frequency_count(
    items: Sequence[Any],
    key: Callable[[Any], str] = lambda job: job.material,
    categories: Sequence[str] = MATERIALS,
) -> dict[str, int]:
    tally = {category: 0 for category in categories}
    for item in items:
        k = key(item)
        tally[k] = tally.get(k, 0) + 1
    return tally


def search_for_minimum(values: Sequence[int]) -> int:
    if len(values) == 0:
        raise ValueError("search_for_minimum needs at least one value")
    best_index = 0
    for index in range(1, len(values)):
        if values[index] < values[best_index]:
            best_index = index
    return best_index


def manual_insert(items: list[T], new_item: T, key: Callable[[T], Any] = by_duration) -> int:
    position = len(items)
    for index in range(len(items)):
        if key(items[index]) > key(new_item):
            position = index
            break

    items.append(new_item)
    for index in range(len(items) - 1, position, -1):
        items[index] = items[index - 1]

    items[position] = new_item
    return position


def manual_delete(items: list[T], index: int) -> T:
    if index < 0 or index >= len(items):
        raise IndexError("queue index out of range")
    removed = items[index]

    for i in range(index, len(items) - 1):
        items[i] = items[i + 1]

    del items[-1]
    return removed
