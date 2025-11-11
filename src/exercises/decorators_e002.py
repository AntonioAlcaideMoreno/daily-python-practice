"""
Decorators exercise 2 decorators_e002: Logging Decorator with Arguments

Concepts: Decorator factories, parameterized decorators, nested closures

Further improvements should include logger objects via the logging library
"""

from functools import wraps


# TODO: Implement the logging_decorator factory
def logging_decorator(log_level="INFO", prefix=""):
    """
    A decorator factory that creates a logging decorator with customizable behavior.

    This is a THREE-LEVEL NESTING pattern:
    - Level 1: logging_decorator(log_level, prefix) → returns a decorator
    - Level 2: decorator(func) → returns a wrapper
    - Level 3: wrapper(*args, **kwargs) → executes the function

    Each level is a closure that remembers the previous level's variables.

    Parameters:
        log_level: String indicating logging level ("DEBUG", "INFO", "WARNING", "ERROR")
        prefix: Optional prefix string to prepend to log messages

    Returns:
        A decorator function that wraps other functions with logging
    """
    # HINT: This function should RETURN a decorator function
    # The returned decorator should RETURN a wrapper function
    # This creates the three-level nesting required for parameterized decorators

    def decorator(func):
        """
        The actual decorator (returned by logging_decorator).
        This is a closure that remembers log_level and prefix.
        """
        # TODO: Define a wrapper function inside decorator
        # The wrapper should:
        #   1. Log a "calling" message with function name, arguments, and log_level
        #   2. Execute the original function
        #   3. Log a "completed" message
        #   4. Return the result

        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Construct a "calling" message
            # Format: f"[{log_level}] {prefix}Calling {func.__name__}({args}, {kwargs})"
            # Hint: Consider whether you need to show all args/kwargs or just a summary
            print(f"[{log_level}] {prefix}Calling {func.__name__}({args},{kwargs})")
            # TODO: Execute the original function
            result = func(*args, **kwargs)

            # TODO: Construct a "completed" message
            print(f"[{log_level}] {prefix}{func.__name__} completed successfully")
            # Format: f"[{log_level}] {prefix}{func.__name__} completed successfully"
            return result
            # TODO: Return the result

        return wrapper

    return decorator


# Example functions to decorate
@logging_decorator(log_level="DEBUG", prefix="[AUTH] ")
def authenticate_user(username, password):
    """Simulate user authentication"""
    if username == "admin" and password == "secret":
        return True
    return False


@logging_decorator(log_level="INFO", prefix="[DB] ")
def fetch_data(query):
    """Simulate database fetch"""
    return f"Data from: {query}"


@logging_decorator(log_level="WARNING")  # Default prefix (empty)
def risky_operation(value):
    """Simulate a risky operation"""
    if value < 0:
        return "Invalid input"
    return f"Processed: {value}"


# Tests (pre-written, just run them)
if __name__ == "__main__":
    print("=== Test 1: DEBUG level with prefix ===")
    result = authenticate_user("admin", "secret")
    print(f"Result: {result}\n")

    print("=== Test 2: INFO level with prefix ===")
    result = fetch_data("SELECT * FROM users")
    print(f"Result: {result}\n")

    print("=== Test 3: WARNING level without prefix ===")
    result = risky_operation(42)
    print(f"Result: {result}\n")

    print("=== Test 4: Different decorator instance ===")
    # Create a decorator with different parameters
    error_logger = logging_decorator(log_level="ERROR", prefix="[CRITICAL] ")

    @error_logger
    def critical_task():
        return "Critical task done"

    result = critical_task()
    print(f"Result: {result}\n")

    print("✅ All tests complete! Check the logging output above.")
