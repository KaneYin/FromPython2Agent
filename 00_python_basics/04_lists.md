Lists are used to store multiple items in a single variable.

Lists are one of 4 built-in data types in Python used to store collections of data, the other 3 are Tuple, Set and Dictionary, all with different qualities and usage.

Lists are created using square brackets:

```python
thislist = ["apple", "banana", "cherry"]
print(thislist)
```

# List

List items are ordered, changeable, and allow duplicate values.

List items are indexed, the first item has index 0, the second item has index 1, etc.

## Access List items
List items are indexed so we can access them by referring to the index number:
```python
thislist = ["apple", "banana", "cherry"]  
print(thislist[1])
```

Always remember: **Index positions start at 0, not 1**.

### Negative Indexing

Negative indexing means start form the end.
`-1` refers to the last item, `-2` refers to the second last item etc.

```python
thislist = ["apple", "banana", "cherry"]
print(thislist[-1])
```

This syntax is quite useful, because you will often want to access the last item in a list without knowling excatly how long the list is.
### Range of Indexes

We can specify a range of indexes by specifying where to start and where to end the range. **Including the start excluding the end.**

When specifying a range, the return value will be a new list with the specified items. 

```python
thisList = [1, 2, 3, 4, 5, 6, 7, 8]
print(thisList[2:5])
```

- [ ] TODO : 的使用


### Check if Item Exists

To determine if a specified item is present in a list use `in` keyword.

```python
thisList = [1, 2, 3, 4, 5, 6, 7, 8]
if 2 in thisList:
    print("Yes")
```

## Change List Items

To change the value of a specific item, refer to the index number:

```python
thisList = [1, 2, 3, 4, 5, 6, 7, 8]
thisList[0] = 111
print(thisList)
```

### Change a Range of Item Values

To change the value of items within a specific range, define a list with the new values, and refer to the range of index numbers where you want to insert the new values:

```python
thislist = ["apple", "banana", "cherry", "orange", "kiwi", "mango"]  
thislist[1:3] = ["blackcurrant", "watermelon"]  
print(thislist)
```

### Insert Items
To insert a new list item, without replacing any of the existing values, we can use the `insert()` method.

The `insert()` method inserts an item at the specified index.

```python
thislist = ["apple", "banana", "cherry"]
thislist.insert(2, "watermelon")
print(thislist)
```

We can also use `insert()` to insert items at the specified index:
```python
thislist = ["apple", "banana", "cherry"]  
thislist.insert(1, "orange")  
print(thislist)
```

## Add List items

To add an item to the end of the list, use the `append()` method:

```python
thislist = ["apple", "banana", "cherry"]
thislist.append("orange")
print(thislist)
```

The `append()` method makes it easy to build lists  dynamically. For example, you can start with an empty list  and then add items to the list using a series of `append()` calls.

Building lists this way is very common, because we often won't know the data your users want to store in a program until after the program is running.
### Extend List
To append elements from _another list_ to the current list, use the `extend()` method.

```python
thislist = ["apple", "banana", "cherry"]
thatlist = ["mango", "pineapple"]
thislist.extend(thatlist)
print(thislist)
```

### Add Any Iterable Objects
The `extend()` method does not have to append lists, we can add any literable object (tuples, sets dictionaries etc.).

```python
thislist = ["apple", "banana", "cherry"]
thatuple = ("kiwi", "orange")
thislist.extend(thatuple)
print(thislist)
```

## Remove List Items
The `remove()` method removes the specified item. **It is removing the element by value.**

```python
thislist = ["apple", "banana", "cherry"]
thislist.remove("apple")
print(thislist)
```

If there are more than one item with the specified value, **the `remove()` method removes the first occurrence:**

```python
thislist = ["apple", "banana", "apple", "cherry"]
thislist.remove("apple")
print(thislist)
```
### Remove specified Index

The `pop()` method removes the specified index and returns the value.

```python
thislist = ["apple", "banana", "apple", "cherry"]
thislist.pop(1)
print(thislist)
```

If we do not specify the index, the `pop()` method removes the last item. **The pop method allows us to access the element after we remove it. This is the main difference of `remove()` and `del()`.**
### `del` keyword
If we **do know the position** of the item that we want to remove from a list, we can use the `del` statement:
```python
motocycles = ["honda", "yamaha"]

del motocycles[0]
print(motocycles)
```


# Loop List

We can loop through the list items using a `for` loop:
```python
thislist = ["apple", "banana", "cherry"]
for x in thislist:
    print(x)
```

**Loop through the index numbers**, we can also loop through the list items by referring to their index number.
Use the `range()` and `len()` to create a suitable iterabe.

```python
thislist = ["apple", "banana", "cherry"]
for i in range(len(thislist)):
    print(thislist[i])
 ```

`range()` function also makes it easy to generate a series of numbers. For example, we can use the `range()` function to print a series of numbers like this:
```python
for value in range(1, 5):
	print(value)
```
The `range()` function  causes Python to start counting at the first value you give it,  and it stops when it reaches the second value you provide.  Because it stops at that second value, the output never  contains the end value, which would have been 5 in this  case.

You can also pass `range()` only one argument, and it will  start the sequence of numbers at 0. For example, `range(6)`  would return the numbers from 0 through 5.
## Using a while loop
We can loop through the list by using a `while` loop.
Use the `len()` function to determine the length of the list, then start at 0 and loop througth the list items referring to their indexes.
Remember to increase the index by 1 after each iteration.

```python
thislist = ["apple", "banana", "cherry"]
i = 0
while i < len(thislist):
    print(thislist[i])
    i = i + 1
```

## Loop use list comprehension

List comprehension offers shortest syntax for looping through lists:

```python
thislist = ["apple", "banana", "cherry"]
[print(x) for x in thislist]
```

We can also use the list comprehension like this:
```python
thislist = ["apple", "banana", "cherry"]
newlist = [x for x in thislist if "a" in x]
print(newlist)
```

### Syntax
`newlist = [expression for item in iterable if condition == True]`

### Condition
The condition is like a filter that only accepts the item that evaluate to True.

```python
newlist = [x for x in fruits if x != "apple"]
```
> Only accept items that are not "apple"

The condition is opeional and can be omitted:

```python
newlist = [x for x in fruits]
```

### Iterable
The iterable acn be any iterable object, list a list, tuple set etc.

We can use `range()` to create an iterable:
```python
newlist = [x for x in range(10)]
```

### Expression
The expression is the current item in the iteration, but it is also the outcome, which you can manipulate before it ends up like a list item in the new list:

# Sort Lists

List objects have a `sort()` method that will sort the list alphanumerically, ascending, by default:

```python
thislist = ["orange", "apple", "banana", "cherry"]
thislist.sort()
print(thislist)
```

Sort the list numerically:
```python
thislist = [100, 50, 65, 82, 23]
thislist.sort()
print(thislist)
```

To sort descending, use the keyword argument `reverse = True`.

```python
thislist = ["orange", "apple", "banana", "cherry"]
thislist.sort(reverse = True)
print(thislist)
```

To maintain the original order of a list but present it in a sorted order, we can use the `sorted()` function. The `sorted()` function les you display you list in a particular order, but doesn't affect the actual order of the list.
```python
thislist = ["orange", "apple", "banana", "cherry"]
print(sorted(thislist))
print(thislist)
```
The sorted() function  can also accept a `reverse=True` argument if you want to  display a list in reverse-alphabetical order.


## Customize Sort Function
We can also customize our own function by using the keyword argument `key=function`.

The function will return a number that will be used to sort the list.

```python
def f(n):
    return abs(n-50)

thislist = [100, 50, 65, 82, 23]
thislist.sort(key = f)
print(thislist)
```
> Sort according to how close the number is to 50.

## Case Insensitive sort

By default the `sort()` method is case sensitive, resulting in all capital letters being sorted before lower case letters:

```python
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort()
print(thislist)
```

We can use built-in functions as key functions when sorting a list.
```python
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.sort(key = str.lower)
print(thislist)
```

## Reverse Order
What if we want to reverse the order of a list, regradless of the alphabet?

The `reverse()` method reverses the current soring order fo the elements.

```python
thislist = ["banana", "Orange", "Kiwi", "cherry"]
thislist.reverse()
print(thislist)
```

**Notice that reverse() doesn't sort backward alphabetically; it simply reverses the order of the list.**

Although it changes the order of a list permanently, but you can revert to the origial order anytime by applying `reverse()` to the same list a second time.

# Copy List

We cannot copy a list simply by typing `list2 = list1`, because: `list2` will only be a reference to `list1`, and changes made in `list1` will autoatically also be made in `list2`.
## Use `copy()` or `list()`

```python
thislist = ["banana", "Orange", "Kiwi", "cherry"]
mylist = thislist.copy()
print(mylist)
```

Another way to make a copy is to use the built-in method `list()`.
```python
thislist = ["banana", "Orange", "Kiwi", "cherry"]
mylist = list(thislist)
print(mylist)
```

Hint: change the items in the origional list would not affect the new list.

# Join Lists

There are several ways to join, or concatenate, two or more lists lists in Python.

**Using the `+` operator:**

```python
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

list3 = list1 + list2
print(list3)
```

**Using `append()` method**:
Join two lists by appending all the items form list2 into list1, one by one.

```python
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

for x in list2:
    list1.append(x)

print(list1)
```

**Use the `extend()` method, where the purpose is to add elements from one list to another list:**

```python
list1 = ["a", "b", "c"]
list2 = [1, 2, 3]

list1.extend(list2)
print(list1)
```

# List Methods


| Method    | Description                                                 |
| --------- | ----------------------------------------------------------- |
| append()  | Adds an element at the end of the list                      |
| clear()   | Removes all the elements from the list                      |
| copy()    | Returns a copy of the list                                  |
| count()   | Returns the number of elements                              |
| extend()  | Add another iterable to the end of current one              |
| index()   | Returns the index of the first element with specified value |
| insert()  | adds an element at the specified position                   |
| pop()     | Removes the element with position                           |
| remove()  | Removes the element with value                              |
| reverse() | reverse the order of the list                               |
| sort()    | sort the list                                               |
