#!/usr/bin/env python3
"""Performance benchmark for collection module functions."""

import time
from typing import Any

from src.pyutils.collection import (
    at,
    every,
    fill,
    find_index,
    flat_map,
    group_by,
    includes,
    some,
    splice,
    to_reversed,
    to_sorted,
)


def benchmark_function(func: Any, *args: Any, iterations: int = 10000) -> float:
    """Benchmark a function with given arguments."""
    start_time = time.perf_counter()
    for _ in range(iterations):
        func(*args)
    end_time = time.perf_counter()
    return (end_time - start_time) / iterations * 1000  # ms per operation


def main() -> None:
    """Run performance benchmarks."""
    print("Collection Module Performance Benchmarks")
    print("=" * 50)

    # Test data
    small_list = list(range(100))
    medium_list = list(range(1000))
    large_list = list(range(10000))

    benchmarks = [
        ("includes (small)", includes, small_list, 50),
        ("includes (medium)", includes, medium_list, 500),
        ("find_index (small)", find_index, small_list, lambda x: x > 50),
        ("find_index (medium)", find_index, medium_list, lambda x: x > 500),
        ("some (small)", some, small_list, lambda x: x > 50),
        ("some (medium)", some, medium_list, lambda x: x > 500),
        ("every (small)", every, small_list, lambda x: x >= 0),
        ("every (medium)", every, medium_list, lambda x: x >= 0),
        ("flat_map (small)", flat_map, small_list[:10], lambda x: [x, x * 2]),
        ("at (small)", at, small_list, 50),
        ("at (medium)", at, medium_list, 500),
        ("to_reversed (small)", to_reversed, small_list),
        ("to_reversed (medium)", to_reversed, medium_list),
        ("to_sorted (small)", to_sorted, small_list.copy()),
        ("group_by (small)", group_by, small_list, lambda x: x % 10),
    ]

    for name, func, *args in benchmarks:
        try:
            avg_time = benchmark_function(func, *args, iterations=1000)
            print(f"{name:<25}: {avg_time:.4f} ms/op")
        except Exception as e:
            print(f"{name:<25}: Error - {e}")

    print("\nBenchmark completed successfully!")


if __name__ == "__main__":
    main()