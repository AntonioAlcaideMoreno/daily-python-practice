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
                self.total_time / self.call_count if self.call_count else 0.0
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
        level = level.upper()

        def logging_decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                print(
                    f"[{level}] Entering function {func.__name__} with args={args}, "
                    f"kwargs={kwargs}"
                )

                try:
                    result = func(*args, **kwargs)
                finally:
                    print(
                        f"[{level}] Exiting function {func.__name__} "
                        f"with result={result}"
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
                    result = self.cache[cache_key]
                else:
                    print("[CACHE] Cache miss")
                    self.cache_hit_miss["Cache Misses"] += 1
                    try:
                        result = func(*args, **kwargs)
                    finally:
                        # We store in cache
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
    sig = inspect.signature(func)
    params = list(sig.parameters.keys())
    print(
        f"[SMART DECORATOR] Inspecting function '{func.__name__}'"
        + f"with {len(params)} parameters."
    )

    # TODO: Adapt behavior based on parameters and return type
    # TODO: Apply appropriate optimizations

    @wraps(func)
    def wrapper(*args, **kwargs):
        if len(params) == 0:
            print("  [SMART] No parameters - this is a good caching candidate")

        # If many parameters: be careful with caching
        elif len(params) > 3:
            print("  [SMART] Many parameters - caching might be inefficient")

        # Execute function
        result = func(*args, **kwargs)

        # Adapt post-execution behavior
        if isinstance(result, dict):
            print(f"  [SMART] Result is dict with keys: {list(result.keys())}")

        return result

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
    wrapper.decorator_name = preserve_metadata.__name__
    wrapper.original_function = func

    return wrapper


# Example: Complex Real-World Scenario
class DataPipelineStep:
    """
    A reusable component for data processing pipelines.

    Combines timing, logging, caching, retry logic, and validation.
    """

    def __init__(self, name, max_retries=3):
        self.name = name
        self.metrics = {
            "calls": 0,
            "successes": 0,
            "failures": 0,
            "total_time": 0,
            "cached_hits": 0,
        }
        self.cache = {}
        self.max_retries = max_retries

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
        sig = inspect.signature(func)

        @wraps(func)
        def wrapper(*args, **kwargs):
            # TODO: Comprehensive pipeline step implementation
            # Start timer
            start_time = time.time()
            # Add call to metrics
            self.metrics["calls"] += 1
            # Create cache key
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            cache_key = tuple(
                (k, bound_args.arguments[k]) for k in bound_args.arguments
            )
            # Check cache
            if cache_key in self.cache:
                print(f"[{self.name} CACHE] Cache hit")
                self.metrics["cached_hits"] += 1
                self.metrics["successes"] += 1
                self.metrics["total_time"] += time.time() - start_time
                return self.cache[cache_key]
            # Retry logic
            attempts = 0
            while attempts < self.max_retries:
                try:
                    print(f"[{self.name}] Attempt {attempts+1} of {self.max_retries}")
                    result = func(*args, **kwargs)
                    # Cache result
                    self.cache[cache_key] = result
                    # Update metrics
                    self.metrics["successes"] += 1
                    self.metrics["total_time"] += time.time() - start_time
                    return result
                except Exception as e:
                    attempts += 1
                    self.metrics["failures"] += 1
                    print(f"[{self.name} ERROR] {e}. Retrying...")
            # If we reach here, all retries failed
            print(f"[{self.name} ERROR] All retries failed. Exiting function.")
            self.metrics["total_time"] += time.time() - start_time
            raise RuntimeError(
                f"Function {func.__name__} failed after {self.max_retries} attempts"
            )

        return wrapper

    def get_metrics(self):
        """Return pipeline metrics"""
        return self.metrics


# Tests
# if __name__ == "__main__":
#     print("=== Test 1: Function Profiler ===")

#     @FunctionProfiler
#     def fibonacci(n):
#         """Calculate fibonacci number"""
#         if n <= 1:
#             return n
#         return fibonacci(n - 1) + fibonacci(n - 2)

#     result = fibonacci(7)
#     print(f"Result: {result}")
#     print(f"Stats: {fibonacci.get_stats()}\n")

#     print("=== Test 2: Conditional Decorator ===")
#     is_production = False

#     @apply_if(is_production, lambda f: f)  # Simplified decorator for demo
#     def config_value():
#         return "production config"

#     result = config_value()
#     print(f"Result: {result}\n")

#     print("=== Test 3: Decorator with Hooks ===")
#     profiler = DecoratorWithHooks()

#     @profiler
#     def process_data(data):
#         print(f"  Processing: {data}")
#         return data.upper()

#     @profiler.before
#     def setup():
#         print("  [SETUP] Initializing resources")

#     @profiler.after
#     def cleanup():
#         print("  [CLEANUP] Releasing resources")

#     result = process_data("hello")
#     print(f"Result: {result}\n")

#     print("=== Test 4: Smart Decorator ===")

#     @smart_decorator
#     def compute(x, y):
#         """Compute something"""
#         return {"sum": x + y, "product": x * y}

#     result = compute(5, 3)
#     print(f"Result: {result}\n")

#     print("=== Test 5: Metadata Preservation ===")

#     @preserve_metadata
#     def important_function():
#         """An important function"""
#         return "result"

#     print(f"Function name: {important_function.__name__}")
#     print(f"Is decorated: {important_function.is_decorated}")
#     print(f"Decorator: {important_function.decorator_name}\n")

#     print("✅ All tests complete!")

# ========== COMPREHENSIVE TEST SUITE ==========

# if __name__ == "__main__":
#     print("=" * 80)
#     print("COMPREHENSIVE DECORATOR TEST SUITE - EXERCISE 10")
#     print("=" * 80)

#     # ===== TEST 1: Function Profiler - Single Calls =====
#     print("\n" + "=" * 80)
#     print("TEST 1: Function Profiler - Single Calls")
#     print("=" * 80)

#     @FunctionProfiler
#     def fibonacci(n):
#         """Calculate fibonacci number"""
#         if n <= 1:
#             return n
#         return fibonacci(n - 1) + fibonacci(n - 2)

#     result = fibonacci(5)
#     print(f"Result: {result}")
#     print(f"Stats: {fibonacci.get_stats()}\n")

#     # ===== TEST 2: Function Profiler - Multiple Calls =====
#     print("=" * 80)
#     print("TEST 2: Function Profiler - Multiple Calls & Statistics")
#     print("=" * 80)

#     @FunctionProfiler
#     def add(a, b):
#         """Add two numbers"""
#         time.sleep(0.01)
#         return a + b

#     print("Calling add() 5 times with different values...")
#     for i in range(5):
#         result = add(i, i + 1)
#         print(f"  Call {i+1}: add({i}, {i+1}) = {result}")

#     stats = add.get_stats()
#     print(f"\nProfiler Stats:")
#     print(f"  Total calls: {stats['call_count']}")
#     print(f"  Total time: {stats['total_time']:.4f}s")
#     print(f"  Average time: {stats['average_time']:.4f}s")
#     print(f"  Min time: {stats['min_time']:.4f}s")
#     print(f"  Max time: {stats['max_time']:.4f}s\n")

#     # ===== TEST 3: Conditional Decorator - Condition True =====
#     print("=" * 80)
#     print("TEST 3: Conditional Decorator - Applied (condition=True)")
#     print("=" * 80)

#     call_count = 0

#     def count_decorator(func):
#         """Simple decorator that counts calls"""
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             global call_count
#             call_count += 1
#             print(f"  [COUNT] Call #{call_count}")
#             return func(*args, **kwargs)
#         return wrapper

#     is_applied = True

#     @apply_if(is_applied, count_decorator)
#     def operation1():
#         """Operation with decorator applied"""
#         return "result1"

#     operation1()
#     operation1()
#     print(f"Decorator was applied: {call_count > 0}\n")

#     # ===== TEST 4: Conditional Decorator - Condition False =====
#     print("=" * 80)
#     print("TEST 4: Conditional Decorator - Not Applied (condition=False)")
#     print("=" * 80)

#     call_count2 = 0

#     def count_decorator2(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             global call_count2
#             call_count2 += 1
#             print(f"  [COUNT] Call #{call_count2}")
#             return func(*args, **kwargs)
#         return wrapper

#     is_applied2 = False

#     @apply_if(is_applied2, count_decorator2)
#     def operation2():
#         """Operation without decorator"""
#         return "result2"

#     operation2()
#     operation2()
#     print(f"Decorator was applied: {call_count2 > 0}\n")

#     # ===== TEST 5: Decorator with Hooks - Single Hooks =====
#     print("=" * 80)
#     print("TEST 5: Decorator with Hooks - Single Before/After")
#     print("=" * 80)

#     hook_profiler = DecoratorWithHooks()

#     @hook_profiler
#     def process_data(data):
#         """Process data with hooks"""
#         print(f"  [PROCESS] Processing: {data}")
#         return data.upper()

#     @hook_profiler.before
#     def setup():
#         print("  [SETUP] Initializing resources")

#     @hook_profiler.after
#     def cleanup():
#         print("  [CLEANUP] Releasing resources")

#     result = process_data("hello")
#     print(f"Result: {result}\n")

#     # ===== TEST 6: Decorator with Hooks - Multiple Hooks =====
#     print("=" * 80)
#     print("TEST 6: Decorator with Hooks - Multiple Before/After Hooks")
#     print("=" * 80)

#     hook_profiler2 = DecoratorWithHooks()

#     @hook_profiler2
#     def complex_operation():
#         """Operation with multiple hooks"""
#         print("  [OPERATION] Performing complex operation...")
#         return "success"

#     @hook_profiler2.before
#     def log_start():
#         print("  [LOG] Starting operation...")

#     @hook_profiler2.before
#     def validate():
#         print("  [VALIDATE] Validating inputs...")

#     @hook_profiler2.after
#     def log_end():
#         print("  [LOG] Operation completed")

#     @hook_profiler2.after
#     def save_results():
#         print("  [SAVE] Saving results to database...")

#     result = complex_operation()
#     print(f"Result: {result}\n")

#     # ===== TEST 7: Smart Decorator - No Parameters =====
#     print("=" * 80)
#     print("TEST 7: Smart Decorator - No Parameters (Caching Candidate)")
#     print("=" * 80)

#     @smart_decorator
#     def get_config():
#         """Get configuration (no parameters)"""
#         return {"debug": True, "timeout": 30}

#     result = get_config()
#     print(f"Result: {result}\n")

#     # ===== TEST 8: Smart Decorator - Many Parameters =====
#     print("=" * 80)
#     print("TEST 8: Smart Decorator - Many Parameters (Cache Inefficient)")
#     print("=" * 80)

#     @smart_decorator
#     def complex_calc(a, b, c, d, e):
#         """Complex calculation with many parameters"""
#         return {
#             "sum": a + b + c + d + e,
#             "product": a * b * c * d * e
#         }

#     result = complex_calc(1, 2, 3, 4, 5)
#     print(f"Result: {result}\n")

#     # ===== TEST 9: Metadata Preservation =====
#     print("=" * 80)
#     print("TEST 9: Metadata Preservation - Dynamic Decorator Name")
#     print("=" * 80)

#     @preserve_metadata
#     def important_function():
#         """An important function"""
#         return "result"

#     print(f"Function name: {important_function.__name__}")
#     print(f"Function docstring: {important_function.__doc__}")
#     print(f"Is decorated: {important_function.is_decorated}")
#     print(f"Decorator name: {important_function.decorator_name}")
#     print(f"Original function: {important_function.original_function.__name__}\n")

#     # ===== TEST 10: Decorator Chain - Timing + Logging =====
#     print("=" * 80)
#     print("TEST 10: Decorator Chain - Timing + Logging Only")
#     print("=" * 80)

#     def add_slow(a, b):
#         """Slow addition"""
#         time.sleep(0.05)
#         return a + b

#     chained = (DecoratorChain(add_slow)
#                .with_timing()
#                .with_logging()
#                .build())

#     result = chained(5, 3)
#     print(f"Result: {result}\n")

#     # ===== TEST 11: Decorator Chain - All Three Decorators =====
#     print("=" * 80)
#     print("TEST 11: Decorator Chain - Timing + Logging + Caching")
#     print("=" * 80)

#     def expensive_operation(x):
#         """Expensive operation to be cached"""
#         print(f"    [COMPUTE] Computing factorial of {x}...")
#         result = 1
#         for i in range(1, x + 1):
#             result *= i
#         return result

#     chained_full = (DecoratorChain(expensive_operation)
#                     .with_timing()
#                     .with_logging()
#                     .with_caching(max_size=10)
#                     .build())

#     print("First calls (cache misses):")
#     print(f"Result: {chained_full(5)}")
#     print(f"Result: {chained_full(6)}")

#     print("\nSecond calls (cache hits):")
#     print(f"Result: {chained_full(5)}")
#     print(f"Result: {chained_full(6)}\n")

#     # ===== TEST 12: Data Pipeline Step - Successful Execution =====
#     print("=" * 80)
#     print("TEST 12: Data Pipeline Step - Successful Execution")
#     print("=" * 80)

#     step = DataPipelineStep("Transform")

#     @step
#     def transform_data(data):
#         """Transform data in pipeline"""
#         print(f"    [TRANSFORM] Converting to uppercase...")
#         return data.upper()

#     print("First call (cache miss):")
#     result1 = transform_data("hello")
#     print(f"Result: {result1}")

#     print("\nSecond call (cache hit):")
#     result2 = transform_data("hello")
#     print(f"Result: {result2}")

#     print(f"\nPipeline metrics: {step.get_metrics()}\n")

#     # ===== TEST 13: Data Pipeline Step - With Retry =====
#     print("=" * 80)
#     print("TEST 13: Data Pipeline Step - Retry on Failure (Succeeds)")
#     print("=" * 80)

#     step_retry = DataPipelineStep("RetryStep", max_retries=3)

#     attempt_count = 0

#     @step_retry
#     def flaky_operation(x):
#         """Operation that fails the first 2 times"""
#         global attempt_count
#         attempt_count += 1
#         if attempt_count < 3:
#             raise ValueError(f"Simulated failure #{attempt_count}")
#         print(f"    [SUCCESS] Operation succeeded on attempt {attempt_count}")
#         return x * 2

#     try:
#         result = flaky_operation(5)
#         print(f"Result: {result}")
#     except RuntimeError as e:
#         print(f"Failed: {e}")

#     print(f"Pipeline metrics: {step_retry.get_metrics()}\n")

#     # ===== TEST 14: Data Pipeline Step - Max Retries Exceeded =====
#     print("=" * 80)
#     print("TEST 14: Data Pipeline Step - Max Retries Exceeded")
#     print("=" * 80)

#     step_fail = DataPipelineStep("FailStep", max_retries=2)

#     @step_fail
#     def always_fails():
#         """Operation that always fails"""
#         raise ValueError("This always fails!")

#     try:
#         result = always_fails()
#     except RuntimeError as e:
#         print(f"✓ Correctly caught exception after max retries:")
#         print(f"  {e}")

#     print(f"Pipeline metrics: {step_fail.get_metrics()}\n")

#     # ===== TEST 15: Metadata Consistency Across Decorators =====
#     print("=" * 80)
#     print("TEST 15: Metadata Consistency - Verify Wraps Preservation")
#     print("=" * 80)

#     @FunctionProfiler
#     def multi_decorated(a, b):
#         """A function with multiple decorations"""
#         return a + b

#     print(f"Function __name__: {multi_decorated.__name__}")
#     print(f"Function __doc__: {multi_decorated.__doc__}")

#     # Call it to verify it works
#     result = multi_decorated(10, 20)
#     print(f"Result: {result}")
#     print(f"Stats: {multi_decorated.get_stats()}\n")

#     # ===== FINAL SUMMARY =====
#     print("=" * 80)
#     print("✅ ALL TESTS COMPLETE!")
#     print("=" * 80)
#     print("\nTest Coverage Summary:")
#     print("✓ Test 1-2: FunctionProfiler basic and advanced")
#     print("✓ Test 3-4: Conditional decorators (applied/not applied)")
#     print("✓ Test 5-6: Hooks with single and multiple before/after")
#     print("✓ Test 7-8: Smart decorator with different parameter counts")
#     print("✓ Test 9: Metadata preservation with dynamic naming")
#     print("✓ Test 10-11: Decorator chains with various combinations")
#     print("✓ Test 12: Data pipeline successful execution")
#     print("✓ Test 13: Data pipeline with retry logic (succeeds)")
#     print("✓ Test 14: Data pipeline max retries exceeded (fails)")
#     print("✓ Test 15: Metadata consistency verification")
#     print("\n✅ All 7 decorator patterns fully tested and working!")
