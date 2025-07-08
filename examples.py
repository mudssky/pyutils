#!/usr/bin/env python3
"""
pyutils 使用示例

这个脚本展示了 pyutils 库的主要功能和使用方法。
"""

import asyncio
import os
import sys


# 添加 src 目录到 Python 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from pyutils import (
    array,
    async_utils,
    bytes,
    function,
    math,
    object,
    string,
)


def demo_array_functions():
    """演示数组工具函数"""
    print("\n🔢 数组工具演示")
    print("=" * 50)

    # 数组分块
    data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    chunks = array.chunk(data, 3)
    print(f"chunk([1,2,3,4,5,6,7,8,9], 3) = {chunks}")

    # 数组去重
    duplicates = [1, 2, 2, 3, 1, 4, 3, 5]
    unique_items = array.unique(duplicates)
    print(f"unique([1,2,2,3,1,4,3,5]) = {unique_items}")

    # 数组分组
    numbers = [1, 2, 3, 4, 5, 6]
    evens, odds = array.fork(numbers, lambda x: x % 2 == 0)
    print(f"fork([1,2,3,4,5,6], is_even) = evens: {evens}, odds: {odds}")

    # 数组差集
    list1 = [1, 2, 3, 4, 5]
    list2 = [3, 4, 5, 6, 7]
    difference = array.diff(list1, list2)
    print(f"diff([1,2,3,4,5], [3,4,5,6,7]) = {difference}")

    # 创建对象映射
    keys = ["name", "age", "city"]
    values = ["Alice", 25, "Beijing"]
    obj = array.zip_object(keys, values)
    print(f"zip_object(['name','age','city'], ['Alice',25,'Beijing']) = {obj}")


def demo_string_functions():
    """演示字符串工具函数"""
    print("\n📝 字符串工具演示")
    print("=" * 50)

    # 命名风格转换
    text = "hello_world_example"
    print(f"原始字符串: {text}")
    print(f"camel_case: {string.camel_case(text)}")
    print(f"pascal_case: {string.pascal_case(text)}")
    print(f"snake_case: {string.snake_case('HelloWorldExample')}")
    print(f"dash_case: {string.dash_case(text)}")

    # URL友好字符串
    title = "Hello World! 这是一个测试 123"
    slug = string.slugify(title)
    print(f"slugify('{title}') = '{slug}'")

    # 模糊匹配
    score1 = string.fuzzy_match("hello", "helo")
    score2 = string.fuzzy_match("python", "pyton")
    print(f"fuzzy_match('hello', 'helo') = {score1:.2f}")
    print(f"fuzzy_match('python', 'pyton') = {score2:.2f}")

    # 生成UUID和随机码
    uuid = string.generate_uuid()
    code = string.generate_base62_code(8)
    print(f"generate_uuid() = {uuid}")
    print(f"generate_base62_code(8) = {code}")

    # 字符串截断
    long_text = "这是一个很长的文本,需要被截断处理"
    truncated = string.truncate(long_text, 10)
    print(f"truncate('{long_text}', 10) = '{truncated}'")


def demo_math_functions():
    """演示数学工具函数"""
    print("\n🧮 数学工具演示")
    print("=" * 50)

    # 数值限制
    value = 150
    clamped = math.clamp(value, 0, 100)
    print(f"clamp(150, 0, 100) = {clamped}")

    # 线性插值
    interpolated = math.lerp(0, 100, 0.5)
    print(f"lerp(0, 100, 0.5) = {interpolated}")

    # 数值归一化
    normalized = math.normalize(75, 0, 100)
    print(f"normalize(75, 0, 100) = {normalized}")

    # 角度转换
    radians = math.degrees_to_radians(90)
    degrees = math.radians_to_degrees(radians)
    print(f"degrees_to_radians(90) = {radians:.4f}")
    print(f"radians_to_degrees({radians:.4f}) = {degrees}")

    # 数学函数
    print(f"fibonacci(10) = {math.fibonacci(10)}")
    print(f"factorial(5) = {math.factorial(5)}")
    print(f"is_prime(17) = {math.is_prime(17)}")
    print(f"gcd(48, 18) = {math.gcd(48, 18)}")
    print(f"lcm(12, 8) = {math.lcm(12, 8)}")

    # 随机数
    random_num = math.random_int(1, 100)
    random_item = math.get_random_item_from_array(["apple", "banana", "orange"])
    print(f"random_int(1, 100) = {random_num}")
    print(f"get_random_item_from_array(['apple','banana','orange']) = {random_item}")


def demo_object_functions():
    """演示对象工具函数"""
    print("\n🏗️ 对象工具演示")
    print("=" * 50)

    # 创建测试对象
    person = {
        "name": "Alice",
        "age": 25,
        "city": "Beijing",
        "email": "alice@example.com",
        "phone": "123-456-7890",
    }

    # 选择和排除属性
    basic_info = object.pick(person, ["name", "age"])
    contact_info = object.omit(person, ["name", "age"])
    print(f"pick(person, ['name', 'age']) = {basic_info}")
    print(f"omit(person, ['name', 'age']) = {contact_info}")

    # 对象合并
    extra_info = {"country": "China", "occupation": "Engineer"}
    merged = object.merge(person, extra_info)
    print(f"merge(person, extra_info) = {merged}")

    # 嵌套对象操作
    nested = {
        "user": {
            "profile": {
                "name": "Bob",
                "settings": {"theme": "dark", "language": "zh-CN"},
            }
        }
    }

    # 获取嵌套值
    theme = object.get_nested_value(nested, "user.profile.settings.theme")
    print(f"get_nested_value(nested, 'user.profile.settings.theme') = {theme}")

    # 扁平化字典
    flattened = object.flatten_dict(nested)
    print(f"flatten_dict(nested) = {flattened}")


def demo_function_utilities():
    """演示函数工具"""
    print("\n⚙️ 函数工具演示")
    print("=" * 50)

    # 记忆化装饰器
    @function.memoize
    def expensive_calculation(n):
        print(f"  计算 {n} 的平方...")
        return n * n

    print("使用 memoize 装饰器:")
    print("第一次调用 expensive_calculation(5):")
    result1 = expensive_calculation(5)
    print(f"结果: {result1}")

    print("第二次调用 expensive_calculation(5) (应该使用缓存):")
    result2 = expensive_calculation(5)
    print(f"结果: {result2}")

    # 单次执行装饰器
    @function.once
    def initialize_system():
        print("  系统初始化完成!")
        return "initialized"

    print("\n使用 once 装饰器:")
    print("第一次调用 initialize_system():")
    initialize_system()
    print("第二次调用 initialize_system() (应该被忽略):")
    initialize_system()


async def demo_async_functions():
    """演示异步工具函数"""
    print("\n⚡ 异步工具演示")
    print("=" * 50)

    # 异步延迟
    print("异步延迟 0.5 秒...")
    await async_utils.sleep_async(0.5)
    print("延迟完成!")

    # 延迟返回值
    print("\n延迟返回值:")
    result = await async_utils.delay("Hello Async!", 0.2)
    print(f"delay('Hello Async!', 0.2) = {result}")

    # 竞态执行
    async def fast_task():
        await asyncio.sleep(0.1)
        return "fast"

    async def slow_task():
        await asyncio.sleep(0.5)
        return "slow"

    print("\n竞态执行 (race):")
    winner = await async_utils.race(fast_task(), slow_task())
    print(f"race(fast_task(), slow_task()) = {winner}")

    # 异步映射
    async def double_async(x):
        await asyncio.sleep(0.05)  # 模拟异步操作
        return x * 2

    print("\n异步映射:")
    numbers = [1, 2, 3, 4, 5]
    doubled = await async_utils.map_async(double_async, numbers, concurrency=2)
    print(f"map_async(double_async, [1,2,3,4,5], concurrency=2) = {doubled}")


def demo_bytes_utilities():
    """演示字节工具"""
    print("\n💾 字节工具演示")
    print("=" * 50)

    # 字节格式化
    byte_sizes = [1024, 1048576, 1073741824, 1099511627776]

    for size in byte_sizes:
        formatted = bytes.humanize_bytes(size)
        print(f"humanize_bytes({size}) = {formatted}")

    # 字节解析
    byte_strings = ["1KB", "2.5MB", "1.2GB", "500B"]

    print("\n字节字符串解析:")
    for byte_str in byte_strings:
        parsed = bytes.parse_bytes(byte_str)
        print(f"parse_bytes('{byte_str}') = {parsed} bytes")

    # Bytes 类使用
    print("\nBytes 类使用:")
    b = bytes.Bytes()

    # 转换和格式化
    size_in_bytes = 2048
    formatted = b.format(size_in_bytes)
    print(f"Bytes().format(2048) = {formatted}")

    # 单位转换
    kb_value = b.to_kb(2048)
    mb_value = b.to_mb(2048)
    print(f"Bytes().to_kb(2048) = {kb_value} KB")
    print(f"Bytes().to_mb(2048) = {mb_value} MB")


def main():
    """主函数"""
    print("🎉 欢迎使用 pyutils 工具库!")
    print("这里展示了库中主要功能的使用示例。")

    try:
        # 演示各个模块
        demo_array_functions()
        demo_string_functions()
        demo_math_functions()
        demo_object_functions()
        demo_function_utilities()
        demo_bytes_utilities()

        # 演示异步功能
        print("\n开始异步功能演示...")
        asyncio.run(demo_async_functions())

        print("\n✅ 所有演示完成!")
        print("\n📚 更多功能请查看文档: https://pyutils.readthedocs.io")

    except Exception as e:
        print(f"\n❌ 演示过程中出现错误: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
