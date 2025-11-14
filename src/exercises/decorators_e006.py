"""
Decorators exercise 6 decorators_e006: Error Handling Decorator with Retry Logic

Concepts: Exception handling, exponential backoff, resilience patterns
"""

import random
import time
from functools import update_wrapper


class RetryDecorator:
    """
    A decorator that retries failed function calls with exponential backoff.

    Exponential backoff: Wait time doubles after each failure
    - Attempt 1 fails → wait 1s
    - Attempt 2 fails → wait 2s
    - Attempt 3 fails → wait 4s
    - Attempt 4 fails → wait 8s

    This prevents overwhelming a failing service (e.g., rate-limited API)
    while giving transient errors time to resolve.

    Design decisions:
    - Which exceptions to catch (not all errors should trigger retry)
    - How many retries before giving up
    - Delay strategy (exponential, linear, constant)
    - Whether to add jitter (randomness) to prevent thundering herd
    """

    def __init__(
        self,
        func,
        max_retries=3,
        base_delay=1,
        exceptions=(Exception,),
        exponential=True,
        jitter=False,
    ):
        """
        Initialize the retry decorator.

        Parameters:
            func: The function to decorate
            max_retries: Maximum number of retry attempts (default 3)
            base_delay: Initial delay in seconds (default 1)
            exceptions: Tuple of exception types to catch (default all Exception)
            exponential: If True, use exponential backoff; if False, constant delay
            jitter: If True, add random jitter to delay (prevents thundering herd)
        """
        # TODO: Store configuration
        self.func = func
        self.max_retries = max_retries
        self.base_delay = base_delay
        if isinstance(exceptions, type):
            self.exceptions = (exceptions,)
        else:
            self.exceptions = tuple(exceptions)
        for ex in self.exceptions:
            if not isinstance(ex, type) or not issubclass(ex, BaseException):
                raise TypeError("Exceptions must be exception types")
        self.exceptions = exceptions
        self.exponential = exponential
        self.jitter = jitter

        # TODO: Initialize statistics
        self.statistics = {"total_attempts": 0, "successful_attempts": 0}

        # TODO: Preserve function metadata
        if func is not None:
            update_wrapper(self, func)

    def _calculate_delay(self, attempt):
        """
        Calculate delay before next retry attempt.

        Parameters:
            attempt: Current attempt number (1-indexed)

        Returns:
            Delay in seconds
        """
        # TODO: Implement delay calculation
        delay = (
            self.base_delay * (2 ** (attempt - 1))
            if self.exponential
            else self.base_delay
        )
        if self.jitter:
            jitter_amount = 0.25 * delay
            delay += random.uniform(-jitter_amount, jitter_amount)
        return delay
        # If exponential: delay = base_delay * (2 ** (attempt - 1))
        # If constant: delay = base_delay
        # If jitter: add random amount (e.g., ±25% of delay)

    def __call__(self, *args, **kwargs):
        """
        Execute function with retry logic.

        Flow:
        1. Try executing the function
        2. If it succeeds: return result
        3. If it fails with a retryable exception:
            a. Check if we have retries remaining
                a.1. If yes: wait (with backoff), then retry
                a.2. If no: raise the exception
        4. Track statistics (attempts, successes, failures)

        Parameters:
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
        """
        # TODO: Implement retry loop
        # Retry loop: attempts from 1 to max_retries + 1
        # (+1 because first attempt is not a "retry")
        for attempt in range(1, self.max_retries + 2):
            self.statistics["total_attempts"] += 1
            try:
                result = self.func(*args, **kwargs)
                self.statistics["successful_attempts"] += 1
                if attempt > 1:
                    print(f"'{self.func.__name__}' succeeded on attempt {attempt}")
                return result
            except self.exceptions as e:
                if attempt >= self.max_retries:
                    print(
                        f"'{self.func.__name__}' failed after {attempt} attempts. "
                        f"No more retries left."
                    )
                    raise e
                delay = self._calculate_delay(attempt)
                print(
                    f"'{self.func.__name__}' failed on attempt {attempt} with "
                    f"{e.__class__.__name__}: {e}. "
                    f"Retrying in {delay:.2f} seconds..."
                )
                time.sleep(delay)
            except Exception as e:
                # Non-retryable exception, re-raise immediately
                print(
                    f"'{self.func.__name__}' failed with non-retryable exception: "
                    + f"{e.__class__.__name__}: {e}. No retries will be attempted."
                )
                raise e

        # Hint: Use a for loop from 1 to max_retries + 1
        # On each iteration:
        #   - Try executing the function
        #   - If success: return immediately
        #   - If failure and retries remain: calculate delay, sleep, continue
        #   - If failure and no retries: raise exception

    def get_stats(self):
        """
        Return retry statistics.
        """
        return {
            "function": self.func.__name__,
            "total_attempts": self.statistics["total_attempts"],
            "successful_attempts": self.statistics["successful_attempts"],
            "failed_attempts": self.statistics["total_attempts"]
            - self.statistics["successful_attempts"],
            "max_retries": self.max_retries,
        }


def retry(
    max_retries=3, base_delay=1, exceptions=(Exception,), exponential=True, jitter=False
):
    """
    Factory function for parameterized retry decorator.

    Usage:
        @retry(max_retries=5, base_delay=2, exceptions=(TimeoutError,))
        def call_api(url):
            response = requests.get(url, timeout=5)
            return response.json()
    """

    def decorator(func):
        return RetryDecorator(
            func,
            max_retries=max_retries,
            base_delay=base_delay,
            exceptions=exceptions,
            exponential=exponential,
            jitter=jitter,
        )

    return decorator


# Simulated unreliable functions for testing
class APIError(Exception):
    """Custom exception for API failures"""

    pass


_call_count = 0


@retry(max_retries=3, base_delay=1, exceptions=(APIError,))
def unreliable_api_call(endpoint):
    """
    Simulates an unreliable API that fails the first 2 times.
    """
    global _call_count
    _call_count += 1

    if _call_count <= 2:
        print(f"  [Attempt {_call_count}] API call to {endpoint} failed!")
        raise APIError(f"Simulated API failure for {endpoint}")

    print(f"  [Attempt {_call_count}] API call to {endpoint} succeeded!")
    return {"status": "success", "data": f"Data from {endpoint}"}


@retry(max_retries=5, base_delay=0.5, exponential=True, jitter=True)
def flaky_database_query(query):
    """
    Simulates a database query that randomly fails 50% of the time.
    """
    if random.random() < 0.5:
        print(f"  Database query failed: {query}")
        raise ConnectionError("Database connection timeout")

    print(f"  Database query succeeded: {query}")
    return f"Results for: {query}"


@retry(max_retries=2, base_delay=1, exceptions=(ValueError,))
def strict_validation(value):
    """
    Function that should NOT retry on TypeError (wrong usage).
    """
    if not isinstance(value, int):
        raise TypeError("Value must be an integer")  # Don't retry this!

    if value < 0:
        raise ValueError("Value must be positive")  # Retry this!

    return value * 2


# Tests
if __name__ == "__main__":
    print("=== Test 1: Unreliable API with retries ===")
    try:
        result = unreliable_api_call("/users")
        print(f"Final result: {result}\n")
    except APIError as e:
        print(f"All retries exhausted: {e}\n")

    # Reset global counter
    _call_count = 0

    print("=== Test 2: API stats ===")
    print(f"Stats: {unreliable_api_call.get_stats()}\n")

    print("=== Test 3: Flaky database with jitter ===")
    try:
        result = flaky_database_query("SELECT * FROM users")
        print(f"Query result: {result}\n")
    except ConnectionError as e:
        print(f"Query failed after retries: {e}\n")

    print("=== Test 4: Selective exception catching ===")
    print("Testing ValueError (should retry):")
    try:
        result = strict_validation(-5)
        print(f"Result: {result}")
    except ValueError as e:
        print(f"Failed after retries: {e}")

    print("\nTesting TypeError (should NOT retry):")
    try:
        result = strict_validation("not an int")
        print(f"Result: {result}")
    except TypeError as e:
        print(f"Failed immediately (no retry): {e}")

    print("\n✅ All tests complete!")
