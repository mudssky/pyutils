"""Examples demonstrating the new collection utility functions.

These functions are inspired by JavaScript array methods and provide
familiar functionality for Python developers coming from JavaScript.
"""

from pyutils.collection import (
    at,
    copy_within,
    entries,
    every,
    fill,
    find_index,
    find_last_index,
    flat_map,
    group_by,
    includes,
    keys,
    some,
    splice,
    to_reversed,
    to_sorted,
    values,
    with_item,
)


def demonstrate_array_methods():
    """Demonstrate JavaScript-like array methods."""
    print("=== JavaScript-like Array Methods ===")
    
    # flat_map - maps and flattens in one step
    numbers = [1, 2, 3]
    result = flat_map(numbers, lambda x: [x, x * 2])
    print(f"flat_map([1, 2, 3], x => [x, x*2]): {result}")
    
    # includes - check if array contains a value
    fruits = ['apple', 'banana', 'cherry']
    print(f"includes(['apple', 'banana', 'cherry'], 'banana'): {includes(fruits, 'banana')}")
    print(f"includes(['apple', 'banana', 'cherry'], 'grape'): {includes(fruits, 'grape')}")
    
    # find_index - find index of first element matching condition
    numbers = [1, 2, 3, 4, 5]
    index = find_index(numbers, lambda x: x > 3)
    print(f"find_index([1, 2, 3, 4, 5], x => x > 3): {index}")
    
    # find_last_index - find index of last element matching condition
    numbers = [1, 2, 3, 2, 4]
    last_index = find_last_index(numbers, lambda x: x == 2)
    print(f"find_last_index([1, 2, 3, 2, 4], x => x == 2): {last_index}")
    
    # some - test if at least one element passes the test
    numbers = [1, 2, 3, 4]
    has_even = some(numbers, lambda x: x % 2 == 0)
    print(f"some([1, 2, 3, 4], x => x % 2 == 0): {has_even}")
    
    # every - test if all elements pass the test
    even_numbers = [2, 4, 6, 8]
    all_even = every(even_numbers, lambda x: x % 2 == 0)
    print(f"every([2, 4, 6, 8], x => x % 2 == 0): {all_even}")
    
    # at - access element at index (supports negative indices)
    letters = ['a', 'b', 'c', 'd']
    print(f"at(['a', 'b', 'c', 'd'], -1): {at(letters, -1)}")
    print(f"at(['a', 'b', 'c', 'd'], 1): {at(letters, 1)}")
    
    print()


def demonstrate_array_manipulation():
    """Demonstrate array manipulation methods."""
    print("=== Array Manipulation Methods ===")
    
    # fill - fill array with a value
    arr = [1, 2, 3, 4, 5]
    filled = fill(arr.copy(), 0, 1, 4)
    print(f"fill([1, 2, 3, 4, 5], 0, 1, 4): {filled}")
    
    # copy_within - copy part of array to another location
    arr = [1, 2, 3, 4, 5]
    copied = copy_within(arr.copy(), 0, 3)
    print(f"copy_within([1, 2, 3, 4, 5], 0, 3): {copied}")
    
    # splice - change array by removing/adding elements
    arr = [1, 2, 3, 4, 5]
    removed = splice(arr, 2, 1, 'a', 'b')
    print(f"splice([1, 2, 3, 4, 5], 2, 1, 'a', 'b'): arr={arr}, removed={removed}")
    
    # with_item - return new array with item at index changed
    original = [1, 2, 3, 4]
    modified = with_item(original, 1, 'two')
    print(f"with_item([1, 2, 3, 4], 1, 'two'): {modified} (original: {original})")
    
    # to_reversed - return new reversed array (non-mutating)
    original = [1, 2, 3, 4]
    reversed_arr = to_reversed(original)
    print(f"to_reversed([1, 2, 3, 4]): {reversed_arr} (original: {original})")
    
    # to_sorted - return new sorted array (non-mutating)
    original = [3, 1, 4, 1, 5]
    sorted_arr = to_sorted(original)
    print(f"to_sorted([3, 1, 4, 1, 5]): {sorted_arr} (original: {original})")
    
    print()


def demonstrate_object_like_methods():
    """Demonstrate object-like methods for arrays."""
    print("=== Object-like Methods ===")
    
    # entries - get [index, value] pairs
    fruits = ['apple', 'banana', 'cherry']
    entry_pairs = entries(fruits)
    print(f"entries(['apple', 'banana', 'cherry']): {entry_pairs}")
    
    # keys - get array indices
    array_keys = keys(fruits)
    print(f"keys(['apple', 'banana', 'cherry']): {array_keys}")
    
    # values - get array values (creates a copy)
    array_values = values(fruits)
    print(f"values(['apple', 'banana', 'cherry']): {array_values}")
    
    print()


def demonstrate_grouping():
    """Demonstrate grouping functionality."""
    print("=== Grouping Methods ===")
    
    # group_by - group elements by a key function
    words = ['apple', 'banana', 'apricot', 'blueberry', 'cherry']
    grouped = group_by(words, lambda word: word[0])
    print(f"group_by(['apple', 'banana', 'apricot', 'blueberry', 'cherry'], first_letter):")
    for letter, group in grouped.items():
        print(f"  {letter}: {group}")
    
    # Group numbers by even/odd
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    even_odd = group_by(numbers, lambda x: 'even' if x % 2 == 0 else 'odd')
    print(f"\ngroup_by([1..10], even_or_odd):")
    for parity, group in even_odd.items():
        print(f"  {parity}: {group}")
    
    print()


def demonstrate_practical_examples():
    """Demonstrate practical use cases."""
    print("=== Practical Examples ===")
    
    # Example 1: Processing nested data
    users = [
        {'name': 'Alice', 'hobbies': ['reading', 'swimming']},
        {'name': 'Bob', 'hobbies': ['gaming', 'cooking']},
        {'name': 'Charlie', 'hobbies': ['reading', 'hiking']}
    ]
    
    all_hobbies = flat_map(users, lambda user: user['hobbies'])
    print(f"All hobbies from users: {all_hobbies}")
    
    # Example 2: Data validation
    scores = [85, 92, 78, 96, 88]
    all_passing = every(scores, lambda score: score >= 70)
    has_excellent = some(scores, lambda score: score >= 95)
    print(f"All students passing (>=70): {all_passing}")
    print(f"Any excellent scores (>=95): {has_excellent}")
    
    # Example 3: Finding specific data
    products = [
        {'name': 'Laptop', 'price': 999, 'category': 'electronics'},
        {'name': 'Book', 'price': 15, 'category': 'education'},
        {'name': 'Phone', 'price': 699, 'category': 'electronics'},
        {'name': 'Desk', 'price': 299, 'category': 'furniture'}
    ]
    
    expensive_index = find_index(products, lambda p: p['price'] > 500)
    if expensive_index != -1:
        print(f"First expensive product: {products[expensive_index]['name']}")
    
    # Example 4: Grouping and analysis
    by_category = group_by(products, lambda p: p['category'])
    print(f"\nProducts by category:")
    for category, items in by_category.items():
        avg_price = sum(item['price'] for item in items) / len(items)
        print(f"  {category}: {len(items)} items, avg price: ${avg_price:.2f}")
    
    print()


if __name__ == '__main__':
    demonstrate_array_methods()
    demonstrate_array_manipulation()
    demonstrate_object_like_methods()
    demonstrate_grouping()
    demonstrate_practical_examples()
    
    print("=== Summary ===")
    print("These JavaScript-inspired methods provide familiar functionality for:")
    print("• Array searching and filtering (includes, find_index, some, every)")
    print("• Array transformation (flat_map, group_by, to_sorted, to_reversed)")
    print("• Array manipulation (splice, fill, copy_within, with_item)")
    print("• Object-like operations (entries, keys, values)")
    print("• Safe element access (at with negative indices)")