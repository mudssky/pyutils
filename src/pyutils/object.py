"""Object utility functions.

This module provides utility functions for working with dictionaries and objects,
ported from the jsutils library.
"""

import json
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union

K = TypeVar('K')
V = TypeVar('V')
T = TypeVar('T')


def pick(obj: Dict[K, V], keys: List[K]) -> Dict[K, V]:
    """Create a new dictionary with only the specified keys.
    
    Args:
        obj: Source dictionary
        keys: List of keys to pick
        
    Returns:
        New dictionary with only the specified keys
        
    Examples:
        >>> pick({'a': 1, 'b': 2, 'c': 3}, ['a', 'c'])
        {'a': 1, 'c': 3}
        >>> pick({'name': 'Alice', 'age': 25, 'city': 'NYC'}, ['name', 'age'])
        {'name': 'Alice', 'age': 25}
    """
    return {key: obj[key] for key in keys if key in obj}


def pick_by(obj: Dict[K, V], predicate: Callable[[V, K], bool]) -> Dict[K, V]:
    """Create a new dictionary with key-value pairs that satisfy the predicate.
    
    Args:
        obj: Source dictionary
        predicate: Function that takes (value, key) and returns boolean
        
    Returns:
        New dictionary with filtered key-value pairs
        
    Examples:
        >>> pick_by({'a': 1, 'b': 2, 'c': 3}, lambda v, k: v > 1)
        {'b': 2, 'c': 3}
        >>> pick_by({'name': 'Alice', 'age': 25}, lambda v, k: isinstance(v, str))
        {'name': 'Alice'}
    """
    return {key: value for key, value in obj.items() if predicate(value, key)}


def omit(obj: Dict[K, V], keys: List[K]) -> Dict[K, V]:
    """Create a new dictionary without the specified keys.
    
    Args:
        obj: Source dictionary
        keys: List of keys to omit
        
    Returns:
        New dictionary without the specified keys
        
    Examples:
        >>> omit({'a': 1, 'b': 2, 'c': 3}, ['b'])
        {'a': 1, 'c': 3}
        >>> omit({'name': 'Alice', 'age': 25, 'city': 'NYC'}, ['age', 'city'])
        {'name': 'Alice'}
    """
    return {key: value for key, value in obj.items() if key not in keys}


def omit_by(obj: Dict[K, V], predicate: Callable[[V, K], bool]) -> Dict[K, V]:
    """Create a new dictionary without key-value pairs that satisfy the predicate.
    
    Args:
        obj: Source dictionary
        predicate: Function that takes (value, key) and returns boolean
        
    Returns:
        New dictionary with filtered key-value pairs
        
    Examples:
        >>> omit_by({'a': 1, 'b': 2, 'c': 3}, lambda v, k: v > 1)
        {'a': 1}
        >>> omit_by({'name': 'Alice', 'age': 25}, lambda v, k: isinstance(v, int))
        {'name': 'Alice'}
    """
    return {key: value for key, value in obj.items() if not predicate(value, key)}


def map_keys(obj: Dict[K, V], mapper: Callable[[K], T]) -> Dict[T, V]:
    """Create a new dictionary with transformed keys.
    
    Args:
        obj: Source dictionary
        mapper: Function to transform keys
        
    Returns:
        New dictionary with transformed keys
        
    Examples:
        >>> map_keys({'a': 1, 'b': 2}, str.upper)
        {'A': 1, 'B': 2}
        >>> map_keys({1: 'one', 2: 'two'}, lambda x: f'num_{x}')
        {'num_1': 'one', 'num_2': 'two'}
    """
    return {mapper(key): value for key, value in obj.items()}


def map_values(obj: Dict[K, V], mapper: Callable[[V], T]) -> Dict[K, T]:
    """Create a new dictionary with transformed values.
    
    Args:
        obj: Source dictionary
        mapper: Function to transform values
        
    Returns:
        New dictionary with transformed values
        
    Examples:
        >>> map_values({'a': 1, 'b': 2}, lambda x: x * 2)
        {'a': 2, 'b': 4}
        >>> map_values({'name': 'alice', 'city': 'nyc'}, str.upper)
        {'name': 'ALICE', 'city': 'NYC'}
    """
    return {key: mapper(value) for key, value in obj.items()}


def is_object(value: Any) -> bool:
    """Check if a value is a dictionary (object-like).
    
    Args:
        value: Value to check
        
    Returns:
        True if value is a dictionary, False otherwise
        
    Examples:
        >>> is_object({'a': 1})
        True
        >>> is_object([1, 2, 3])
        False
        >>> is_object('string')
        False
        >>> is_object(None)
        False
    """
    return isinstance(value, dict)


def merge(*dicts: Dict[Any, Any]) -> Dict[Any, Any]:
    """Recursively merge multiple dictionaries.
    
    Args:
        *dicts: Dictionaries to merge
        
    Returns:
        Merged dictionary
        
    Examples:
        >>> merge({'a': 1}, {'b': 2})
        {'a': 1, 'b': 2}
        >>> merge({'a': {'x': 1}}, {'a': {'y': 2}})
        {'a': {'x': 1, 'y': 2}}
        >>> merge({'a': 1}, {'a': 2})
        {'a': 2}
    """
    result: Dict[Any, Any] = {}
    
    for d in dicts:
        if not isinstance(d, dict):
            continue
            
        for key, value in d.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = merge(result[key], value)
            else:
                result[key] = value
    
    return result


def remove_non_serializable_props(obj: Any) -> Any:
    """Remove properties that cannot be JSON serialized.
    
    Args:
        obj: Object to clean
        
    Returns:
        Object with only JSON-serializable properties
        
    Examples:
        >>> import datetime
        >>> data = {'name': 'Alice', 'func': lambda x: x, 'date': 'today'}
        >>> cleaned = remove_non_serializable_props(data)
        >>> 'name' in cleaned
        True
        >>> 'func' in cleaned
        False
    """
    def is_serializable(value: Any) -> bool:
        try:
            json.dumps(value)
            return True
        except (TypeError, ValueError):
            return False
    
    if isinstance(obj, dict):
        return {
            key: remove_non_serializable_props(value)
            for key, value in obj.items()
            if is_serializable(value)
        }
    elif isinstance(obj, list):
        return [
            remove_non_serializable_props(item)
            for item in obj
            if is_serializable(item)
        ]
    else:
        return obj if is_serializable(obj) else None


def safe_json_stringify(obj: Any, indent: Optional[int] = None) -> str:
    """Safely convert object to JSON string, removing non-serializable properties.
    
    Args:
        obj: Object to stringify
        indent: JSON indentation, optional
        
    Returns:
        JSON string
        
    Examples:
        >>> safe_json_stringify({'name': 'Alice', 'age': 25})
        '{"name": "Alice", "age": 25}'
        >>> import datetime
        >>> data = {'name': 'Alice', 'func': lambda x: x}
        >>> result = safe_json_stringify(data)
        >>> 'name' in result
        True
        >>> 'func' in result
        False
    """
    cleaned_obj = remove_non_serializable_props(obj)
    return json.dumps(cleaned_obj, indent=indent)


def invert(obj: Dict[K, V]) -> Dict[V, K]:
    """Create a new dictionary with keys and values swapped.
    
    Args:
        obj: Source dictionary
        
    Returns:
        New dictionary with keys and values swapped
        
    Examples:
        >>> invert({'a': 1, 'b': 2})
        {1: 'a', 2: 'b'}
        >>> invert({'name': 'Alice', 'age': 25})
        {'Alice': 'name', 25: 'age'}
    """
    return {value: key for key, value in obj.items()}


def deep_copy(obj: Any) -> Any:
    """Create a deep copy of an object.
    
    Args:
        obj: Object to copy
        
    Returns:
        Deep copy of the object
        
    Examples:
        >>> original = {'a': {'b': 1}}
        >>> copied = deep_copy(original)
        >>> copied['a']['b'] = 2
        >>> original['a']['b']
        1
    """
    import copy
    return copy.deepcopy(obj)


def flatten_dict(obj: Dict[str, Any], separator: str = '.', prefix: str = '') -> Dict[str, Any]:
    """Flatten a nested dictionary.
    
    Args:
        obj: Dictionary to flatten
        separator: Separator for nested keys, defaults to '.'
        prefix: Prefix for keys, defaults to ''
        
    Returns:
        Flattened dictionary
        
    Examples:
        >>> flatten_dict({'a': {'b': {'c': 1}}})
        {'a.b.c': 1}
        >>> flatten_dict({'user': {'name': 'Alice', 'age': 25}})
        {'user.name': 'Alice', 'user.age': 25}
    """
    result = {}
    
    for key, value in obj.items():
        new_key = f"{prefix}{separator}{key}" if prefix else key
        
        if isinstance(value, dict):
            result.update(flatten_dict(value, separator, new_key))
        else:
            result[new_key] = value
    
    return result


def unflatten_dict(obj: Dict[str, Any], separator: str = '.') -> Dict[str, Any]:
    """Unflatten a flattened dictionary.
    
    Args:
        obj: Flattened dictionary
        separator: Separator used in keys, defaults to '.'
        
    Returns:
        Nested dictionary
        
    Examples:
        >>> unflatten_dict({'a.b.c': 1})
        {'a': {'b': {'c': 1}}}
        >>> unflatten_dict({'user.name': 'Alice', 'user.age': 25})
        {'user': {'name': 'Alice', 'age': 25}}
    """
    result: Dict[str, Any] = {}
    
    for key, value in obj.items():
        parts = key.split(separator)
        current = result
        
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        
        current[parts[-1]] = value
    
    return result


def get_nested_value(obj: Dict[str, Any], path: str, separator: str = '.', default: Any = None) -> Any:
    """Get a nested value from a dictionary using a path.
    
    Args:
        obj: Source dictionary
        path: Path to the value (e.g., 'user.profile.name')
        separator: Path separator, defaults to '.'
        default: Default value if path not found
        
    Returns:
        Value at the specified path or default
        
    Examples:
        >>> data = {'user': {'profile': {'name': 'Alice'}}}
        >>> get_nested_value(data, 'user.profile.name')
        'Alice'
        >>> get_nested_value(data, 'user.profile.age', default=0)
        0
    """
    parts = path.split(separator)
    current = obj
    
    try:
        for part in parts:
            current = current[part]
        return current
    except (KeyError, TypeError):
        return default


def set_nested_value(obj: Dict[str, Any], path: str, value: Any, separator: str = '.') -> Dict[str, Any]:
    """Set a nested value in a dictionary using a path.
    
    Args:
        obj: Target dictionary (will be modified)
        path: Path to set the value (e.g., 'user.profile.name')
        value: Value to set
        separator: Path separator, defaults to '.'
        
    Returns:
        The modified dictionary
        
    Examples:
        >>> data = {}
        >>> set_nested_value(data, 'user.profile.name', 'Alice')
        {'user': {'profile': {'name': 'Alice'}}}
        >>> data
        {'user': {'profile': {'name': 'Alice'}}}
    """
    parts = path.split(separator)
    current = obj
    
    for part in parts[:-1]:
        if part not in current:
            current[part] = {}
        current = current[part]
    
    current[parts[-1]] = value
    return obj