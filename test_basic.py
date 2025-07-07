#!/usr/bin/env python3
# ruff: noqa: T201
"""Basic test script to verify pyutils functionality.

This script tests the basic functionality of all modules in pyutils
to ensure they are working correctly after porting from jsutils.
"""

import asyncio
import sys
from pathlib import Path

import pytest


# Add src to path so we can import pyutils
sys.path.insert(0, str(Path(__file__).parent / "src"))

try:
    import pyutils
    from pyutils import array, async_utils, bytes_utils, function, math, object, string

    print("✅ Successfully imported pyutils and all modules")
except ImportError as e:
    print(f"❌ Failed to import pyutils: {e}")
    sys.exit(1)


def test_array_functions():
    """Test array utility functions."""
    print("\n🧪 Testing array functions...")

    # Test range_list
    result = array.range_list(5)
    assert result == [0, 1, 2, 3, 4], f"Expected [0,1,2,3,4], got {result}"
    print("  ✅ range_list works")

    # Test chunk
    result = array.chunk([1, 2, 3, 4, 5], 2)
    assert result == [[1, 2], [3, 4], [5]], f"Expected [[1,2],[3,4],[5]], got {result}"
    print("  ✅ chunk works")

    # Test unique
    result = array.unique([1, 2, 2, 3, 3, 3])
    assert result == [1, 2, 3], f"Expected [1,2,3], got {result}"
    print("  ✅ unique works")

    # Test first and last
    assert array.first([1, 2, 3]) == 1
    assert array.last([1, 2, 3]) == 3
    print("  ✅ first and last work")

    print("✅ All array functions passed")


def test_string_functions():
    """Test string utility functions."""
    print("\n🧪 Testing string functions...")

    # Test case conversions
    assert string.camel_case("hello world") == "helloWorld"
    assert string.snake_case("helloWorld") == "hello_world"
    assert string.dash_case("hello world") == "hello-world"
    assert string.pascal_case("hello world") == "HelloWorld"
    print("  ✅ Case conversion functions work")

    # Test capitalize
    assert string.capitalize("hello") == "Hello"
    print("  ✅ capitalize works")

    # Test trim
    assert string.trim("  hello  ") == "hello"
    assert string.trim("xxhelloxx", "x") == "hello"
    print("  ✅ trim works")

    # Test slugify
    assert string.slugify("Hello World!") == "hello-world"
    print("  ✅ slugify works")

    # Test UUID generation
    uuid = string.generate_uuid()
    assert len(uuid) == 36
    assert uuid.count("-") == 4
    print("  ✅ generate_uuid works")

    print("✅ All string functions passed")


def test_math_functions():
    """Test math utility functions."""
    print("\n🧪 Testing math functions...")

    # Test clamp
    assert math.clamp(5, 0, 10) == 5
    assert math.clamp(-5, 0, 10) == 0
    assert math.clamp(15, 0, 10) == 10
    print("  ✅ clamp works")

    # Test lerp
    assert math.lerp(0, 10, 0.5) == 5.0
    print("  ✅ lerp works")

    # Test is_even and is_odd
    assert math.is_even(4)
    assert math.is_odd(5)
    print("  ✅ is_even and is_odd work")

    # Test gcd and lcm
    assert math.gcd(12, 8) == 4
    assert math.lcm(4, 6) == 12
    print("  ✅ gcd and lcm work")

    # Test factorial
    assert math.factorial(5) == 120
    print("  ✅ factorial works")

    # Test is_prime
    assert math.is_prime(7)
    assert not math.is_prime(8)
    print("  ✅ is_prime works")

    print("✅ All math functions passed")


def test_object_functions():
    """Test object utility functions."""
    print("\n🧪 Testing object functions...")

    # Test pick
    obj = {"a": 1, "b": 2, "c": 3}
    result = object.pick(obj, ["a", "c"])
    assert result == {"a": 1, "c": 3}
    print("  ✅ pick works")

    # Test omit
    result = object.omit(obj, ["b"])
    assert result == {"a": 1, "c": 3}
    print("  ✅ omit works")

    # Test merge
    obj1 = {"a": 1, "b": 2}
    obj2 = {"b": 3, "c": 4}
    result = object.merge(obj1, obj2)
    assert result == {"a": 1, "b": 3, "c": 4}
    print("  ✅ merge works")

    # Test flatten_dict
    nested = {"a": {"b": {"c": 1}}}
    result = object.flatten_dict(nested)
    assert result == {"a.b.c": 1}
    print("  ✅ flatten_dict works")

    # Test get_nested_value
    result = object.get_nested_value(nested, "a.b.c")
    assert result == 1
    print("  ✅ get_nested_value works")

    print("✅ All object functions passed")


def test_function_utilities():
    """Test function utility decorators."""
    print("\n🧪 Testing function utilities...")

    # Test memoize
    call_count = 0

    @function.memoize
    def expensive_func(x):
        nonlocal call_count
        call_count += 1
        return x * x

    result1 = expensive_func(5)
    result2 = expensive_func(5)  # Should use cache
    assert result1 == result2 == 25
    assert call_count == 1  # Should only be called once
    print("  ✅ memoize works")

    # Test once
    call_count = 0

    @function.once
    def init_func():
        nonlocal call_count
        call_count += 1
        return "initialized"

    result1 = init_func()
    result2 = init_func()  # Should return cached result
    assert result1 == result2 == "initialized"
    assert call_count == 1  # Should only be called once
    print("  ✅ once works")

    print("✅ All function utilities passed")


@pytest.mark.asyncio()
async def test_async_functions():
    """Test async utility functions."""
    print("\n🧪 Testing async functions...")

    # Test sleep_async
    import time

    start = time.time()
    await async_utils.sleep_async(0.1)
    elapsed = time.time() - start
    assert 0.09 <= elapsed <= 0.15  # Allow some tolerance
    print("  ✅ sleep_async works")

    # 测试 delay
    result = await async_utils.delay("hello", 0.05)
    assert result == "hello"
    print("  ✅ delay works")

    # Test race
    async def slow_task():
        await asyncio.sleep(0.2)
        return "slow"

    async def fast_task():
        await asyncio.sleep(0.05)
        return "fast"

    result = await async_utils.race(slow_task(), fast_task())
    assert result == "fast"
    print("  ✅ race works")

    # Test map_async
    async def double(x):
        await asyncio.sleep(0.01)
        return x * 2

    result = await async_utils.map_async(double, [1, 2, 3], concurrency=2)
    assert result == [2, 4, 6]
    print("  ✅ map_async works")

    print("✅ All async functions passed")


def test_bytes_utilities():
    """Test bytes utility functions."""
    print("\n🧪 Testing bytes utilities...")

    # Test Bytes.format
    assert bytes_utils.Bytes.format(1024) == "1 KB"
    assert bytes_utils.Bytes.format(1536) == "1.5 KB"
    print("  ✅ Bytes.format works")

    # Test Bytes.parse
    assert bytes_utils.Bytes.parse("1 KB") == 1024
    assert bytes_utils.Bytes.parse("1.5 MB") == 1572864
    print("  ✅ Bytes.parse works")

    # Test bytes_util convenience function
    assert bytes_utils.bytes_util(1024) == "1 KB"
    assert bytes_utils.bytes_util("1 KB") == 1024
    print("  ✅ bytes_util works")

    # Test humanize_bytes
    assert bytes_utils.humanize_bytes(1024) == "1 KB"
    print("  ✅ humanize_bytes works")

    print("✅ All bytes utilities passed")


def test_imports():
    """Test that imports work correctly."""
    print("\n🧪 Testing imports...")

    # Test direct imports from pyutils
    from pyutils import camel_case, chunk, clamp, pick

    # Test that they work
    assert chunk([1, 2, 3, 4], 2) == [[1, 2], [3, 4]]
    assert camel_case("hello world") == "helloWorld"
    assert clamp(5, 0, 10) == 5
    assert pick({"a": 1, "b": 2}, ["a"]) == {"a": 1}

    print("  ✅ Direct imports work")
    print("✅ All import tests passed")


def main():
    """Run all tests."""
    print("🚀 Starting pyutils test suite...")
    print(f"Python version: {sys.version}")
    print(f"pyutils version: {pyutils.__version__}")

    try:
        # Run synchronous tests
        test_array_functions()
        test_string_functions()
        test_math_functions()
        test_object_functions()
        test_function_utilities()
        test_bytes_utilities()
        test_imports()

        # Run async tests
        asyncio.run(test_async_functions())

        print("\n🎉 All tests passed! pyutils is working correctly.")
        print("\n📊 Summary:")
        print("  ✅ Array utilities: Working")
        print("  ✅ String utilities: Working")
        print("  ✅ Math utilities: Working")
        print("  ✅ Object utilities: Working")
        print("  ✅ Function utilities: Working")
        print("  ✅ Async utilities: Working")
        print("  ✅ Bytes utilities: Working")
        print("  ✅ Import system: Working")

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
