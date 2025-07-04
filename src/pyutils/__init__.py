"""Top-level package for pyutils.

A comprehensive Python utility library providing functions for array manipulation,
string processing, mathematical operations, object handling, function utilities,
asynchronous operations, and byte processing.

Ported from the jsutils JavaScript library to provide similar functionality in Python.
"""

__author__ = """mudssky"""
__email__ = 'mudssky@gmail.com'
__version__ = '0.1.0'

# Import all modules
from . import array
from . import string
from . import math
from . import object
from . import function
from . import async_utils
from . import bytes as bytes_utils

# Import commonly used functions for convenience
from .array import (
    range_list,
    range_iter,
    chunk,
    unique,
    shuffle,
    first,
    last,
    diff,
    has_intersects,
    toggle,
    zip_object,
    alphabetical,
)

from .string import (
    camel_case,
    snake_case,
    dash_case,
    pascal_case,
    capitalize,
    slugify,
    truncate,
    trim,
    generate_uuid,
    fuzzy_match,
    parse_template,
)

from .math import (
    random_int,
    clamp,
    lerp,
    normalize,
    is_even,
    is_odd,
    gcd,
    lcm,
    factorial,
    is_prime,
    fibonacci,
)

from .object import (
    pick,
    omit,
    merge,
    deep_copy,
    flatten_dict,
    get_nested_value,
    set_nested_value,
    safe_json_stringify,
)

from .function import (
    debounce,
    throttle,
    with_retry,
    memoize,
    once,
)

from .async_utils import (
    sleep_async,
    timeout,
    delay,
    race,
    retry_async,
    map_async,
    filter_async,
    run_in_thread,
)

from .bytes import (
    Bytes,
    bytes_util,
    humanize_bytes,
    parse_bytes,
)

# Define what gets exported when using "from pyutils import *"
__all__ = [
    # Modules
    'array',
    'string', 
    'math',
    'object',
    'function',
    'async_utils',
    'bytes_utils',
    
    # Array functions
    'range_list',
    'range_iter',
    'chunk',
    'unique',
    'shuffle',
    'first',
    'last',
    'diff',
    'has_intersects',
    'toggle',
    'zip_object',
    'alphabetical',
    
    # String functions
    'camel_case',
    'snake_case',
    'dash_case',
    'pascal_case',
    'capitalize',
    'slugify',
    'truncate',
    'trim',
    'generate_uuid',
    'fuzzy_match',
    'parse_template',
    
    # Math functions
    'random_int',
    'clamp',
    'lerp',
    'normalize',
    'is_even',
    'is_odd',
    'gcd',
    'lcm',
    'factorial',
    'is_prime',
    'fibonacci',
    
    # Object functions
    'pick',
    'omit',
    'merge',
    'deep_copy',
    'flatten_dict',
    'get_nested_value',
    'set_nested_value',
    'safe_json_stringify',
    
    # Function utilities
    'debounce',
    'throttle',
    'with_retry',
    'memoize',
    'once',
    
    # Async utilities
    'sleep_async',
    'timeout',
    'delay',
    'race',
    'retry_async',
    'map_async',
    'filter_async',
    'run_in_thread',
    
    # Bytes utilities
    'Bytes',
    'bytes_util',
    'humanize_bytes',
    'parse_bytes',
]
