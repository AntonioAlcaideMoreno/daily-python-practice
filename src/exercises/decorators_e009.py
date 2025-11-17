"""
Decorators exercise 9 decorators_e009: Context Manager Decorator (Resource Management)

Concepts: Context managers, __enter__/__exit__, setup/cleanup, exception handling
"""

import time
from functools import wraps


class DatabaseConnection:
    """
    Simulates a database connection that needs cleanup.

    Demonstrates resource management: open on entry, close on exit.
    """

    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.is_connected = False

    def open(self):
        """Simulate opening a connection (setup)"""
        print(f"  [DB] Opening connection to {self.connection_string}")
        self.is_connected = True
        time.sleep(0.1)  # Simulate connection time
        return self

    def close(self):
        """Simulate closing a connection (cleanup)"""
        print(f"  [DB] Closing connection to {self.connection_string}")
        self.is_connected = False

    def query(self, sql):
        """Execute a query"""
        if not self.is_connected:
            raise RuntimeError("Database not connected")
        print(f"  [DB] Executing: {sql}")
        return f"Results for: {sql}"

    def __enter__(self):
        """Context manager entry"""
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit (called even if exception occurs)"""
        self.close()
        # Return False to propagate any exception
        return False


class TemporaryFileHandle:
    """Simulates a file handle that needs cleanup."""

    def __init__(self, filename):
        self.filename = filename
        self.is_open = False
        self.data = []

    def open(self):
        """Open the file"""
        print(f"  [FILE] Opening file: {self.filename}")
        self.is_open = True
        return self

    def close(self):
        """Close the file"""
        print(f"  [FILE] Closing file: {self.filename}")
        self.is_open = False

    def write(self, content):
        """Write to file"""
        if not self.is_open:
            raise RuntimeError("File not open")
        self.data.append(content)
        print(f"  [FILE] Wrote to {self.filename}: {content}")

    def __enter__(self):
        return self.open()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
        return False


# Decorator: Automatically manage resource via context manager
def manage_resource(resource_factory):
    """
    Decorator factory that manages a resource's lifecycle.

    The resource_factory is a callable that returns a context manager.
    The decorated function receives the resource as first argument.

    Usage:
        def create_database():
            return DatabaseConnection("postgres://localhost/mydb")

        @manage_resource(create_database)
        def fetch_users(db):
            return db.query("SELECT * FROM users")

        # When you call fetch_users(), the decorator:
        # 1. Creates the database connection
        # 2. Opens it (calls __enter__)
        # 3. Calls the function with the open connection
        # 4. Closes it (calls __exit__), even if exception occurs
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Create the resource (via factory)
            resource = resource_factory()
            # Hint: resource = resource_factory()
            with resource as res:
                return func(res, *args, **kwargs)
            # TODO: Use context manager to manage resource lifecycle
            # Hint: with resource as res:
            #           return func(res, *args, **kwargs)

        return wrapper

    return decorator


# Decorator: Timing with guaranteed cleanup
class TimedContext:
    """
    A context manager that times execution and ensures cleanup.

    Even if the function raises an exception, cleanup code runs.
    """

    def __init__(self, name):
        self.name = name
        self.start_time = None

    def __enter__(self):
        """Called on entry: start timing"""
        print(f"[TIMER] Starting {self.name}")
        self.start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called on exit: print elapsed time, cleanup"""
        elapsed = time.time() - self.start_time

        if exc_type is not None:
            # An exception occurred
            print(
                f"[TIMER] {self.name} failed after {elapsed:.3f}s: {exc_type.__name__}"
            )
        else:
            # Success
            print(f"[TIMER] {self.name} completed in {elapsed:.3f}s")

        # Return False to propagate any exception
        return False


def timed_execution(func):
    """
    Decorator that times function execution and ensures cleanup.

    Demonstrates using a context manager within a decorator.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: Use TimedContext to wrap execution
        with TimedContext(func.__name__):
            # DOUBT: Why do we use an alias in this case and not in the
            # logged_execution one?
            return func(*args, **kwargs)
        # Hint: with TimedContext(func.__name__) as timer:
        #           return func(*args, **kwargs)

    return wrapper


# Decorator: Exception handling with cleanup
class LoggingContext:
    """
    A context manager that logs entry/exit and handles exceptions.
    """

    def __init__(self, function_name):
        self.function_name = function_name

    def __enter__(self):
        """Called on entry"""
        print(f"[LOG] >>> Entering {self.function_name}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Called on exit (even if exception)"""
        if exc_type is None:
            print(f"[LOG] <<< Exiting {self.function_name} (success)")
        else:
            print(
                f"[LOG] <<< Exiting {self.function_name}"
                + f" (exception: {exc_type.__name__})"
            )

        # Return False to propagate exception
        return False


def logged_execution(func):
    """
    Decorator that logs function entry/exit with exception handling.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: Use LoggingContext to wrap execution
        with LoggingContext(func.__name__):
            # DOUBT: Why don't we use an alias in this case and not in the
            # timed_execution one?
            # Hint: with LoggingContext(func.__name__):
            #           return func(*args, **kwargs)
            return func(*args, **kwargs)

    return wrapper


# Example functions using decorators


def create_database():
    """Factory that creates a database connection resource"""
    return DatabaseConnection("postgres://localhost/mydb")


def create_file():
    """Factory that creates a file handle resource"""
    return TemporaryFileHandle("/tmp/data.txt")


@manage_resource(create_database)
def query_database(db, user_id):
    """
    Query database. Resource is automatically managed.
    """
    return db.query(f"SELECT * FROM users WHERE id = {user_id}")


@manage_resource(create_file)
def write_file(file_handle, content):
    """
    Write to file. Resource is automatically managed.
    """
    file_handle.write(content)
    return "Wrote to file"


@timed_execution
def slow_operation():
    """Operation that takes time. Timing is automatic."""
    print("  Performing slow operation...")
    time.sleep(0.5)
    return "Done"


@logged_execution
def divide_numbers(a, b):
    """
    Division function with logging.

    Demonstrates that cleanup happens even if exception occurs.
    """
    result = a / b
    print(f"  Result: {result}")
    return result


# Tests
if __name__ == "__main__":
    print("=== Test 1: Database resource management ===")
    result = query_database(user_id=123)
    print(f"Result: {result}\n")

    print("=== Test 2: File resource management ===")
    result = write_file("Important data")
    print(f"Result: {result}\n")

    print("=== Test 3: Timed execution (success) ===")
    result = slow_operation()
    print(f"Result: {result}\n")

    print("=== Test 4: Logged execution (success) ===")
    result = divide_numbers(10, 2)
    print(f"Result: {result}\n")

    print("=== Test 5: Logged execution with exception ===")
    try:
        result = divide_numbers(10, 0)  # Division by zero!
        print(f"Result: {result}")
    except ZeroDivisionError as e:
        print(f"Exception caught: {e}\n")

    print("=== Test 6: Resource cleanup even on exception ===")

    @manage_resource(create_database)
    def buggy_query(db):
        db.query("SELECT * FROM users")
        raise RuntimeError("Oops! Something went wrong")

    try:
        result = buggy_query()
    except RuntimeError as e:
        print(f"Exception caught: {e}\n")

    print("✅ All tests complete!")
