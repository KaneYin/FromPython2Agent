# Creating and using a class
## Creating class
> dog.py

```python
class Dog:
	"""
	A simple attempt to model a dog.
	"""
	
	def __init__(self, name, age):
	    self.name = name
	    self.age = age
	    
	def sit(self):
		print(f"{self.name} is now sitting")
	
	def roll_over(self):
		print(f"{self.name} r oller over")
```

To create a class, use the keyword `class`:
```python
class MyClass:
	x = 5
```

Now we can use the class named MyClass to create objects:
```python
p1 = MyClass()
print(p1.x)
```

We can also delete objects by using the `del` keyword:
```python
del p1
```

Class definitions cannot be empty, but if you for some reason have a class definition with no content, put in the pass statement to avoid getting an error.
```python
class Person:  
  pass
```

## `__init()__` method

All classes have a built-in method called `__init__()`, which is **always executed** when the class is being initiated.

The `__init__()` method is used to assign values to object properties, or to perform operations that are necessary when the object is being created.
```python
class Person:
	def __init__(self, name, age):
	self.name = name
	self.age = age
	
p1 = Person("Emil". 36)

print(p1.name)
print(p1.age)
```

Without the `__init__()` method, you would need to set properties manually for each object:
```python
class Person:  
  pass  
  
p1 = Person()  
p1.name = "Tobias"  
p1.age = 25  
  
print(p1.name)  
print(p1.age)
```

Using `__init__()`, we can set initial values when creating the object:
```python
class Person:
	def __init__(self, name, age):
		self.name = name
		self.age = age

p1 = Person("Linus", 28)

print(p1.name)
print(p1.age)
```

We can also set default values for parameters in the `__init__()` method:

```python
class Person:  
  def __init__(self, name, age=18):  
    self.name = name  
    self.age = age  
  
p1 = Person("Emil")  
p2 = Person("Tobias", 25)  
  
print(p1.name, p1.age)  
print(p2.name, p2.age)
```

## Python self Parameter
The self parameter is a reference to the current instance of the class.
It is used to access properties and methods that belong to the class.

```python
class Person:  
  def __init__(self, name, age):  
    self.name = name  
    self.age = age  
  
  def greet(self):  
    print("Hello, my name is " + self.name)  
  
p1 = Person("Emil", 25)  
p1.greet()
```

> **Note**: the `self` parameter must be the first parameter of any method in the class.

## Class Properties
Properties are variables that belong to a class. They store data for each object created from the class.

```python
class Person:  
  def __init__(self, name, age):  
    self.name = name  
    self.age = age  
  
p1 = Person("Emil", 36)  
  
print(p1.name)  
print(p1.age)
```

We can access object properties using dot notation. And we can also modify the value of properties on objects:
```python
class Person:
	def __init__(self, name, age):
		self.name = name
		self.age = age

p1 = Person("Tobias", 35)
print(p1.age)

p1.age = 26
print(p1.age)
```

We can delete properties from objects using the `del` keyword:
```python
class Person:  
  def __init__(self, name, age):  
    self.name = name  
    self.age = age  
  
p1 = Person("Linus", 30)  
  
del p1.age  
  
print(p1.name) # This works  
# print(p1.age) # This would cause an error
```

### Class Properties vs Object Properties
Properties defined inside `__init__()` belong to each object (instance properties).

Properties defined outside methods belong to the class itself (class properties) and are shared by all objects:
```python
class Person:  
  species = "Human" # Class property  
  
  def __init__(self, name):  
    self.name = name # Instance property  
  
p1 = Person("Emil")  
p2 = Person("Tobias")  
  
print(p1.name)  
print(p2.name)  
print(p1.species)  
print(p2.species)
```

### Modifying Class Properties
When we modify a class property, it affects all objects:

```python
class Person:
	lastname = ""
	
	def __init__(self, name)
		self.name = name

p1 = Person("Linus")
p2 = Person("Emil")

Person.lastname = "Refsnes"

print(p1.lastname)
print(p2.lastname)
```

## Class Methods

Methods are functions that belong to a class. They define the behavior of objects created from the class.

```python
class Person:
	def __init__(self, name):
		self.name = name
	
	def greet(self):
		print("Hello, my name is " + self.name)

p1 = Person("Emil")
p1.greet()
```

> Note: All methods must have `self` as the first parameter.

Methods can also accept parameters just like regular functions:
```python
class Calculator:
	def add(self, a, b):
		return a + b
	
	def multiply(self, a, b):
		return a * b
		
	calc = Calculator()
	print(calc.add(5, 3))
	print(calc.multuply(4, 7))
```

## Methods Accessing Properties
Methods can access and modify object properties using `self`.

```python
class Person:
	def __init__(self, name, age):
		self.name = name
		self.age = age
	
	def greet(self):
		print(f"{self.name} is {self.age} years old")
		
p = Person("kane", 18)
p.greet()
```

Methods can modify the properties of an object:
```python
class Person:
	def __init__(self, name, age):
		self.name = name
		self.age = age
	
	def celebrate_birthday(self):
		self.age += 1
		print(f"Happy birthday! You are now {self.age}")
		
p1 = Person("Linux", 25)
p1.celebrate_birthday()  
p1.celebrate_birthday()
```

### The `__str__()` Method
The `__str__()` method is a special method that controls what is returned when the object is printed:

Without the `__str__()` method:
```python
class Person:  
  def __init__(self, name, age):  
    self.name = name  
    self.age = age  
  
p1 = Person("Emil", 36)  
print(p1)
```

With the `__str__()` method:
```python
class Person:
	def __init__(self, name, age):
		self.name = name
		self.age = age
	def __str__(self):
		return f"{self.name} {self.age}"

p1 = Person("Tobias", 36)
print(p1)
```