# Collection Module - JavaScript-Inspired Array Methods

## Overview

The `collection` module provides JavaScript-inspired array methods for Python, making it easier for developers familiar with JavaScript to work with Python lists. These methods offer familiar functionality while maintaining Python's conventions.

## New Functions Added

### Array Search and Testing

- **`includes(arr, search_element, from_index=0)`** - Check if array contains a value
- **`find_index(arr, predicate, from_index=0)`** - Find index of first element matching condition
- **`find_last_index(arr, predicate, from_index=None)`** - Find index of last element matching condition
- **`some(arr, predicate)`** - Test if at least one element passes the test
- **`every(arr, predicate)`** - Test if all elements pass the test

### Array Transformation

- **`flat_map(arr, mapper)`** - Map each element and flatten the result
- **`group_by(arr, key_func)`** - Group elements by a key function
- **`to_reversed(arr)`** - Return new reversed array (non-mutating)
- **`to_sorted(arr, key=None, reverse=False)`** - Return new sorted array (non-mutating)

### Array Manipulation

- **`fill(arr, value, start=0, end=None)`** - Fill array with a value (mutating)
- **`copy_within(arr, target, start, end=None)`** - Copy part of array to another location (mutating)
- **`splice(arr, start, delete_count=None, *items)`** - Change array by removing/adding elements (mutating)
- **`with_item(arr, index, item)`** - Return new array with item at index changed (non-mutating)

### Element Access

- **`at(arr, index)`** - Access element at index (supports negative indices, returns None for out-of-bounds)

### Object-like Methods

- **`entries(arr)`** - Get [index, value] pairs
- **`keys(arr)`** - Get array indices
- **`values(arr)`** - Get array values (creates a copy)

## Usage Examples

```python
from pyutils.collection import flat_map, includes, group_by, some, every, at

# flat_map - transform and flatten
result = flat_map([1, 2, 3], lambda x: [x, x * 2])
# Result: [1, 2, 2, 4, 3, 6]

# includes - check if value exists
has_banana = includes(['apple', 'banana', 'cherry'], 'banana')
# Result: True

# some/every - test conditions
has_even = some([1, 2, 3, 4], lambda x: x % 2 == 0)
all_positive = every([1, 2, 3, 4], lambda x: x > 0)
# Results: True, True

# group_by - organize data
grouped = group_by(['apple', 'banana', 'apricot'], lambda x: x[0])
# Result: {'a': ['apple', 'apricot'], 'b': ['banana']}

# at - safe element access
last_item = at([1, 2, 3, 4], -1)  # Result: 4
out_of_bounds = at([1, 2, 3], 10)  # Result: None
```

## Practical Use Cases

### 1. Data Processing
```python
# Extract all hobbies from user data
users = [
    {'name': 'Alice', 'hobbies': ['reading', 'swimming']},
    {'name': 'Bob', 'hobbies': ['gaming', 'cooking']}
]
all_hobbies = flat_map(users, lambda user: user['hobbies'])
```

### 2. Data Validation
```python
# Check if all scores are passing
scores = [85, 92, 78, 96, 88]
all_passing = every(scores, lambda score: score >= 70)
has_excellent = some(scores, lambda score: score >= 95)
```

### 3. Data Organization
```python
# Group products by category
products = [
    {'name': 'Laptop', 'category': 'electronics'},
    {'name': 'Book', 'category': 'education'},
    {'name': 'Phone', 'category': 'electronics'}
]
by_category = group_by(products, lambda p: p['category'])
```

## Key Benefits

1. **Familiar API** - JavaScript developers can use familiar method names
2. **Functional Programming** - Encourages immutable operations where appropriate
3. **Type Safety** - Proper handling of edge cases (empty arrays, out-of-bounds access)
4. **Performance** - Efficient implementations using Python's built-in functions
5. **Consistency** - Follows JavaScript behavior while respecting Python conventions

## Installation

These functions are available as part of the `pyutils` package:

```python
from pyutils import flat_map, includes, group_by  # Direct import
# or
from pyutils.collection import *  # Import all collection functions
```

## Comparison with JavaScript

| JavaScript | Python (pyutils.collection) | Notes |
|------------|------------------------------|-------|
| `arr.includes(x)` | `includes(arr, x)` | Same functionality |
| `arr.flatMap(fn)` | `flat_map(arr, fn)` | Same functionality |
| `arr.some(fn)` | `some(arr, fn)` | Same functionality |
| `arr.every(fn)` | `every(arr, fn)` | Same functionality |
| `arr.findIndex(fn)` | `find_index(arr, fn)` | Same functionality |
| `arr.at(i)` | `at(arr, i)` | Same functionality |
| `arr.splice(...)` | `splice(arr, ...)` | Mutates original array |
| `arr.with(i, x)` | `with_item(arr, i, x)` | Returns new array |

These additions make the `pyutils` library more comprehensive and provide JavaScript developers with familiar tools for array manipulation in Python.
