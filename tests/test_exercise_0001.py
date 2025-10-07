import pytest

# Tests for recursive_nested_list_function.py file

from exercises.recursive_nested_list_function import sum_nested_list

def test_sum_nested_list():
    assert sum_nested_list([1, 2, [3, 4], 5]) == 15
    assert sum_nested_list([[1, 2], [3, 4], 5]) == 15
    assert sum_nested_list([1, [2, [3, 4]], 5]) == 15
    assert sum_nested_list([[[1, 2], 3], 4, 5]) == 15
    assert sum_nested_list([1, 2, 3, 4, 5]) == 15
    assert sum_nested_list([]) == 0
    assert sum_nested_list([[[[[]]]]]) == 0
    assert sum_nested_list([[[[1]]]]) == 1
    assert sum_nested_list([1, [2, [3, [4, [5]]]]]) == 15
    assert sum_nested_list([10, [20, [30, [40]]], 50]) == 150
    assert sum_nested_list([-1, [-2, [-3, [-4]]], -5]) == -15
    assert sum_nested_list([0, [0, [0]], 0]) == 0
    assert sum_nested_list([1, [2], [[3]], [[[4]]], [[[[5]]]]]) == 15
    assert sum_nested_list([1, [2, [3]], [4, [5]]]) == 15
    assert sum_nested_list([[[1]], [[2]], [[3]], [[4]], [[5]]]) == 15
    assert sum_nested_list([1, [2, [3, [4, [5, [6]]]]]]) == 21
    assert sum_nested_list([100]) == 100
    assert sum_nested_list([[100]]) == 100
    assert sum_nested_list([[[100]]]) == 100
    assert sum_nested_list([1.5, [2.5], [[3.5]]]) == pytest.approx(7.5)