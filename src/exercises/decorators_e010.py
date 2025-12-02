"""
Decorators exercise 10 decorators_e010: Advanced Decorator Composition & Patterns

Concepts: Decorator stacking, composition, metaprogramming and frameworks
"""

import inspect
import time
from functools import update_wrapper, wraps


# Pattern 1: Stacking Multiple Behaviors
class FunctionProfiler:
    """
    A decorator that profiles function execution: timing, call count, arguments

    Demonstrates combining multiple metrics into one decorator
    """

    def __init__(self, func):
        self.func = func
        self.call_count = 0
        self.total_time = 0
        self.call_times = []
        update_wrapper(self, func)

    def __call__(self, *args, **kwargs):
        """
        TODO: Implement profiling logic
        1. Record start time
        2. Increment call count
        3. Execute function
        4. Record end time
        5. Store metrics (total_time, individual times)
        6. Return result
        """
        # 1. Start time
        start_time = time.time()
        # 2. Increment call count
        self.call_count += 1
        # 3. Execute function
        try:
            result = self.func(*args, **kwargs)
        finally:
            # 4. Record end time
            end_time = time.time()
            elapsed = end_time - start_time
            # 5. Store metrics
            self.total_time += elapsed
            self.call_times.append(elapsed)
        return result

    def get_stats(self):
        """Return profiling statistics"""
        # TODO: Return dict with:
        # - call_count
        # - total_time
        # - average_time
        # - min_time
        # - max_time
        if not self.call_times:
            return {}

        return {
            "call_count": self.call_count,
            "total_time": self.total_time,
            "average_time": (
                self.total_time / self.call_count
                if self.call_count
                else "No average time available"
            ),
            "min_time": min(self.call_times),
            "max_time": max(self.call_times),
            "function_name": self.func.__name__,
        }


# Pattern 2: Decorator Chains with Configuration
class DecoratorChain:
    """
    A builder pattern for chaining multiple decorators.

    Usage:
        @(DecoratorChain(my_function)
          .with_timing()
          .with_logging()
          .with_caching()
          .build())
        def my_function(x):
            return x * 2
    """

    def __init__(self, func):
        self.func = func
        self.decorators = []

    def with_timing(self):
        """Add timing functionality"""

        # TODO: Add timing decorator to chain
        def timing_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                start_time = time.time()
                try:
                    result = func(*args, **kwargs)
                finally:
                    elapsed = time.time() - start_time
                    print(f"[TIMER] executed in {elapsed:.4f}s")
                return result

            return wrapper

        self.decorators.append(timing_decorator)
        return self

    def with_logging(self, level="INFO"):
        """Add logging functionality"""
        # TODO: Add logging decorator to chain
        level = level.upper()

        def logging_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(
                    f"[{level}] Entering function {func.__name__} with args={args},"
                    + f" kwargs={kwargs}"
                )
                try:
                    result = func(*args, **kwargs)
                finally:
                    print(
                        f"[{level}] Exiting function {func.__name__}"
                        + f" with result={result}"
                    )
                return result

            return wrapper

        self.decorators.append(logging_decorator)
        return self

    def with_caching(self, max_size=128):
        """Add caching functionality"""
        self.cache = {}
        self.cache_hit_miss = {"Cache Hits": 0, "Cache Misses": 0}
        self.sig = inspect.signature(self.func)
        self.max_cache_size = max_size

        # TODO: Add caching decorator to chain
        def caching_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # We create a cache key
                bound_args = self.sig.bind(*args, **kwargs)
                bound_args.apply_defaults()
                cache_key = tuple(
                    (k, bound_args.arguments[k]) for k in bound_args.arguments
                )
                # We check if in cache
                if cache_key in self.cache:
                    print(
                        "[CACHE] Cache hit. Returning cached result for "
                        + f"function {func.__name__}"
                    )
                    self.cache_hit_miss["Cache Hits"] += 1
                    return self.cache[cache_key]
                else:
                    print("[CACHE] Cache miss")
                    self.cache_hit_miss["Cache Misses"] += 1
                    try:
                        result = func(*args, **kwargs)
                    finally:
                        if len(self.cache) >= self.max_cache_size:
                            self.cache.pop(next(iter(self.cache)))
                            """ Iter creates an iterator over dictionary's keys.
                            From Python 3.7 onwards, dictionaries maintain insertion
                            order, so popping the first key effectively removes the
                            oldest entry in the cache. Next is just used to go
                            to the first key from the iterator."""
                        self.cache[cache_key] = result
                    return result
                return wrapper

            self.decorators.append(caching_decorator)
            return self

    def build(self):
        """Apply all decorators and return wrapped function"""
        result = self.func
        for decorator in self.decorators:
            result = decorator(result)
        return result
        # TODO: Apply decorators in order and return result
        # Hint: Start with self.func, apply each decorator


# Pattern 3: Conditional Decorators
def apply_if(condition, decorator):
    """
    Conditionally apply a decorator based on a condition.

    Usage:
        is_production = os.getenv("ENV") == "production"

        @apply_if(is_production, cache(max_size=1000))
        def expensive_operation():
            return compute()
    """

    def wrapper(func):
        # TODO: If condition is true, apply decorator
        # Otherwise, return function unchanged
        if condition:
            return decorator(func)
        else:
            return func

    return wrapper


# Pattern 4: Decorator with Before/After Hooks
class DecoratorWithHooks:
    """
    A decorator that supports before/after execution hooks.

    Usage:
        @DecoratorWithHooks()
        def process_data(data):
            return transform(data)

        @process_data.before
        def setup():
            print("Setting up...")

        @process_data.after
        def cleanup():
            print("Cleaning up...")
    """

    def __init__(self):
        self.before_hooks = []
        self.after_hooks = []

    def __call__(self, func):
        """Applied as a decorator"""

        # TODO: Implement decorator logic
        # Calls before_hooks, func, then after_hooks
        @wraps(func)
        def wrapper(*args, **kwargs):
            for b_hook in self.before_hooks:
                b_hook()
            try:
                result = func(*args, **kwargs)
            finally:
                for a_hook in self.after_hooks:
                    a_hook()
            return result

        return wrapper

    def before(self, hook_func):
        """Register a before-execution hook"""
        # TODO: Add hook to self.before_hooks
        if hook_func and hook_func not in self.before_hooks:
            self.before_hooks.append(hook_func)
        return hook_func

    def after(self, hook_func):
        """Register an after-execution hook"""
        # TODO: Add hook to self.after_hooks
        if hook_func and hook_func not in self.after_hooks:
            self.after_hooks.append(hook_func)
        return hook_func


# Pattern 5: Decorator That Inspects and Adapts
def smart_decorator(func):
    """
    A decorator that adapts its behavior based on function signature.

    - If function takes no arguments: cache results
    - If function takes arguments: validate them
    - If function returns dict: log keys
    """

    # TODO: Inspect function signature
    # TODO: Adapt behavior based on parameters and return type
    # TODO: Apply appropriate optimizations

    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: Implement adaptive behavior
        return func(*args, **kwargs)

    return wrapper


# Pattern 6: Metadata-Preserving Decorator
def preserve_metadata(func):
    """
    A decorator that preserves and augments function metadata.

    Demonstrates that decorators should maintain full traceability.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        # TODO: Execute function
        return func(*args, **kwargs)

    # TODO: Add decorator metadata
    wrapper.is_decorated = True
    wrapper.decorator_name = "preserve_metadata"

    return wrapper


# Example: Complex Real-World Scenario
class DataPipelineStep:
    """
    A reusable component for data processing pipelines.

    Combines timing, logging, caching, retry logic, and validation.
    """

    def __init__(self, name):
        self.name = name
        self.metrics = {
            "calls": 0,
            "successes": 0,
            "failures": 0,
            "total_time": 0,
            "cached_hits": 0,
        }

    def __call__(self, func):
        """
        TODO: Implement a decorator that:
        1. Validates input data
        2. Times execution
        3. Caches results
        4. Retries on failure
        5. Logs everything
        6. Tracks metrics

        All without modifying the original function!
        """

        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Comprehensive pipeline step implementation
            pass

        return wrapper

    def get_metrics(self):
        """Return pipeline metrics"""
        return self.metrics


# Tests
if __name__ == "__main__":
    print("=== Test 1: Function Profiler ===")

    @FunctionProfiler
    def fibonacci(n):
        """Calculate fibonacci number"""
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    result = fibonacci(5)
    print(f"Result: {result}")
    print(f"Stats: {fibonacci.get_stats()}\n")

    print("=== Test 2: Conditional Decorator ===")
    is_production = False

    @apply_if(is_production, lambda f: f)  # Simplified decorator for demo
    def config_value():
        return "production config"

    result = config_value()
    print(f"Result: {result}\n")

    print("=== Test 3: Decorator with Hooks ===")
    profiler = DecoratorWithHooks()

    @profiler
    def process_data(data):
        print(f"  Processing: {data}")
        return data.upper()

    @profiler.before
    def setup():
        print("  [SETUP] Initializing resources")

    @profiler.after
    def cleanup():
        print("  [CLEANUP] Releasing resources")

    result = process_data("hello")
    print(f"Result: {result}\n")

    print("=== Test 4: Smart Decorator ===")

    @smart_decorator
    def compute(x, y):
        """Compute something"""
        return {"sum": x + y, "product": x * y}

    result = compute(5, 3)
    print(f"Result: {result}\n")

    print("=== Test 5: Metadata Preservation ===")

    @preserve_metadata
    def important_function():
        """An important function"""
        return "result"

    print(f"Function name: {important_function.__name__}")
    print(f"Is decorated: {important_function.is_decorated}")
    print(f"Decorator: {important_function.decorator_name}\n")

    print("✅ All tests complete!")
