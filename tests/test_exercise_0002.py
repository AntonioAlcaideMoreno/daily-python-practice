import pytest

# Tests for fibonacci.py file
from exercises.fibonacci import fibonacci


def test_fibonacci_base_cases():
    assert fibonacci(1) == 0
    assert fibonacci(2) == 1


def test_fibonacci_sequence():
    assert fibonacci(6) == 5
    assert fibonacci(11) == 55


def test_fibonacci_negative_raises():
    with pytest.raises(ValueError):
        fibonacci(-1)
