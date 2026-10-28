A dictionary in python is a collection of key-value pairs. Each key is connected to a value, and you can use a key to access the value associated with that key. A key's value can be a number, a string, a list, or even another dictionary.

In Python, a dictionary is wrapped in braces ({}) with a  series of key-value pairs inside the braces, as shown in the  earlier example:
```
alien_0 = {'color': 'green', 'points': 5}
```

A **key-value pair** is a set of values associated with each other. When you provide a key, Python returns the value associated with that key. **Every key is connected to its value by a colon**, and individual key-value pairs are separated by commas. You can store as may key-value pairs as you want in a dictionary.

The simplest dictionary has exactly one key-value pair.

# Accessing values in a dictionary
To get the value associated with a key, give the name of the dictionary and then **place the key inside a set of square brackets**, as shown here:
```
alien_0 = {'color': 'green'}
print(alien_0['color'])
```

We can hvae an **unlimited number of key-value pairs** in a dictionary. For example, here is the original dictionary with two key-value pairs:
```
alien_0 = {'color': 'green', 'points': 5}
```

## Using `get()` to access values
Using keys in square brackets to access the value we are looking for might cause one potential proble: if the key we need doesn't exist, we will get an error.

For dictionaries specifically, you can  use the `get()` method to set a default value that will be  returned if the requested key doesn’t exist.
**The get() method requires a key as a first argument. As a  second optional argument, you can pass the value to be  returned if the key doesn’t exist:**
```python
alien_0 = {'color': 'green', 'points': 5}
point_value = alien_0.get('points', 'No point value assigned.')
print(point_value)
```

If there is a chance the key you are looking for might not exist, consider using the `get()` method instead f the square bracknet notation.

# Adding new key-value pairs
Dictionaries are dynamic structures, and you can add new  key-value pairs to a dictionary at any time. To add a new  key-value pair, you would give the name of the dictionary  followed by the new key in square brackets, along with the  new value.

```python
alien_0 = {'color': 'green', 'points': 5}
print(alien_0)

alien_0['x_position'] = 0
alien_0['y_position'] = 25
print(alien_0)
```
The final version of the dictionary contains four key-value  pairs.

**Dictionaries retain the order in which they were defined.**  When we print a dictionary or loop through its elements,  we will see the elements in the same order they were  added to the dictionary.

- [ ] TODO: starting with an empty dictionary



# Looping through a dictionary
Dictionaries can be used to store information in a  variety of ways; therefore, several different ways exist to  loop through them. You can loop through all of a dictionary’s  key-value pairs, through its keys, or through its values.

## Looping through all key-value pairs
Consider a new dictionary designed to store infromation about a user on a website. The following dictionary would store one person's username, first name, and last name:

```python
user = {
    'username': 'afns',
    'first': 'fasd',
    'last': 'fermi',
}
```

To loop through the dictionary using a `for` loop:
```python
user = {
    'username': 'afns',
    'first': 'fasd',
    'last': 'fermi',
}

for key, value in user.items():
    print(f"Key:{key}")
    print(f"Value:{value}")
```

To write a `for` loop for a dictionary, we create names for the two variables that will hode the key and value in each key-value pair. You can choose any names you want for these two variables. This code would ork just as well if you had used abbreviations for the variable names, like this: `for k, v in user.items()`

The second half of the for statement includes the name of  the dictionary followed by the method `items()`, which returns  a sequence of key-value pairs.
## Looping through all the keys in a dictionary

The `keys()` method is useful when you don’t need to work  with all of the values in a dictionary.

```python
user = {
    'username': 'afns',
    'first': 'fasd',
    'last': 'fermi',
}

for key in user.keys():
    print(f"key: {key}")
```

**Looping through the keys is actually the default behavior**  when looping through a dictionary, so this code would have  exactly the same output if we wrote:

```python
user = {
    'username': 'afns',
    'first': 'fasd',
    'last': 'fermi',
}

for key in user:
    print(f"key: {key}")
```

The `keys()` method is not just for looping, it actually returns a sequence of all the keys, and the `if` statement simple checks if a specific element is in this sequence.

## Looping through a dict's keys in a particular order

When we loop through a dictionary, it returns the items in the same order they were inserted. Sometimes, though, you will want to loop through a dict in a different order.

**One way to do this is to sort the keys as they’re returned  in the for loop.** You can use the sorted() function to get a  copy of the keys in order:
```python
user = {
    'username': 'afns',
    'first': 'fasd',
    'last': 'fermi',
}

for key in sorted(user.keys()):
    print(f"key: {key}")
```

This tells Python to get all the  keys in the dictionary and sort them before starting the  loop.
## Looping through all values in a dict

**We can use `values()` method to return a sequence of values without any keys.**

This approach pulls all the values from the dictionary  **without checking for repeats**. This might work fine with a  small number of values, but in a poll with a large number of  respondents, it would result in a very repetitive list. **To see  each language chosen without repetition, we can use a set.**  A set is a collection in which each item must be unique.
```python
favorite_languages = {  
    'jen': 'python',
    'sarah': 'c',
    'edward': 'rust',
    'phil': 'python',
}

for language in set(favorite_languages.values()):
    print(language.title())
```

When we wrap `set()` around a collection of values that  contains duplicate items, Python identifies the unique items  in the collection and builds a set from those items. Here we  use `set()` to pull out the unique languages in  `favorite_languages.values()`.

# Nesting
Sometimes we’ll want to store multiple dictionaries in a list,  or a list of items as a value in a dictionary. This is called  nesting. We can nest dictionaries inside a list, a list of items  inside a dictionary, or even a dictionary inside another  dictionary. Nesting is a powerful feature, as the following  examples will demonstrate.

## A list of dict
One way is to make a list of aliens in which each alien is a dictionary of information  about that alien.

```python
alien_0 = {'color': 'green', 'point': 5}
alien_1 = {'color': 'yellow', 'point': 5}
alien_2 = {'color': 'red', 'point': 5}

aliens = [alien_0, alien_1, alien_2]

for alien in aliens:
    print(alien)
```

**It is common to store a number of dictionaries in a list when each dictionary contains many kinds of information about one obect.**

## A list in a dict
Rather than putting a dictionary inside a list, it’s sometimes  useful to put a list inside a dictionary.



**We can nest a list inside a dictionary anytime we want  more than one value to be associated with a single key in a  dictionary.**

