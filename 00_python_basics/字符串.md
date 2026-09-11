 Python 中的定义形式：
 1. 单引号定义：`name = 'abc'`
 2. 双引号定义：`name = "abc"`
 3. 三引号定义：`name = """abc"""`

- 三引号定义，和多行注释写法一样，支持换行操作，使用变量接收就是字符串，不用变量接收就是多行注释。
- 字符串里面的引号记得使用 `\` 转义
## Strings are Arrays
就像其他编程语言一样，python 中的字符串就是 unicodo 字符串的数组。但是，Python 中没有字符数据类型，一个单字符就是一个长度为一的字符串。
语法：
```python
a = "Hello, world"
print(a[1])
```
### 遍历字符串

> looping through a String

Since strings are arrays, we can loop through the characters in a string, with a `for`  loop

```python
for x in "banana":
	print(x)
```

### 字符串长度
to get the length of a string, use the `len()` function.

```python
a = "hello world"
print(len(a))
```
### 判断子字符串
To check if a certain phrase or character is present in a string, we can use the keyword `in`.
```python
txt = "The best things in life are free!"
print("free" in txt)
```

Also , we can add `not` keyword to check if a word exist in the string.
```python
txt = "The best things in life are free!"
print("free" not in txt)
```
## 分割字符串
You can return a range of characters by using the slice syntax.

Specify the start index and the end index, separated by a colon, to return a part of the string.

```python
b = "Hello, World!"  
print(b[2:5])
```

- By leaving out the start index, the range will start at the first character
```python
b = "Hello, World!"  
print(b[:5])
```

- Likewise, we can leaving out the end index, meaning that the range will go to the end:
```python
b = "Hello, World!"  
print(b[2:])
```

- Negative Indexing: use negative indexes to start the slice from the end of the string. Remember to have from smaller to larger. ( index 顺序很重要 )
```pyhon
b = "Hello, World!"  
print(b[-5:-2])
```
## 更改字符串
Python has a set of built-in methods that you can use on strings.

- Upper case: The `upper()` method returns the string in upper case
```python
a = "Hello, World!"  
print(a.upper())
```

- Lower case: The `lower()` method returns the string in lower case:
```python
a = "Hello, World!"  
print(a.lower())
```

- Remove Whitespace: whitespace is the space before and/or after the actual text, use `strip()` to remove the space.

```python
a = " Hello, World! "  
print(a.strip()) # returns "Hello, World!"
```

- replace string: `replace()` method replaces a string with another string:
```python
a = "Hello, World!"  
print(a.replace("H", "J"))
```

- Split String: `split()` method splits the string into substrings if it finds instances of the separator
```python
a = "Hello, World!"  
print(a.split(",")) # returns ['Hello', ' World!']
```



## 字符串拼接

使用 `+` 进行拼接字符串本身。

```python
name = 'abc'
str = 'someone is'
print(str + name)
```

## 字符串格式化

Python 中支持非常多的数据类型占位，最常用的是下面三类：

| 格式符号 | 转化                |
| ---- | ----------------- |
| %s   | 将内容转成字符串，放入占位位置   |
| %d   | 将内容转换成整数，放入占位位置   |
| %f   | 将内容转换为浮点类型，放入占位位置 |
### 格式化的精度控制

```python
num = 19.99
print("num is: %f" %num)
```
输出是：
`num is: 19.990000`

这是因为没有对数字进行输出的精度控制，我们可以使用 **m.n** 来控制数据的宽度和精度。
- m，控制宽度，要求是数字。（很少使用）设置的宽度小于数字自身，不生效。
- .n 控制小数点精度，要求是数字，会进行小数的四舍五入。

示例：
- `%5d` 表示将整数的宽度控制在 5 位，如果数字宽度不足，前面补上空格。
- `%5.2f` 表示将宽度控制位 5，小数点精度设置为 2。
	- 小数点和小数部分也算入宽度计算

### 另一种字符串格式化的方式 F-Strings
F-String was introduced in Python 3.6 and is now the preferred way of formatting strings.
To specify a string as an f-string, simply put an `f` in front of the string then add curly brackets `{}`.

**快速格式化：**
`f“内容{变量}”`

- 特点：不限制数据类型，也不做精度控制。



# 参考内容
