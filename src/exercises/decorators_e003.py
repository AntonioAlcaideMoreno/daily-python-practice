"""
Decorators exercise 3 decorators_e003: Stacking Decorators - Validation + Timing

Concepts: Decorator composition, execution order, separation of concerns
"""

import inspect
import time
from functools import wraps


# Timing decorator (from Exercise 1—provided for reference)
def timer_decorator(func):
    """Measures execution time"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = time.time() - start
        print(f"⏱️  {func.__name__} took {elapsed:.4f} seconds")
        return result

    return wrapper


# TODO: Implement the validation decorator
def validate_positive(*arg_names):
    """
    A decorator factory that validates specified arguments are positive numbers.

    This decorator accepts a list of argument names to validate. For example:
    @validate_positive("age", "salary") checks that 'age' and 'salary' are > 0

    Parameters:
        *arg_names: Variable number of argument names to validate as positive

    Returns:
        A decorator that validates the specified arguments

    Behavior:
    - Before executing the function, check each specified argument
    - If any specified argument is <= 0 or not a number, raise ValueError
    - If all specified arguments are positive, execute normally
    - Include the function name and argument name in error messages
    """
    # HINT: This is also a decorator factory
    # It takes configuration (arg_names)
    # Returns a decorator
    # Which returns a wrapper

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Create a mapping of argument names to their values
            # Hint: Use inspect.signature() or zip function names with args
            # For now, assume args are positional and in order

            sig = inspect.signature(func)  # Get function signature for argument mapping
            bound = sig.bind(*args, **kwargs)  # Bind args/kwargs to parameter names
            bound.apply_defaults()  # Apply default values for missing args
            # Now arguments are available as a dictionary: bound.arguments

            # HINT: The following code assumes function has arguments in order
            # For a more robust solution, use inspect module
            # but this simplified version works for positional args

            # Get function argument names (you'll need to extract them from func)
            # One approach: Use func.__code__.co_varnames

            # func_arg_names = func.__code__.co_varnames[:len(args)]
            # arg_dict = dict(zip(func_arg_names, args))

            # TODO: Iterate through arg_names (the ones specified for validation)
            # For each arg_name in arg_names:
            #   - Check if arg_name is in arg_dict
            #   - If it is, verify that arg_dict[arg_name] > 0
            #   - If validation fails, raise ValueError with a descriptive message
            for argname in arg_names:
                if argname in bound.arguments:
                    value = bound.arguments[argname]
                    if not isinstance(value, (int, float)) or value <= 0:
                        raise ValueError(
                            f"Argument '{argname}' must be a positive number in"
                            + " function '{func.__name__}'"
                        )
            # If all validations pass, execute and return the function
            return func(*args, **kwargs)

        return wrapper

    return decorator


# Example function: calculate discount
# Multiple decorators are applied: validation first, then timing
@timer_decorator
@validate_positive("amount", "discount_percent")
def calculate_discount(amount, discount_percent):
    """
    Calculate discount on a purchase amount.

    Args:
        amount: Purchase amount (must be positive)
        discount_percent: Discount percentage (must be positive)

    Returns:
        Discount amount
    """
    return amount * (discount_percent / 100)


# Example function: calculate compound interest
@timer_decorator
@validate_positive("principal", "rate", "years")
def compound_interest(principal, principal_rate, years):
    """
    Calculate compound interest.

    Args:
        principal: Initial amount (must be positive)
        principal_rate: Interest rate as percentage (must be positive)
        years: Time period (must be positive)

    Returns:
        Total amount after interest
    """
    # Simulate some computation
    time.sleep(0.1)
    rate = principal_rate / 100
    return principal * ((1 + rate) ** years)


# Tests (pre-written)
if __name__ == "__main__":
    print("=== Test 1: Valid arguments (both decorators work) ===")
    try:
        result = calculate_discount(100, 20)
        print(f"Discount: ${result:.2f}\n")
    except ValueError as e:
        print(f"Validation error: {e}\n")

    print("=== Test 2: Invalid argument (validation fails) ===")
    try:
        result = calculate_discount(100, -20)
        print(f"Discount: ${result:.2f}\n")
    except ValueError as e:
        print(f"Validation error: {e}\n")

    print("=== Test 3: Multiple validations ===")
    try:
        result = compound_interest(1000, 5, 2)
        print(f"Total: ${result:.2f}\n")
    except ValueError as e:
        print(f"Validation error: {e}\n")

    print("=== Test 4: Multiple failures ===")
    try:
        result = compound_interest(-1000, 5, 2)
        print(f"Total: ${result:.2f}\n")
    except ValueError as e:
        print(f"Validation error: {e}\n")

    print("✅ All tests complete!")
