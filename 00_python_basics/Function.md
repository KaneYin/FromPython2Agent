# How to define a function

In python, a function is defined using the `def` keyword, followed by a function name and parentheses.

Syntax:
```python
def func_name(parameter):
	do_something
	return return_val
```

Example:
```python
def greet():  
  print("Hello from a function")
```

## Parameter and Arguments
**Arguments are specified after the function name, inside the parentheses.** You can add as many arguments as you want, just separate them with a comma.

The terms _parameter_ and _argument_ can be used for the same thing: information that are passed into a function.

> **From a function's perspective:
> 
> A parameter is the variable listed inside the parentheses in the function definition.
> 
> An argument** is the actual value that is sent to the function when it is called.

### Default parameter values
We can assign default values to parameters, If the function is called without an argument, it uses the default value:
```python
def my_function(name = "friend"):  
  print("Hello", name)  
  
my_function("Emil")  
my_function("Tobias")  
my_function()  
my_function("Linus")
```

> **When we use default values, any parameter with a default value needs to be listed after all the parameters that don't have default values.** 
### Keyword Arguments

You can send arguments with the `key=value` syntax. We directly associate the name and the value within the argument, so when we pass the argument to the funciton, there is no confusion. **Keyword arguments free us form havign to worry about correctly ordering our arguments in the function call, and they clarify the role of each value in the function call.**
```python
def my_function(animal, name):  
  print("I have a", animal)  
  print("My", animal + "'s name is", name)  
  
my_function(animal = "dog", name = "Buddy")
```

This way, with keyword arguments, **the order of the arguments does not matter.**

> When we use keyword arguments, be sure to use the **exact names of the parameters in the function's definition**.


### Positional Arguments

**When you call a function with arguments without using keywords, they are called positional arguments.** This is based on the order of the arguments provided.
Positional arguments must be in the correct order:

```python
def my_function(animal, name):  
  print("I have a", animal)  
  print("My", animal + "'s name is", name)  
  
my_function("dog", "Buddy")
```
#### Order matters
We may get unexpected results if we mix up the order of  the arguments in a function call when using positional  arguments:
```python
def my_function(animal, name):  
  print("I have a", animal)  
  print("My", animal + "'s name is", name)  
  
my_function("Buddy", "dog")
```
### Mixing Positional and Keyword Arguments
You can mix positional and keyword arguments in a function call.

However, positional arguments must come before keyword arguments:

```python
def my_function(animal, name, age):  
  print("I have a", age, "year old", animal, "named", name)  
  
my_function("dog", name = "Buddy", age = 5)
```

### Passing different data types
You can send any data type as an argument to a function (string, number, list, dictionary, etc).
The data type will be preserved inside the function:
```python
def my_function(fruits):
	for fruit in fruits:
		print(friut)
		

my_fruits = ["apple", "banana", "cherry"]  
my_function(my_fruits)
```

### Positional only arguments
You can specify that a function can have ONLY positional arguments.

To specify positional-only arguments, add `, /` after the arguments:

```python
def my_function(name, /):  
  print("Hello", name)  
  
my_function("Emil")
```

### Keyword only arguments
To specify that a function can have only keyword arguments, add `*,` _before_ the arguments:
```python
def my_function(*, name):  
  print("Hello", name)  
  
my_function(name = "Emil")
```

### Avoid argument errors
Unmatched  arguments occur when we provide fewer or more arguments than a function needs to do its work.

Python is helpful in that it reads the funciton 's code for us and tells us the names of the arguments we need to provide. This is another motivation for giving your variables  and functions descriptive names. If you do, Python’s error  messages will be more useful to you and anyone else who  might use your code.

## Function Names
Function names follow the same rules as variable names in Python:
- A function name must start with a letter or underscore
- A function name can only contain letters, numbers, and underscores
- Function names are case-sensitive

## Return values
Functions can send data back to the code that called them using the `return` statement.

When a function reaches a `return` statement, it stops executing and sends the result back:
```python
def my_function(x, y):
	retrun x+y

result = my_function(5, 3)
print(result)
```
### Returning different data types
Functions can return any data type, including lists, tuples, dictionaries, and more.
```python
def my_function():  
  return ["apple", "banana", "cherry"] 
  
fruits = my_function()  
print(fruits[0])  
print(fruits[1])  
print(fruits[2])
```

### None type
If we do not define the return values of a function, the function will return the none by default.
```python
def say():
    print("hi")

result = say()
print(type(result))
```

The program will output the `<class 'NoneType'>`.


## The pass statement
Function definitions cannot be empty. If you need to create a function placeholder without any code, use the `pass` statement:

```python
def my_function():  
  pass
```


# How to call a function
When we want to use a function, we have to call it. A *function call* tells Python to execute the code in the function. To call a function, we can write the name of the function, followed by any necessary information in parentheses.
```python
func_name(parameter)
```

We can call the same function multiple times.


# Python \*args and \*\*kwargs
By default, a function must be called with the correct number of arguments.

However, sometimes you may not know how many arguments that will be passed into your function.

\*args and \*\*kwargs allow functions to accept a unknown number of arguments.
## Arbitrary Arguments - \* args
If you do not know how many arguments will be passed into your function, add a `*` before the parameter name.

This way, the function will receive a _tuple_ of arguments and can access the items accordingly:

```python
def my_function(*kids):  
  print("The youngest child is " + kids[2])  
  
my_function("Emil", "Tobias", "Linus")****
```

### What is \*args?
The `*args` parameter allows a function to accept any number of positional arguments.

Inside the function, `args` becomes a tuple containing all the passed arguments:

```python
def my_function(*args):  
  print("Type:", type(args))  
  print("First argument:", args[0])  
  print("Second argument:", args[1])  
  print("All arguments:", args)  
  
my_function("Emil", "Tobias", "Linus")
```

### Using \ *args with Regular Arguments

We can combine regular parameters with \*args.
Regular parameters must come before \*args.

```python
def my_function(greeting, *names):  
  for name in names:  
    print(greeting, name)  
  
my_function("Hello", "Emil", "Tobias", "Linus")
```

## Arbitrary Keyword Arguments \*\*kwargs
If you do not know how many keyword arguments will be passed into your function, add two asterisks `**` before the parameter name.

This way, the function will receive a _dictionary_ of arguments and can access the items accordingly:
```python
def my_function(****kid**):  
  print("His last name is " + kid["lname"])  
  
my_function(fname = "Tobias", lname = "Refsnes")
```


### What is \*\*kwargs
The `**kwargs` parameter allows a function to accept any number of keyword arguments.

Inside the function, `kwargs` becomes a dictionary containing all the keyword arguments:


TODO

# Python Scope
A variable is only available from inside the region it is created. This is called **scope**.

## Local Scope
A variable created inside a function belongs to the _local scope_ of that function, and can only be used inside that function. The variable `x` is not available outside the function, but it is available for any function inside the function:

```python
def myfunc():  
  x = 300  
  def myinnerfunc():  
    print(x)  
  myinnerfunc()  
  
myfunc()
```

## Global Scope
A variable created in the main body of the Python code is a global variable and belongs to the global scope.

Global variables are available from within any scope, global and local.

```python
x = 300  
  
def myfunc():  
  print(x)  
  
myfunc()  
  
print(x)
```

## Variables with same names inside and outside of function
If you operate with the same variable name inside and outside of a function, Python will treat them as two separate variables, one available in the global scope (outside the function) and one available in the local scope (inside the function):
```python
x = 300  
  
def myfunc():  
  x = 200  
  print(x)  
  
myfunc()  
  
print(x)
```

## Global Keyword
If you need to create a global variable, but are stuck in the local scope, you can use the `global` keyword.

The `global` keyword makes the variable global.

```python
def myfunc():  
  global x  
  x = 300  
  
myfunc()  
  
print(x)
```

## Nonlocal keyword

The `nonlocal` keyword is used to work with variables inside nested functions.
The `nonlocal` keyword makes the variable belong to the outer function.

# Python Decorators
Decorators let you add extra behavior to a function, without changing the function's code.

A decorator is a function that takes another function as input and returns a new function.
## Basic Decorator
 
```python
# decorator function
def changecase(func):  
  def myinner():  
    return func().upper()  
  return myinner  
  
# define the function that will use the decorator
@changecase  
def myfunction():  
  return "Hello Sally"  
  
print(myfunction())
```

```output
HELLO SALLY
```

By placing `@changecase` directly above the function definition, the function `myfunction` is being "decorated" with the `changecase` function.

The function `changecase` is the decorator.

The function `myfunction` is the function that gets decorated.

## What happened inside the decorator
when we use the `@decorator`, actually it is the same as below:
```python
myfunction = changecase(myfunction)
```

## Why we need decorator
1. 代码复用性：相同的功能可以应用到多个函数上。
2. 不修改原函数：保持原函数的纯净性

## Multiple decorator calls

A decorator can be called multiple times, just place the decorator above the function you want to decorate

```python
def changecase(func):
    def inner():
        return func().upper()
    return inner

@changecase
def myfunction():
    return "hello world"

@changecase
def otherfunction():
    return "I am speed!"

print(myfunction())
print(otherfunction())
```
## Arguments in the decorated function
Function that requires arguments can also be decorated, just make sure you pass the arguments to the wrapper function:

```python
def changecase(func):
	def myinner(x):
		return func(x).upper()
	return myinner
	
@changecase
def myfunction(nam):
	return "Hello " + nam

print(myfunction("John"))
```

# Storing our function in modules
The advantage of functions is the way they seperate blocks of code from our mian program. When we use descriptive names for our functions, our programs become much easier to follow.

We can go a step further by storing our functions in a separate file called a module and then importing that module into your main program. An `import` statement tells Python to make the code in a module  available in the currently running program file.

## Importing an Entire Module
To start importing functions, we first need to create a module. A module is a file ending in `.py` that contains the code you want to import into your program. Let’s make a module that contains the function `make_pizza()`.

> pizza.py

```python
def make_pizza(size, *toppings):
	print(f"\nMaking a {size}-inch pizza with the following toppings:")
	for topping in toppings:
		print(f"-{topping}")
```

Now we will make a separate file called `making_pizzas.py` in the same directory as `pizza.py`. This file imports the module we just created and tehn makes two calls to `make_pizza()`:
> making_pizzas.py

```python
import pizza
```

When python reads the file, the `import` line tells python to open the file `pizza.py` and copy all the functions from it into this program. Any function defined in `pizza.py` will now be available in `making_pizzas.py`.

**Summary**
This first approach to importing, in which we simply **write import followed by the name of the module**, makes **every function from the module available in our program**. If we use this kind of import statement to import an entire module  named `module_name.py`, each function in the module is  available through the following syntax:
```python
module_name.function()
```

## Importing specific functions
Syntax:
```python
from module_name import function_name

# import as many functions as we want from a module
from module_name import func_0, func_1, func_2
```
## Using `as` to give function another name
If the name of a function we’re importing might conflict  with an existing name in our program, or if the function name is long, we can use a short, unique alias—an  alternate name similar to a nickname for the function.

For example, later we will introduce `matplotlib.pyplot` funcion to draw. To import, it is common to see:
```python
import matplotlib.pyplot as plt
```

The general syntax for providing an alias is:
```python
from module_name import function_name as fn
```

## Using `as` to give module another name
We can also provide an alias for a module name. Giving a module a short name like `p` for `pizza`, llows us to call the module’s functions more quickly. Calling `p.make_pizza()` is  more concise than calling `pizza.make_pizza()`.

The general syntax for this approach is:
```python
import module_name as mn
```

## Importing All functions in a Module

We can tell python to import all function in a module by using the `*` operator:
```python
from piazza import *
```

The `*` in the import statement tells Python to copy every function from the module `piazza` into this program file. Because every function is imported, we can tell each function by name without the dot notation.

However, it's best not to use this approach when you are working with larger modules that we didn't write: if the module has a function name that maches an existing name in our project, we may get unexpected results.

# Styling Functions

1. Functions should have descriptive names, and these names should use lowercase letters and underscores.
2. Every function should have a comment that explains  concisely what the function does. This comment should  appear immediately after the function definition and use the  docstring format.

