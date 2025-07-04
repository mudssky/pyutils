"""Array utility functions.

This module provides utility functions for working with arrays/lists,
ported from the jsutils library.
"""

import random
from typing import (
    Any,
    Callable,
    Dict,
    Generator,
    Iterable,
    List,
    Optional,
    Tuple,
    TypeVar,
    Union,
)

T = TypeVar('T')
K = TypeVar('K')
V = TypeVar('V')


def range_list(start: int, end: Optional[int] = None, step: int = 1) -> List[int]:
    """Generate a list of integers from start to end (exclusive).
    
    Args:
        start: Starting value (or end if end is None)
        end: Ending value (exclusive), optional
        step: Step size, defaults to 1
        
    Returns:
        List of integers
        
    Examples:
        >>> range_list(5)
        [0, 1, 2, 3, 4]
        >>> range_list(2, 5)
        [2, 3, 4]
        >>> range_list(0, 10, 2)
        [0, 2, 4, 6, 8]
    """
    if end is None:
        end = start
        start = 0
    return list(range(start, end, step))


def range_iter(start: int, end: Optional[int] = None, step: int = 1) -> Generator[int, None, None]:
    """Generate integers from start to end (exclusive).
    
    Args:
        start: Starting value (or end if end is None)
        end: Ending value (exclusive), optional
        step: Step size, defaults to 1
        
    Yields:
        Integer values
        
    Examples:
        >>> list(range_iter(3))
        [0, 1, 2]
        >>> list(range_iter(1, 4))
        [1, 2, 3]
    """
    if end is None:
        end = start
        start = 0
    yield from range(start, end, step)


def boil(items: List[T], compare_fn: Callable[[T, T], T]) -> Optional[T]:
    """Reduce a list to a single value using a comparison function.
    
    Args:
        items: List of items to reduce
        compare_fn: Function that takes two items and returns the preferred one
        
    Returns:
        The final reduced value, or None if list is empty
        
    Examples:
        >>> boil([1, 2, 3, 4], max)
        4
        >>> boil(['a', 'bb', 'ccc'], lambda a, b: a if len(a) > len(b) else b)
        'ccc'
    """
    if not items:
        return None
    
    result = items[0]
    for item in items[1:]:
        result = compare_fn(result, item)
    return result


def chunk(items: List[T], size: int) -> List[List[T]]:
    """Split a list into chunks of specified size.
    
    Args:
        items: List to split
        size: Size of each chunk
        
    Returns:
        List of chunks
        
    Examples:
        >>> chunk([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
        >>> chunk(['a', 'b', 'c', 'd'], 3)
        [['a', 'b', 'c'], ['d']]
    """
    if size <= 0:
        return []
    return [items[i:i + size] for i in range(0, len(items), size)]


def count_by(items: List[T], key_fn: Callable[[T], K]) -> Dict[K, int]:
    """Count items by a key function.
    
    Args:
        items: List of items to count
        key_fn: Function to extract key from each item
        
    Returns:
        Dictionary mapping keys to counts
        
    Examples:
        >>> count_by(['apple', 'banana', 'apricot'], lambda x: x[0])
        {'a': 2, 'b': 1}
        >>> count_by([1, 2, 3, 4, 5], lambda x: x % 2)
        {1: 3, 0: 2}
    """
    result: Dict[K, int] = {}
    for item in items:
        key = key_fn(item)
        result[key] = result.get(key, 0) + 1
    return result


def diff(old_list: List[T], new_list: List[T]) -> Tuple[List[T], List[T]]:
    """Find items added and removed between two lists.
    
    Args:
        old_list: Original list
        new_list: New list
        
    Returns:
        Tuple of (added_items, removed_items)
        
    Examples:
        >>> diff([1, 2, 3], [2, 3, 4])
        ([4], [1])
        >>> diff(['a', 'b'], ['b', 'c', 'd'])
        (['c', 'd'], ['a'])
    """
    old_set = set(old_list)
    new_set = set(new_list)
    
    added = [item for item in new_list if item not in old_set]
    removed = [item for item in old_list if item not in new_set]
    
    return added, removed


def first(items: List[T], default: Optional[T] = None) -> Optional[T]:
    """Get the first item from a list.
    
    Args:
        items: List to get first item from
        default: Default value if list is empty
        
    Returns:
        First item or default value
        
    Examples:
        >>> first([1, 2, 3])
        1
        >>> first([], 'default')
        'default'
    """
    return items[0] if items else default


def last(items: List[T], default: Optional[T] = None) -> Optional[T]:
    """Get the last item from a list.
    
    Args:
        items: List to get last item from
        default: Default value if list is empty
        
    Returns:
        Last item or default value
        
    Examples:
        >>> last([1, 2, 3])
        3
        >>> last([], 'default')
        'default'
    """
    return items[-1] if items else default


def fork(items: List[T], condition: Callable[[T], bool]) -> Tuple[List[T], List[T]]:
    """Split a list into two based on a condition.
    
    Args:
        items: List to split
        condition: Function to test each item
        
    Returns:
        Tuple of (items_matching_condition, items_not_matching_condition)
        
    Examples:
        >>> fork([1, 2, 3, 4, 5], lambda x: x % 2 == 0)
        ([2, 4], [1, 3, 5])
        >>> fork(['apple', 'banana', 'cherry'], lambda x: len(x) > 5)
        (['banana', 'cherry'], ['apple'])
    """
    true_items = []
    false_items = []
    
    for item in items:
        if condition(item):
            true_items.append(item)
        else:
            false_items.append(item)
    
    return true_items, false_items


def has_intersects(list1: List[T], list2: List[T]) -> bool:
    """Check if two lists have any common elements.
    
    Args:
        list1: First list
        list2: Second list
        
    Returns:
        True if lists have common elements, False otherwise
        
    Examples:
        >>> has_intersects([1, 2, 3], [3, 4, 5])
        True
        >>> has_intersects([1, 2], [3, 4])
        False
    """
    set1 = set(list1)
    return any(item in set1 for item in list2)


def max_by(items: List[T], key_fn: Callable[[T], Any]) -> Optional[T]:
    """Find the item with the maximum value according to a key function.
    
    Args:
        items: List of items
        key_fn: Function to extract comparison value
        
    Returns:
        Item with maximum value, or None if list is empty
        
    Examples:
        >>> max_by(['apple', 'banana', 'cherry'], len)
        'banana'
        >>> max_by([{'age': 20}, {'age': 30}, {'age': 25}], lambda x: x['age'])
        {'age': 30}
    """
    if not items:
        return None
    return max(items, key=key_fn)


def min_by(items: List[T], key_fn: Callable[[T], Any]) -> Optional[T]:
    """Find the item with the minimum value according to a key function.
    
    Args:
        items: List of items
        key_fn: Function to extract comparison value
        
    Returns:
        Item with minimum value, or None if list is empty
        
    Examples:
        >>> min_by(['apple', 'banana', 'cherry'], len)
        'apple'
        >>> min_by([{'age': 20}, {'age': 30}, {'age': 25}], lambda x: x['age'])
        {'age': 20}
    """
    if not items:
        return None
    return min(items, key=key_fn)


def toggle(items: List[T], item: T) -> List[T]:
    """Add item to list if not present, remove if present.
    
    Args:
        items: List to toggle item in
        item: Item to toggle
        
    Returns:
        New list with item toggled
        
    Examples:
        >>> toggle([1, 2, 3], 4)
        [1, 2, 3, 4]
        >>> toggle([1, 2, 3], 2)
        [1, 3]
    """
    result = items.copy()
    if item in result:
        result.remove(item)
    else:
        result.append(item)
    return result


def sum_by(items: List[T], key_fn: Callable[[T], Union[int, float]]) -> Union[int, float]:
    """Sum values extracted from items using a key function.
    
    Args:
        items: List of items
        key_fn: Function to extract numeric value from each item
        
    Returns:
        Sum of extracted values
        
    Examples:
        >>> sum_by([{'value': 10}, {'value': 20}, {'value': 30}], lambda x: x['value'])
        60
        >>> sum_by(['hello', 'world', 'python'], len)
        16
    """
    return sum(key_fn(item) for item in items)


def zip_object(keys: List[K], values: List[V]) -> Dict[K, V]:
    """Create a dictionary from lists of keys and values.
    
    Args:
        keys: List of keys
        values: List of values
        
    Returns:
        Dictionary mapping keys to values
        
    Examples:
        >>> zip_object(['a', 'b', 'c'], [1, 2, 3])
        {'a': 1, 'b': 2, 'c': 3}
        >>> zip_object(['name', 'age'], ['Alice', 25])
        {'name': 'Alice', 'age': 25}
    """
    return dict(zip(keys, values))


def zip_lists(*lists: List[T]) -> List[Tuple[T, ...]]:
    """Zip multiple lists together.
    
    Args:
        *lists: Variable number of lists to zip
        
    Returns:
        List of tuples containing corresponding elements
        
    Examples:
        >>> zip_lists([1, 2, 3], ['a', 'b', 'c'])
        [(1, 'a'), (2, 'b'), (3, 'c')]
        >>> zip_lists([1, 2], [3, 4], [5, 6])
        [(1, 3, 5), (2, 4, 6)]
    """
    return list(zip(*lists))


def unique(items: List[T]) -> List[T]:
    """Remove duplicate items from a list while preserving order.
    
    Args:
        items: List with potential duplicates
        
    Returns:
        List with duplicates removed
        
    Examples:
        >>> unique([1, 2, 2, 3, 1, 4])
        [1, 2, 3, 4]
        >>> unique(['a', 'b', 'a', 'c', 'b'])
        ['a', 'b', 'c']
    """
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def shuffle(items: List[T]) -> List[T]:
    """Return a new list with items in random order.
    
    Args:
        items: List to shuffle
        
    Returns:
        New shuffled list
        
    Examples:
        >>> original = [1, 2, 3, 4, 5]
        >>> shuffled = shuffle(original)
        >>> len(shuffled) == len(original)
        True
        >>> set(shuffled) == set(original)
        True
    """
    result = items.copy()
    random.shuffle(result)
    return result


def alphabetical(items: List[str], key_fn: Optional[Callable[[str], str]] = None) -> List[str]:
    """Sort strings alphabetically.
    
    Args:
        items: List of strings to sort
        key_fn: Optional function to extract sort key from each string
        
    Returns:
        New sorted list
        
    Examples:
        >>> alphabetical(['banana', 'apple', 'cherry'])
        ['apple', 'banana', 'cherry']
        >>> alphabetical(['Apple', 'banana', 'Cherry'], key_fn=str.lower)
        ['Apple', 'banana', 'Cherry']
    """
    if key_fn is None:
        return sorted(items)
    return sorted(items, key=key_fn)