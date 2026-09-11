# frozenset
`frozenset()` function returns an unchangeable frozenset object (which is like a `set` object, only unchangeable)

**Syntax**:
`frozenset(iterable)`

> This will cause an error

```python
mylist = ['apple', 'banana', 'cherry']
x = frozenset(mylist)
x[1] = 'newapple' 
```

# getattr

`getattr()` function returns the value of the specified attribute from the specified object

**Syntax**:
`getattr(_object_, _attribute_, _default_)`



# References
1. https://www.w3schools.com/python/ref_func_frozenset.asp