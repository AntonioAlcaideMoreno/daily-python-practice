"""
Comprehensive test suite for decorators_e010: Advanced Decorator Composition & Patterns

Tests cover:
- FunctionProfiler: timing, call count, statistics aggregation
- DecoratorChain: builder pattern with timing, logging, caching
- apply_if: conditional decorator application
- DecoratorWithHooks: before/after execution hooks
- smart_decorator: adaptive behavior based on function signature
- preserve_metadata: metadata preservation and augmentation
- DataPipelineStep: complex real-world pipeline with retry logic and caching
"""

import sys
from functools import wraps
from pathlib import Path

import pytest

# Ensure src/ is on sys.path for consistent imports across environments (different OS)
repo_src = Path(__file__).resolve().parent.parent
if str(repo_src) not in sys.path:
    sys.path.insert(0, str(repo_src))

from exercises.decorators_e010 import (
    DataPipelineStep,
    DecoratorChain,
    DecoratorWithHooks,
    FunctionProfiler,
    apply_if,
    preserve_metadata,
    smart_decorator,
)


# ========== TEST 1: FunctionProfiler - Single Calls =====
def test_function_profiler_single_call():
    """Test FunctionProfiler with a single function call."""

    @FunctionProfiler
    def fibonacci(n):
        """Calculate fibonacci number"""
        if n <= 1:
            return n
        return fibonacci(n - 1) + fibonacci(n - 2)

    result = fibonacci(5)
    assert result == 5
    stats = fibonacci.get_stats()
    assert stats["call_count"] >= 1
    assert "total_time" in stats
    assert "average_time" in stats


# ========== TEST 2: FunctionProfiler - Multiple Calls & Statistics =====
def test_function_profiler_multiple_calls():
    """Test FunctionProfiler with multiple calls and verify statistics."""

    @FunctionProfiler
    def add(a, b):
        """Add two numbers"""
        return a + b

    # Make 5 calls with different values
    for i in range(5):
        result = add(i, i + 1)
        assert result == 2 * i + 1

    stats = add.get_stats()
    assert stats["call_count"] == 5
    assert stats["total_time"] >= 0
    assert stats["average_time"] == stats["total_time"] / 5
    assert stats["min_time"] <= stats["average_time"] <= stats["max_time"]
    assert stats["function_name"] == "add"


# ========== TEST 3: Conditional Decorator - Applied =====
def test_apply_if_condition_true():
    """Test conditional decorator application when condition is True."""
    call_count = 0

    def count_decorator(func):
        """Simple decorator that counts calls"""

        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return func(*args, **kwargs)

        return wrapper

    @apply_if(True, count_decorator)
    def operation1():
        """Operation with decorator applied"""
        return "result1"

    operation1()
    operation1()
    assert call_count == 2, "Decorator should have been applied"


# ========== TEST 4: Conditional Decorator - Not Applied =====
def test_apply_if_condition_false():
    """Test conditional decorator when condition is False."""
    call_count = 0

    def count_decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            return func(*args, **kwargs)

        return wrapper

    @apply_if(False, count_decorator)
    def operation2():
        """Operation without decorator"""
        return "result2"

    operation2()
    operation2()
    assert call_count == 0, "Decorator should not have been applied"


# ========== TEST 5: Decorator with Hooks - Single Hooks =====
def test_decorator_with_hooks_single():
    """Test DecoratorWithHooks with single before/after hooks."""
    hook_profiler = DecoratorWithHooks()
    execution_log = []

    @hook_profiler
    def process_data(data):
        """Process data with hooks"""
        execution_log.append("process")
        return data.upper()

    @hook_profiler.before
    def setup():
        execution_log.append("setup")

    @hook_profiler.after
    def cleanup():
        execution_log.append("cleanup")

    result = process_data("hello")
    assert result == "HELLO"
    assert execution_log == ["setup", "process", "cleanup"]


# ========== TEST 6: Decorator with Hooks - Multiple Hooks =====
def test_decorator_with_hooks_multiple():
    """Test DecoratorWithHooks with multiple before/after hooks."""
    hook_profiler = DecoratorWithHooks()
    execution_order = []

    @hook_profiler
    def complex_operation():
        """Operation with multiple hooks"""
        execution_order.append("operation")
        return "success"

    @hook_profiler.before
    def log_start():
        execution_order.append("log_start")

    @hook_profiler.before
    def validate():
        execution_order.append("validate")

    @hook_profiler.after
    def log_end():
        execution_order.append("log_end")

    @hook_profiler.after
    def save_results():
        execution_order.append("save_results")

    result = complex_operation()
    assert result == "success"
    # Verify execution order: all before hooks, then operation, then all after hooks
    assert execution_order[:2] == ["log_start", "validate"]
    assert execution_order[2] == "operation"
    assert execution_order[3:] == ["log_end", "save_results"]


# ========== TEST 7: Smart Decorator - No Parameters =====
def test_smart_decorator_no_parameters():
    """Test smart_decorator with a function that has no parameters."""

    @smart_decorator
    def get_config():
        """Get configuration (no parameters)"""
        return {"debug": True, "timeout": 30}

    result = get_config()
    assert isinstance(result, dict)
    assert result["debug"] is True
    assert result["timeout"] == 30


# ========== TEST 8: Smart Decorator - Many Parameters =====
def test_smart_decorator_many_parameters():
    """Test smart_decorator with many parameters (cache inefficient)."""

    @smart_decorator
    def complex_calc(a, b, c, d, e):
        """Complex calculation with many parameters"""
        return {"sum": a + b + c + d + e, "product": a * b * c * d * e}

    result = complex_calc(1, 2, 3, 4, 5)
    assert result["sum"] == 15
    assert result["product"] == 120


# ========== TEST 9: Metadata Preservation =====
def test_preserve_metadata():
    """Test metadata preservation with dynamic decorator name."""

    @preserve_metadata
    def important_function():
        """An important function"""
        return "result"

    assert important_function.__name__ == "important_function"
    assert important_function.__doc__ == "An important function"
    assert important_function.is_decorated is True
    assert important_function.decorator_name == "preserve_metadata"
    assert important_function.original_function.__name__ == "important_function"
    assert important_function() == "result"


# ========== TEST 10: Decorator Chain - Timing + Logging =====
def test_decorator_chain_timing_logging():
    """Test DecoratorChain with timing and logging decorators."""

    def add_slow(a, b):
        """Slow addition"""
        return a + b

    chained = DecoratorChain(add_slow).with_timing().with_logging().build()

    result = chained(5, 3)
    assert result == 8


# ========== TEST 11: Decorator Chain - All Three Decorators =====
def test_decorator_chain_all_decorators():
    """Test DecoratorChain with timing, logging, and caching."""
    call_count = 0

    def expensive_operation(x):
        """Expensive operation to be cached"""
        nonlocal call_count
        call_count += 1
        result = 1
        for i in range(1, x + 1):
            result *= i
        return result

    chained_full = (
        DecoratorChain(expensive_operation)
        .with_timing()
        .with_logging()
        .with_caching(max_size=10)
        .build()
    )

    # First calls (cache misses)
    result1 = chained_full(5)
    result2 = chained_full(6)
    assert result1 == 120  # 5!
    assert result2 == 720  # 6!
    first_call_count = call_count

    # Second calls (cache hits) — should not increment call_count
    result3 = chained_full(5)
    result4 = chained_full(6)
    assert result3 == 120
    assert result4 == 720
    assert call_count == first_call_count, "Cache should have prevented re-execution"


# ========== TEST 12: Data Pipeline Step - Successful Execution =====
def test_data_pipeline_step_success():
    """Test DataPipelineStep with successful execution and caching."""
    step = DataPipelineStep("Transform")

    @step
    def transform_data(data):
        """Transform data in pipeline"""
        return data.upper()

    # First call (cache miss)
    result1 = transform_data("hello")
    assert result1 == "HELLO"
    metrics1 = step.get_metrics()
    assert metrics1["calls"] == 1
    assert metrics1["successes"] == 1
    assert metrics1["cached_hits"] == 0

    # Second call (cache hit)
    result2 = transform_data("hello")
    assert result2 == "HELLO"
    metrics2 = step.get_metrics()
    assert metrics2["calls"] == 2
    assert metrics2["cached_hits"] == 1


# ========== TEST 13: Data Pipeline Step - Retry Success =====
def test_data_pipeline_step_retry_success():
    """Test DataPipelineStep retry logic that eventually succeeds."""
    step_retry = DataPipelineStep("RetryStep", max_retries=3)
    attempt_count = 0

    @step_retry
    def flaky_operation(x):
        """Operation that fails the first 2 times"""
        nonlocal attempt_count
        attempt_count += 1
        if attempt_count < 3:
            raise ValueError(f"Simulated failure #{attempt_count}")
        return x * 2

    result = flaky_operation(5)
    assert result == 10
    metrics = step_retry.get_metrics()
    assert metrics["successes"] == 1
    assert metrics["calls"] == 1


# ========== TEST 14: Data Pipeline Step - Max Retries Exceeded =====
def test_data_pipeline_step_retry_failure():
    """Test DataPipelineStep when max retries are exceeded."""
    step_fail = DataPipelineStep("FailStep", max_retries=2)

    @step_fail
    def always_fails():
        """Operation that always fails"""
        raise ValueError("This always fails!")

    with pytest.raises(RuntimeError) as exc_info:
        always_fails()

    assert "failed after 2 attempts" in str(exc_info.value)
    metrics = step_fail.get_metrics()
    assert metrics["failures"] > 0


# ========== TEST 15: Metadata Consistency Across Decorators =====
def test_metadata_consistency():
    """Test metadata consistency with FunctionProfiler."""

    @FunctionProfiler
    def multi_decorated(a, b):
        """A function with multiple decorations"""
        return a + b

    assert multi_decorated.__name__ == "multi_decorated"
    assert multi_decorated.__doc__ == "A function with multiple decorations"
    result = multi_decorated(10, 20)
    assert result == 30
    stats = multi_decorated.get_stats()
    assert stats["call_count"] == 1
    assert stats["function_name"] == "multi_decorated"
