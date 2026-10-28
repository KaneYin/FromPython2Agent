- Part of python standard libraries
- Usefull in algorithms, data structures

# deque
- stands for double ended queue
- allows to add and remove elements from both ends efficiently
- works as both a queue and a stack

## operations

- `append()`: adds an element to the right end of the deque
- `appendleft()`: adds an element to the left end of the deque
extend
- `extend()`: adds multiple elements to the right end of the deque
- `extendleft()`: adds multiple elements to the left end of the deque
- `remove()`: removes the first occurrence of a specified value
- `pop()`: removes and returns the element from the right end
- `popleft():` removes and returns the element from the left end
- `clear()`: removes all elements from the deque
- `len()`: returns the total number of elements in the deque. Usage, `len(deque)`
- `count():` returns how many times a specific element appears in the deque
- `rotate()`: rotates the elements of the deque
- `reverse()`: reverses the order of elements in the deque.

# Counter

## Operations
- `update()`: adds counts from another iterable or mapping. Existing counts increase and new elements are added
- `elements()`: Returns an iterator over elements repeating each as many times as its count. Elements are returned in arbitrary order
- `most_common()`: Returns a list of the n most common elements and their counts from the most common to the least. If n is not specified, it returns all elements in the Counter
-  increasing count manually: Increases the count of a single element by 1.
```python
ctr = Counter([1, 1, 2, 3])

ctr[2] += 2
ctr[4] += 1
print(ctr)
# Counter({2: 3, 1: 2, 3: 1, 4: 1})
```
- `subtract()`: subtracts element counts from another iterable or mapping. Counts can go negative.

# `defaultdict`
- subclass of the built-in dict class from the collections
- automatically assigns a default value to keys that do not exist

**Syntax:**
```python
defaultdict(default_factory)
```

Parameters:
- default_factory: A callable (like int, list, set, str or a custom function) that provides the default value for missing keys.
- If this argument is None, accessing a missing key raises a KeyError.
## Operations


# References
1. [Deque in Python](https://www.geeksforgeeks.org/python/deque-in-python/)
2. 