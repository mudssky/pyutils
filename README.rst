=======
pyutils
=======


.. image:: https://img.shields.io/pypi/v/pyutils.svg
        :target: https://pypi.python.org/pypi/pyutils

.. image:: https://img.shields.io/travis/mudssky/pyutils.svg
        :target: https://travis-ci.com/mudssky/pyutils

.. image:: https://readthedocs.org/projects/pyutils/badge/?version=latest
        :target: https://pyutils.readthedocs.io/en/latest/?version=latest
        :alt: Documentation Status


Python通用工具库 - 提供丰富的实用函数和工具类
============================================

pyutils是一个功能丰富的Python工具库，提供了大量常用的实用函数，涵盖数组操作、字符串处理、数学计算、对象操作、函数工具、异步编程和字节处理等多个领域。

* 免费开源: MIT许可证
* 文档地址: https://pyutils.readthedocs.io
* 支持Python 3.6+


快速开始
--------

安装::

    pip install pyutils

基本使用::

    from pyutils import array, string, math
    
    # 数组操作
    result = array.chunk([1, 2, 3, 4, 5], 2)  # [[1, 2], [3, 4], [5]]
    
    # 字符串处理
    camel = string.camel_case("hello_world")  # "helloWorld"
    
    # 数学计算
    random_num = math.random_int(1, 100)  # 1-100之间的随机整数


主要功能模块
-----------

**数组工具 (array)**

* ``chunk`` - 将数组分块
* ``unique`` - 数组去重
* ``shuffle`` - 数组随机排序
* ``diff`` - 数组差集
* ``fork`` - 数组分组
* ``zip_object`` - 创建对象映射
* 更多数组操作函数...

**字符串工具 (string)**

* ``camel_case`` - 转换为驼峰命名
* ``snake_case`` - 转换为下划线命名
* ``pascal_case`` - 转换为帕斯卡命名
* ``slugify`` - 生成URL友好字符串
* ``fuzzy_match`` - 模糊匹配
* ``generate_uuid`` - 生成UUID
* 更多字符串处理函数...

**数学工具 (math)**

* ``clamp`` - 数值限制
* ``lerp`` - 线性插值
* ``normalize`` - 数值归一化
* ``fibonacci`` - 斐波那契数列
* ``is_prime`` - 质数判断
* ``gcd/lcm`` - 最大公约数/最小公倍数
* 更多数学计算函数...

**对象工具 (object)**

* ``pick/omit`` - 对象属性选择/排除
* ``merge`` - 深度合并对象
* ``flatten_dict`` - 扁平化字典
* ``get_nested_value`` - 获取嵌套值
* ``deep_copy`` - 深度复制
* 更多对象操作函数...

**函数工具 (function)**

* ``memoize`` - 函数记忆化
* ``debounce`` - 防抖装饰器
* ``throttle`` - 节流装饰器
* ``with_retry`` - 重试装饰器
* ``once`` - 单次执行装饰器
* 更多函数增强工具...

**异步工具 (async_utils)**

* ``sleep_async`` - 异步延迟
* ``timeout`` - 超时控制
* ``race`` - 竞态执行
* ``gather_with_concurrency`` - 并发控制
* ``map_async`` - 异步映射
* ``batch_process`` - 批量处理
* 更多异步编程工具...

**字节工具 (bytes)**

* ``Bytes`` - 字节处理类
* ``humanize_bytes`` - 人性化字节显示
* ``parse_bytes`` - 字节字符串解析
* 字节单位转换工具


使用示例
--------

**数组操作示例**::

    from pyutils import array
    
    # 数组分块
    chunks = array.chunk([1, 2, 3, 4, 5, 6], 2)
    # 结果: [[1, 2], [3, 4], [5, 6]]
    
    # 数组去重并保持顺序
    unique_items = array.unique([1, 2, 2, 3, 1, 4])
    # 结果: [1, 2, 3, 4]
    
    # 根据条件分组
    evens, odds = array.fork([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
    # evens: [2, 4], odds: [1, 3, 5]

**字符串处理示例**::

    from pyutils import string
    
    # 命名风格转换
    camel = string.camel_case("hello_world_example")  # "helloWorldExample"
    snake = string.snake_case("HelloWorldExample")   # "hello_world_example"
    pascal = string.pascal_case("hello-world")       # "HelloWorld"
    
    # URL友好字符串
    slug = string.slugify("Hello World! 你好世界")    # "hello-world"
    
    # 模糊匹配
    score = string.fuzzy_match("hello", "helo")      # 0.8

**异步编程示例**::

    import asyncio
    from pyutils import async_utils
    
    async def example():
        # 异步延迟
        await async_utils.sleep_async(1.0)
        
        # 竞态执行，返回最快完成的结果
        async def fast(): 
            await asyncio.sleep(0.1)
            return "fast"
        async def slow(): 
            await asyncio.sleep(1.0)
            return "slow"
            
        result = await async_utils.race(fast(), slow())  # "fast"
        
        # 带并发限制的异步映射
        async def process(x):
            await asyncio.sleep(0.1)
            return x * 2
            
        results = await async_utils.map_async(
            process, [1, 2, 3, 4, 5], concurrency=2
        )  # [2, 4, 6, 8, 10]

**函数增强示例**::

    from pyutils.function import memoize, debounce, with_retry
    
    # 记忆化缓存
    @memoize
    def expensive_calculation(n):
        return sum(range(n))
    
    # 防抖处理
    @debounce(delay=1.0)
    def search_handler(query):
        print(f"Searching for: {query}")
    
    # 自动重试
    @with_retry(max_attempts=3, delay=1.0)
    def unreliable_api_call():
        # 可能失败的API调用
        pass


开发和贡献
----------

克隆项目::

    git clone https://github.com/mudssky/pyutils.git
    cd pyutils

安装开发依赖::

    pip install -e .[dev]

运行测试::

    pytest
    
    # 或运行基础测试
    python test_basic.py

代码检查::

    ruff check .
    mypy .


许可证
------

本项目采用MIT许可证 - 详见 `LICENSE <LICENSE>`_ 文件。


致谢
----

本项目使用 Cookiecutter_ 和 `audreyr/cookiecutter-pypackage`_ 项目模板创建。

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
