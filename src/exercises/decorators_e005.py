"""
Decorators exercise 5 decorators_e005: Caching Decorator (Memoization)

Concepts: Cache design, argument hashing, memory-performance trade-offs
"""

import inspect
from functools import update_wrapper


class CacheDecorator:
    """
    A class-based decorator that caches function results.

    This demonstrates the trade-off between memory usage and performance:
    - First call: Execute function, store result
    - Subsequent calls with same args: Return cached result (fast!)
    - Different args: Execute function again (no cache hit)

    Design considerations:
    - Cache key must be derived from arguments
    - Only works for pure functions (same args → same result)
    - Memory grows with cache size
    - Need strategy for cache eviction (max size, TTL, LRU)
    """

    def __init__(self, func, max_cache_size=128):
        """
        Initialize the cache decorator.

        Parameters:
            func: The function to cache
            max_cache_size: Maximum number of cached results (default 128)
        """
        # TODO: Store the function
        self.func = func

        # TODO: Initialize the cache as an empty dictionary
        # Format: { cache_key: result }
        self.cache = {}

        # TODO: Store the maximum cache size
        self.max_cache_size = max_cache_size

        # TODO: Initialize cache hit/miss statistics (optional but useful)
        self.cache_hits_miss = {"Cache Hits": 0, "Cache Misses": 0}
        self.sig = inspect.signature(
            self.func
        )  # We perform this expensive operation once

        # TODO: Preserve function metadata
        if func is not None:
            update_wrapper(self, func)

    def _make_cache_key(self, args, kwargs):
        """
        Create a hashable cache key from function arguments.

        Challenge: args and kwargs must be converted to something hashable
        so they can be dictionary keys.

        Approach:
        - Convert args tuple (already hashable if contents are hashable)
        - Convert kwargs dict to a sorted tuple of (key, value) pairs
        - Combine both into a single hashable key

        Returns:
            A hashable object usable as dict key
        """
        # TODO: Create a hashable key from args and kwargs
        bound_args = self.sig.bind(*args, **kwargs)
        bound_args.apply_defaults()
        cache_key = tuple((k, bound_args.arguments[k]) for k in bound_args.arguments)
        return cache_key

    def __call__(self, *args, **kwargs):
        """
        Execute the cached function.

        Flow:
        1. Generate cache key from arguments
        2. Check if key exists in cache
        3. If yes (cache hit): return cached result
        4. If no (cache miss): execute function, cache result, return it
        5. Track hits/misses for statistics

        Parameters:
            *args: Positional arguments for the function
            **kwargs: Keyword arguments for the function
        """
        # TODO: Generate cache key
        cache_key = self._make_cache_key(args, kwargs)
        # TODO: Check if key is in cache
        if cache_key in self.cache:
            # TODO: On cache hit:
            #   - Increment cache_hits
            #   - Print a message like "[CACHE HIT] Returning cached result for
            #     {func_name}"
            #   - Return the cached result
            self.cache_hits_miss["Cache Hits"] += 1
            print(
                f"[CACHE HIT] Returning cached result for {self.func.__name__}"
                + "function"
            )
            return self.cache[cache_key]
        # TODO: On cache miss:
        self.cache_hits_miss["Cache Misses"] += 1
        result = self.func(*args, **kwargs)
        if len(self.cache) >= self.max_cache_size:
            self.cache.pop(next(iter(self.cache)))
            """ Iter creates an iterator over dictionary's keys. From Python 3.7
            onwards, dictionaries maintain insertion order, so popping the first key
            effectively removes the oldest entry in the cache. Next is just used to go
            to the first key from the iterator."""
        self.cache[cache_key] = result
        print(
            f"[CACHE MISS] Computed and cached result for {self.func.__name__}"
            + "function"
        )
        return result
        #   - Increment cache_misses
        #   - Execute the function
        #   - Check if cache is full (len(self.cache) >= self.max_cache_size)
        #   - If full, evict one entry (for now, pop any entry or oldest)
        #   - Store result in cache
        #   - Print a message like "[CACHE MISS] Computed and cached result"
        #   - Return the result

    def clear_cache(self):
        """
        Clear all cached results.
        """
        self.cache.clear()
        for key in self.cache_hits_miss.keys():
            self.cache_hits_miss[key] = 0

    def get_cache_stats(self):
        """
        Return cache statistics.
        """
        total_requests = sum(self.cache_hits_miss.values())
        hit_rate = (
            (self.cache_hits_miss["Cache Hits"] / total_requests * 100)
            if total_requests > 0
            else 0
        )

        return {
            "cache_size": len(self.cache),
            "max_cache_size": self.max_cache_size,
            "cache_hits": self.cache_hits_miss["Cache Hits"],
            "cache_misses": self.cache_hits_miss["Cache Misses"],
            "total_requests": total_requests,
            "hit_rate": f"{hit_rate:.1f}%",
        }


def cache(max_cache_size=128):
    """
    Factory function for parameterized cache decorator.

    Usage:
        @cache(max_cache_size=256)
        def expensive_function(x, y):
            return x ** y
    """

    def decorator(func):
        return CacheDecorator(func, max_cache_size=max_cache_size)

    return decorator


# Example functions
@cache(max_cache_size=10)
def fibonacci(n):
    """
    Compute fibonacci number (expensive without caching).

    Args:
        n: Position in fibonacci sequence

    Returns:
        nth fibonacci number
    """
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)


@cache()
def expensive_computation(x, y, operation="add"):
    """
    Simulate an expensive computation (e.g., ML model inference, database query).

    Args:
        x, y: Input values
        operation: Type of operation ("add", "multiply", "power")
    """
    # Simulate expensive work
    import time

    time.sleep(0.1)

    if operation == "add":
        return x + y
    elif operation == "multiply":
        return x * y
    elif operation == "power":
        return x**y
    else:
        return None


# Tests (pre-written)
if __name__ == "__main__":
    print("=== Test 1: Basic caching (same args = cache hit) ===")
    result1 = expensive_computation(5, 3, operation="add")
    print(f"Result 1: {result1}")
    result2 = expensive_computation(5, 3, operation="add")
    print(f"Result 2: {result2} (cached)\n")

    print("=== Test 2: Different args = cache miss ===")
    result3 = expensive_computation(10, 2, operation="multiply")
    print(f"Result 3: {result3}\n")

    print("=== Test 3: Keyword argument variation ===")
    result4 = expensive_computation(x=5, y=3, operation="add")
    print(f"Result 4: {result4} (should be cache hit despite keyword syntax)\n")

    print("=== Test 4: Cache statistics ===")
    stats = expensive_computation.get_cache_stats()
    print(f"Cache stats: {stats}\n")

    print("=== Test 5: Fibonacci (exponential complexity reduced by caching) ===")
    result = fibonacci(10)
    print(f"fibonacci(10) = {result}")
    fib_stats = fibonacci.get_cache_stats()
    print(f"Fibonacci cache stats: {fib_stats}\n")

    print("=== Test 6: Cache overflow (max_cache_size=10) ===")
    for i in range(15):
        fibonacci(i)
    fib_stats = fibonacci.get_cache_stats()
    print(f"Fibonacci cache stats after overflow: {fib_stats}\n")

    print("=== Test 7: Clear cache ===")
    expensive_computation.clear_cache()
    print(f"After clear: {expensive_computation.get_cache_stats()}\n")

    print("✅ All tests complete!")
