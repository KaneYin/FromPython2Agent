# -*- coding: utf-8 -*-
""" 
Python String Basic Practice
Programming under each # TODO 
After done run the file to check
"""

print("=== Python String Practive ===\n")

# 1. count the len of a string
# input: s = "Hello, Python!"
# output: 14
s = "Hello, Python!"
# TODO: print len of a string
print(len(s))

# 2. To uppercase and lowercase
# input: s = "PyThOn"
# output: python, PYTHON
s = "PyThOn"
# TODO: 
print(s.lower())
print(s.upper())

# 3. strip the string
# input: s = "   Python  "
# output: Python
s = "   Python  "
# TODO: 
print(s.strip())

# 4. combine strings
# input: first = "Hello", last = "World"
# output: "Hello World!"
first = "Hello"
last = "World"
# TODO: combine strings and print
new = first + " " + last
print(new)

# 5. Tell if a String contains a substring
# input: s = "I love Python", sub = "Python"
# output: True
s = "I love Python"
sub = "Python"
# TODO
print(sub in s)

# 6. split a string
# input: s = "Python"
# output: Phy, hon
s = "Python"
# TODO: print first 3 letters and last 3 letters
print(s[:3])
print(s[-3:])

# 7. reverse a string
# input: s = "Python"
# output: "nohtyP"
s = "Python"
# TODO:
print(s[::-1])

# 8. Count a sub string
# input: s = "banana", sub = "a"
# output: 3
s = "banana"
sub = "a"
# TODO:
print(s.count(sub))
    

# 9. replace the substring
# input: s = "I like Java",  "Java" -> "Python"
# output: "I like Python"
s = "I like Java"
# TODO: 
print(s.replace("Java", "Python"))

# 10. 格式化字符串
# input: name = "Alice", age = 20
# output: "My name is Alice, I am 20 years old."
name = "Alice"
age = 20
# TODO:
print(f"My name is {name}, I am {age} years old.", name, age)


print("\n=== Congraduations! ===")
