"""
Tests for src/exercises/high_order_function_generation_exercise.py

Covers `count` and `average` with lists, generators and edge cases.
The test ensures the `src` package is importable by inserting it into sys.path
when pytest does not already configure it.
"""

import pytest

from exercises.high_order_function_generation_exercise import average, count


def test_count_with_range_and_predicate():
    # Count even numbers in 0..9 -> 5 evens
    evens = count(lambda x: x % 2 == 0, range(10))
    assert evens == 5

    # Count strings with length > 3
    words = ("a", "abcd", "xyz", "hello", "")
    assert count(lambda s: len(s) > 3, words) == 2


def test_average_with_list_of_floats_and_ints():
    assert average([1.0, 2.0, 3.0]) == pytest.approx(2.0)
    # integers accepted too
    assert average([1, 2, 3, 4]) == pytest.approx(2.5)


def test_average_with_generator():
    # generator producing 0, 0.5, 1, 1.5 -> average 0.75
    gen = (x / 2 for x in range(4))
    assert average(gen) == pytest.approx(0.75)


def test_average_raises_on_empty_iterable():
    # empty list
    with pytest.raises(ValueError):
        average([])
    # empty generator
    with pytest.raises(ValueError):
        average((x for x in []))


def test_count_works_with_consumable_iterators():
    # verify count works with a generator (consumes it)
    g = (i for i in range(6))  # 0..5 -> 6 items, 3 are > 2
    result = count(lambda x: x > 2, g)
    assert result == 3
    # generator is now exhausted; counting again yields 0
    assert count(lambda x: True, g) == 0
