
Variables are containers for storing data values.

# Creating Values
## Basic

Python has no command for declaring a variable.

> Python 没有声明变量的语句。


A variable is created the moment you first assign a value to it.

Example:
```python
x = 5  
y = "John"  
print(x)  
print(y)
```

Variables do not need to be declared with any particular _type_, and can even change type after they have been set.

```python
x = 4       # x is of type int  
x = "Sally" # x is now of type str  
print(x)
```
## Casting

If you want to specify the data type of a variable, this can be done with casting.

```python
x = str(3)    # x will be '3'  
y = int(3)    # y will be 3  
z = float(3)  # z will be 3.0
```

## Get the type of variable
You can get the data type of a variable with the `type()` function
```python
x = 5  
y = "John"  
print(type(x))  
print(type(y))
```

## String variables

String variables can be declared either by using single or double quotes:
```python
x = "John"  
# is the same as  
x = 'John'
```
# Values names
A variable can have a short name (like x and y) or a more descriptive name (age, carname, total_volume).

Rules for Python variables:

- A variable name must start with a letter or the underscore character
- A variable name cannot start with a number
- A variable name can only contain alpha-numeric characters and underscores (A-z, 0-9, and _ )
- Variable names are case-sensitive (age, Age and AGE are three different variables)
- A variable name can not be any of the Python Keywords

Examples of Python variable names:
```python
myvar = "John"  
my_var = "John"  
_my_var = "John"  
myVar = "John"  
MYVAR = "John"  
myvar2 = "John"
```
# Assign Multi values

## Multi values to Multi variables
Python allows you to assign values to multiple variables in one line:

```python
x, y, z = "Orange", "Banana", "Cherry"  
print(x)  
print(y)  
print(z)
```

> **Note:** Make sure the number of variables matches the number of values, or else you will get an error.

## One value to Multi variables

And you can assign the _same_ value to multiple variables in one line:

```python
x = y = z = "Orange"  
print(x)  
print(y)  
print(z)
```

## Unpack a Collection

If you have a collection of values in a list, tuple etc. Python allows you to extract the values into variables. This is called _unpacking_.

```python
fruits = ["apple", "banana", "cherry"]  
x, y, z = fruits  
print(x)  
print(y)  
print(z)
```

# Output Variable
The Python `print()` function is often used to output variables.

```python
x = "Python is awesome"  
print(x)
```

In `print()` function, you can output multiple variables, separated by a comma:
```python
x = "Python"  
y = "is"  
z = "awesome"  
print(x, y, z)
```