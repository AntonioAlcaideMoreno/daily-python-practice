"""
Decorators exercise 4 decorators_e004: Class-Based Decorators with State

Concepts: Class-based decorators, state management, __call__ method
"""

from functools import update_wrapper


# TODO: Implement the CallCounter class decorator
class CallCounter:
    """
    A class-based decorator that counts function calls.

    This demonstrates state management: the decorator remembers how many times
    the function has been called across invocations.

    Class-based decorators work via two special methods:
    - __init__(self, func): Called when decorator is applied (initialization)
    - __call__(self, *args, **kwargs): Called when the decorated function is invoked

    Parameters:
        max_calls: Optional limit on number of calls (None = unlimited)

    Raises:
        RuntimeError: If max_calls is exceeded
    """

    def __init__(self, func=None, max_calls=None):
        """
        Initialize the decorator.

        This is called when the decorator is applied to a function.
        For example: @CallCounter or @CallCounter(max_calls=5)

        Parameters:
            func: The function being decorated (None if decorator has arguments)
            max_calls: Optional maximum number of allowed calls
        """
        # TODO: Store the function being decorated
        # Hint: Save it as self.func
        self.func = func
        # TODO: Initialize a call counter
        # Hint: Use self.call_count = 0
        self.call_count = 0
        # TODO: Store the max_calls limit
        # Hint: Use self.max_calls = max_calls
        self.max_calls = max_calls
        # TODO: Preserve function metadata
        # Hint: Use functools.update_wrapper(self, func) if func is not None
        if func is not None:
            update_wrapper(self, func)  # This is a function coming from functools

    def __call__(self, *args, **kwargs):
        """
        This method is called when the decorated function is invoked.

        Flow:
        1. Increment the call counter
        2. Check if max_calls limit is exceeded
        3. If exceeded, raise RuntimeError
        4. Otherwise, execute the original function
        5. Return the result

        Parameters:
            *args: Positional arguments for the decorated function
            **kwargs: Keyword arguments for the decorated function
        """
        # TODO: Increment the call counter
        # Hint: self.call_count += 1
        self.call_count += 1
        if (self.max_calls is not None) and (self.call_count > self.max_calls):
            raise RuntimeError(
                f"'{self.func.__name__}' has exceeded max calls {self.max_calls}"
            )
        print(f"[Call {self.call_count}] Calling '{self.func.__name__}'")
        return self.func(*args, **kwargs)

        # TODO: Check if max_calls is set and exceeded
        # Hint: if self.max_calls is not None and self.call_count > self.max_calls:

        # TODO: If exceeded, raise RuntimeError with a descriptive message
        # Format: f"{self.func.__name__} has exceeded max calls ({self.max_calls})"

        # TODO: Log the call (optional but helpful for visibility)
        # Format: f"[Call {self.call_count}] Calling {self.func.__name__}"

        # TODO: Execute the original function and return the result

    def reset(self):
        """
        Resets the call counter to zero.
        """
        self.call_count = 0

    def get_stats(self):
        """
        Returns a dictionary with call statistics.
        """
        return {
            "function name": self.func.__name__,
            "callcount": self.call_count,
            "max calls": self.max_calls,
            "remaining calls": (
                None if self.max_calls is None else self.max_calls - self.call_count
            ),
        }


# Alternative: Decorator factory pattern for class-based decorators
def call_counter(max_calls=None):
    """
    Factory function that returns a CallCounter instance.

    This enables the syntax: @call_counter(max_calls=5)
    """

    def decorator(func):
        return CallCounter(func, max_calls=max_calls)

    return decorator


# Example functions to decorate
@CallCounter
def greet(name):
    """Simple greeting function with unlimited calls"""
    return f"Hello, {name}!"


@call_counter(max_calls=3)
def fetch_data(query):
    """Function with call limit (max 3 calls)"""
    return f"Data for query: {query}"


@call_counter(max_calls=1)
def initialize_system():
    """Function that should only be called once"""
    return "System initialized"


# Tests (pre-written)
if __name__ == "__main__":
    print("=== Test 1: Unlimited calls (CallCounter without arguments) ===")
    for i in range(5):
        result = greet(f"User{i}")
        print(f"  {result}")
    print()

    print("=== Test 2: Limited calls (max_calls=3) ===")
    for i in range(4):
        try:
            result = fetch_data(f"SELECT * FROM table{i}")
            print(f"  {result}")
        except RuntimeError as e:
            print(f"  Error: {e}")
    print()

    print("=== Test 3: Single call limit (max_calls=1) ===")
    for _ in range(3):
        try:
            result = initialize_system()
            print(f"  {result}")
        except RuntimeError as e:
            print(f"  Error: {e}")
    print()

    print("=== Test 4: Inspect call counts ===")
    print(f"  greet called: {greet.call_count} times")
    print(f"  fetch_data called: {fetch_data.call_count} times")
    print(f"  initialize_system called: {initialize_system.call_count} times")

    print("\n=== Test 5: Resetting call counter for fetch_data ===")
    print(f"  Before reset: fetch_data called {fetch_data.call_count} times")
    fetch_data.reset()
    print(f"  After reset: fetch_data called {fetch_data.call_count} times")

    print("\n=== Test 6: Call stats ===")
    print(f"  greet stats: {greet.get_stats()}")

    print("\n✅ All tests complete!")
