"""
Decorators exercise 1 decorators_e001: Your First Decorator - Function Timing

Concepts: Closures, Decorators, Function wrapping
"""

import time
from functools import wraps  # We'll explain this shortly


# TODO: Implement the timer_decorator function
def timer_decorator(func):
    """
    A decorator that measures how long a function takes to execute.

    This is a closure pattern: the wrapper function 'remembers' func.

    Parameters:
        func: The function to be timed

    Returns:
        A wrapped version of func that prints execution time
    """
    # HINT: You'll need to define an inner function (wrapper)
    # Approach:
    #   1. Create a wrapper function inside timer_decorator
    #   2. The wrapper should:
    #      - Record the start time before calling func()
    #      - Call the original function
    #      - Record the end time after calling func()
    #      - Print the elapsed time
    #      - Return the function's result
    #   3. Return the wrapper from timer_decorator

    @wraps(func)  # This preserves the original function's name and docstring
    def wrapper(*args, **kwargs):
        # TODO: Capture the start time using time.time()
        start_time = (
            time.time()
        )  # If we want this to be more accurate, we should use time.perf_counter()
        # TODO: Call the original function with its arguments
        # and store the result
        result = func(*args, **kwargs)
        # TODO: Capture the end time using time.time()
        end_time = time.time()
        # TODO: Calculate elapsed time (end - start)
        elapsed_time = end_time - start_time
        # TODO: Print a message showing execution time
        # Format: f"⏱️  {func.__name__} took {elapsed:.4f} seconds"
        print(f"{func.__name__} took {elapsed_time:.4f} seconds")
        # TODO: Return the result from the original function
        return result

    return wrapper


# Example functions to decorate (you won't modify these)
def slow_function():
    """A function that takes time to complete"""
    time.sleep(1)  # Simulate work by sleeping
    return "Task completed!"


def fast_function():
    """A function that completes quickly"""
    total = sum(range(1000000))
    return total


# Apply the decorator using the @ syntax
@timer_decorator
def greet(name):
    """Greet someone by name"""
    time.sleep(0.5)
    return f"Hello, {name}!"


# Tests (pre-written, just run them)
if __name__ == "__main__":
    print("=== Test 1: Timing a function ===")
    result = greet("Alice")
    print(f"Result: {result}\n")

    print("=== Test 2: Timing slow_function ===")
    decorated_slow = timer_decorator(slow_function)
    output = decorated_slow()
    print(f"Output: {output}\n")

    print("=== Test 3: Timing fast_function ===")
    decorated_fast = timer_decorator(fast_function)
    output = decorated_fast()
    print(f"Output: {output}\n")

    print("✅ All tests complete! Check the timing outputs above.")
