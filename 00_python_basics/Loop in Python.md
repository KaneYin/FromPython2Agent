Python has two primitive loop commands:
- `while` loop
- `for` loop
# While loops
With the while loop we can execute a set of statements as long as a condition is true.
```python
i = 1  
while i < 6:  
  print(i)  
  i += 1
```

> Note: remember to increment i, or else the loop will continue forever.

The `while` loop requires relevant variables to be ready, in this example we need to define an indexing variable, `i` which we set to 1.

## The break statement
With the `break` statement we can stop the loop even if the while condition is true:

```python
i = 1  
while i < 6:  
  print(i)  
  if i == 3:  
    break  
  i += 1
```

## The continue statement
With the `continue` statement we can stop the current iteration, and continue with the next:
```python
i = 0  
while i < 6:  
  i += 1  
  if i == 3:  
    continue  
  print(i)
```

> 结果不会包含 3，因为 continue 语句会跳出当前循环但是继续整个循环。

## The else statement
With the `else` statement we can run a block of code once when the condition no longer is true:
```python
i = 1  
while i < 6:  
  print(i)  
  i += 1  
else:  
  print("i is no longer less than 6")
```

# Python For loops

A for loop is used for iterating over a sequence (that is either a list, a tuple, a dictionary, a set, or a string).

This is less like the [for](https://www.w3schools.com/python/ref_keyword_for.asp) keyword in other programming languages, and works more like an iterator method as found in other object-orientated programming languages.

With the [for](https://www.w3schools.com/python/ref_keyword_for.asp) loop we can execute a set of statements, once for each item in a list, tuple, set etc.

基础语法：
```
for 临时变量 in 序列类型:
	循环满足条件时执行的代码
```

```python
name = "hello world"
for x in name:
	print(x)
```

所谓序列类型，就是指内容可以一个个依次取出来的一种类型，包括：
- 字符串
- 列表
- 元组
- 等

for 循环语句，本质上是遍历：序列类型。通过 range 语句可以构建序列类型。
## range
1. `range(num)`，获取一个从 0 开始，到 num 结束的数字序列（不包含 num 本身）
2. `range(num1, num2)` , 获取一个从 num1 开始，到 num2 结束的数字序列，不包含num2 本身。
3. `range(num1, num2, step)`, 获得一个从 num1 开始，到 num2 结束的数字序列，数字之间的步长为 step

## 变量作用域

for 循环里面的临时变量，在编程规范上，作用域只限定在 for 循环内部。

但是如果我们强行编程在 for 循环外部访问临时变量：
- 实际上是可以访问到的
- 在编程规范上不建议这样做

解决办法就是在 for 循环之前先定义好这个临时变量。
