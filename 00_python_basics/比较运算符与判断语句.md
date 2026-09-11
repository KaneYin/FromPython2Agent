# 布尔类型

| 运算符 | 描述     |
| --- | ------ |
| ==  | 是否相等   |
| !=  | 是否不等   |
| >   | 是否大于   |
| <   | 是否小于   |
| >=  | 是否大于等于 |
| <=  | 是否小于等于 |

# 判断语句

1. if 语句
	格式：

```python
if condition:
    do something
```

注意：
- 空格缩进，作用相当于定义 if 作用的范围

 2. if-else 组合使用
	格式：
```python
if condition:
    do something
else:
	do some other things
```

3. if-elif-else 组合使用
	格式：

```python
if condition1:
	do a
elif condition2:
	do b
elif condtion3:
	do c
else:
	do other things
```

注意：
- 判断是互斥并且有顺序的。
- else 可以不写，效果相当于几个单独的 if 语句

## 嵌套判断语句

注意点就是语句内的缩进。

## `pass` statement

由于 `if` 语句不能为空，但是我们有时候需要写空 `if` 语句，这个时候我们就需要使用 `pass` statement 用来避免程序出错。
```python
a = 33  
b = 200  
  
if b > a:  
  pass
```

`pass` 语句是一个空操作，当这条语句执行的时候没有事情发生。作用仅仅是一个占位符。

相比于注释来说，pass 语句不会被 python 编译器忽略，如果在 if 范围内使用注释，由于注释会被编译器忽略，最终就导致 pyhon 抛出错误。

Pass 语句也可以用在其他地方，比如定义在函数中：
```python
def calculate_discount(price):  
  pass # TODO: Implement discount logic  
  
# Function exists but doesn't do anything yet
```

> While we focus on pass with if statements here, it's also commonly used with loops, functions, and classes.

