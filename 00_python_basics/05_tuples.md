Lists work well for storing collections of items that can  change throughout the life of a program.

However, sometimes you’ll want to create a list of  items that cannot change. Tuples allow you to do just that.  **Python refers to values that cannot change as immutable,  and an immutable list is called a tuple.**

# Defining a Tuple
A tuple looks just like a list, except we use parentheses instead of square brackets. Once we define a tuple, we can access individual elements by using each item's index, just as we would for a list.

For example, if we have a rectangle that should always be a certain size, we can unsure that its size doesn't change by putting the dimensions into a tuple:
```python
dimensions = (200, 50)
print(dimensions[0])
print(dimensions[1])
```

This code tries to change the value of the first dimension, but python returns a type error. Because we’re trying to  alter a tuple, which can’t be done to that type of object,  Python tells us we can’t assign a new value to an item in a  tuple:
```python
dimensions = (200, 50)
print(dimensions[0])
dimensions[1] = 100
print(dimensions[1])

// TypeError: 'tuple' object does not support item assignment
```

## Writing over a tuple
Although you can’t modify a tuple, you can assign a new  value to a variable that represents a tuple. For example, if  we wanted to change the dimensions of this rectangle, we  could redefine the entire tuple:
```python
dimensions = (200, 50)
print(dimensions)

dimensions = (1, 2, 3)
print(dimensions)
```

# Looping through all values in a tuple
We can loop over all the values in a tuple using a `for` loop, just as we did with a list:
```python
dimensions = (200, 50)
for dimension in dimensions:
    print(dimension)
```
