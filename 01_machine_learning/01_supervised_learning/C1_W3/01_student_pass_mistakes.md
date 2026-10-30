# 错题本：学生期末考试通过预测（Logistic Regression 从零实现）

对应练习：[01_student_pass_logistic_regression_exercises.ipynb](01_student_pass_logistic_regression_exercises.ipynb)

英文课程对照：[C1_W3_Logistic_Regression.ipynb](C1_W3_Logistic_Regression.ipynb)（共同算法见第 2 节；第 3 节正则化是额外内容）。
本分支的练习 notebook 保留 TODO 函数体和针对这些错误的自检，供读者自行实现。
下面保留个人学习时的错误与修正示例；建议先独立尝试，再查阅本记录。

按练习顺序整理。每一条包括：当时的写法、问题出在哪、正确写法、要记住的点。

---

## 练习 A — 特征标准化

### A-1 计算结果没有赋值给变量

```python
# ❌
np.mean(X_train, axis=0)
np.std(X_train, axis=0, ddof=0, keepdims=True)

# ✅
mean = np.mean(X_train, axis=0, keepdims=True)
scale = np.std(X_train, axis=0, ddof=0, keepdims=True)
```

- 表达式算完不赋值，结果马上就丢了，后面的代码拿不到。
- `np.mean` 也要加 `keepdims=True`，约定的形状是 `(1, d)`，不是 `(d,)`。

### A-2 布尔索引写成了推导式

```python
# ❌ 语法错误；就算能运行，也会把所有位置都设成 1
scale[i for i in range(len(bool_arr))] = 1

# ✅ 布尔数组直接当下标，只改 True 的位置
scale[scale <= eps] = 1.0
```

### A-3 最后忘了 return

`raise NotImplementedError(...)` 还留着，函数算完就抛异常。要换成 `return mean, scale`。

### 相关概念

| 概念 | 要点 |
|---|---|
| `axis=0` | 沿样本方向（跨行）汇总，**每个特征**得到一个数。`axis=1` 是每个样本一个数，把不同特征混在一起平均，没有意义。 |
| `keepdims=True` | 被汇总掉的那一维保留为 1：`(m, d)` → `(1, d)`。形状带方向，广播时不会对错位置。 |
| `ddof` | 标准差的分母是 `N - ddof`。`0` 是总体标准差（NumPy 默认），`1` 是样本标准差（pandas 默认）。本题用 0，否则标准化后标准差不等于 1。`np.mean` **没有** `ddof` 参数。 |
| `eps` | 只是判断“标准差是否接近 0”的阈值。满足条件的列，缩放因子设为 **1**，不是设为 eps。除以 eps 会把浮点误差放大 10¹² 倍。 |

官方文档：[`np.mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)、[`np.std`](https://numpy.org/doc/stable/reference/generated/numpy.std.html)、[`boolean indexing`](https://numpy.org/doc/stable/user/basics.indexing.html#boolean-array-indexing)。

---

## 练习 B — 初始化参数

### B-1 函数内部用了全局变量 `d`，而不是参数 `n_features`

```python
def initialize_parameters(n_features):
    W = np.zeros((d, 1), dtype=float)            # ❌ d 是从全局作用域读到的
    W = np.zeros((n_features, 1), dtype=float)   # ✅
```

- 自检里写了 `for d in (3, 5): initialize_parameters(d)`，全局 `d` 恰好等于传入的参数，所以 **B 的自检碰巧通过了**。
- 循环结束后全局 `d = 5`。到了练习 H，传入 `n_features=1`，却得到 `(5, 1)` 的 W，报错：`(2,1) @ (5,1)` → `size 5 is different from 1`。
- **教训**：函数只用自己的参数和局部变量。“自检过了，换个地方调用就出错”，多半是读了全局变量。notebook 里前面格子留下的变量会一直留在 kernel 里，特别容易出这种问题。

官方文档：[`np.zeros`](https://numpy.org/doc/stable/reference/generated/numpy.zeros.html)。

---

## 练习 C — Sigmoid

### C-1 只写了公式的一部分

```python
ans = np.exp(-Z)              # ❌ 只算了 e^{-z}
return 1 / (1 + np.exp(-Z))   # ✅ σ(z) = 1 / (1 + e^{-z})
```

用自检输入快速核对：σ(0) 应该等于 0.5，而 `exp(0) = 1`。另外，σ 的结果要随 z 递增，并且落在 [0, 1] 之间。

官方文档：[`np.exp`](https://numpy.org/doc/stable/reference/generated/numpy.exp.html)。

---

## 练习 D — 前向传播

### D-1 把矩阵乘法写成了逐元素乘法

```python
Z = X * W + b   # ❌ 逐元素乘 + 广播，不会求和
Z = X @ W + b   # ✅ (m, d) @ (d, 1) → (m, 1)
```

| 运算 | 写法 |
|---|---|
| 逐元素加减乘除 | `+ - * /` |
| 矩阵乘法 | `@` 或 `np.dot` |

- 自检里 m = d = 2，`X * W` 能广播成功，只是得到了 `(2, 2)`，**不会报错**。换成真实数据 `(1600, 3) * (3, 1)` 才会报错。
- **检查方法**：先在纸上对形状，`(m, d) @ (d, 1)` 中间两维必须相等。

官方文档：[`np.matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)、[`np.dot`](https://numpy.org/doc/stable/reference/generated/numpy.dot.html)、[`np.multiply`](https://numpy.org/doc/stable/reference/generated/numpy.multiply.html)、[`broadcasting`](https://numpy.org/doc/stable/user/basics.broadcasting.html)。

---

## 练习 E — 二元交叉熵

### E-1 拼写错误

`keepdims=Teue` → 报 `NameError`。

### E-2 给 `np.mean` 传了 `ddof`

`ddof` 只属于 `np.std` 和 `np.var`，传给 `np.mean` 会报 `TypeError`。

### E-3 返回了数组，不是 float

```python
# ❌ 返回 (1, 1) 数组
return -np.mean(..., axis=0, keepdims=True)

# ✅ 对全部样本求平均，再转成 Python float
return float(-np.mean(...))
```

练习 A 需要“每列一个数”，所以用 `axis=0, keepdims=True`。损失是“全部样本一个数”，不需要指定 axis。

### E-4 没有裁剪概率

预测值恰好是 0 或 1 时，会出现 `log(0) = -inf` 和 `0 × (-inf) = nan`。

```python
y_hat_safe = np.clip(y_hat, eps, 1 - eps)   # 返回新数组，不修改原 y_hat
```

- 范围两端都要防：下限防 `log(ŷ)`，上限防 `log(1 - ŷ)`。
- 浮点数下 `sigmoid(40)` 恰好等于 `1.0`，所以这种情况在训练中真的会出现。

### E-5 `np.clip` 第一个参数写错

```python
np.clip(eps, eps, 1 - eps)     # ❌ 裁剪的是 eps 自己，结果恒为 1e-12
np.clip(y_hat, eps, 1 - eps)   # ✅ np.clip(数组, 下限, 上限)
```

官方文档：[`np.mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)、[`np.var`](https://numpy.org/doc/stable/reference/generated/numpy.var.html)、[`np.std`](https://numpy.org/doc/stable/reference/generated/numpy.std.html)、[`np.clip`](https://numpy.org/doc/stable/reference/generated/numpy.clip.html)、[`np.log`](https://numpy.org/doc/stable/reference/generated/numpy.log.html)、[`float`](https://docs.python.org/3.13/library/functions.html#float)。

---

## 练习 F — 反向传播

### F-1 求和之后又求了一次平均，平均错了维度

```python
dw = np.mean(X.T @ diff)   # ❌ 把 d 个特征的梯度平均成了一个标量
dW = X.T @ diff / m        # ✅ (d, m) @ (m, 1) → (d, 1)
```

- `X.T @ diff` 本身已经对 m 个样本求和了，只剩下“除以 m”这一步。
- 平均只做一次：`@` 负责求和，`/ m` 负责平均。
- F1 里已经求了 `m`，却没用上，这本身就是一个提示。

### 相关概念：运算符优先级

`@` 和 `* / // %` **同一级**，从左到右计算。所以 `X.T @ diff / m` 等于 `(X.T @ diff) / m`。不确定的时候就加括号。

官方文档：[`np.matmul`](https://numpy.org/doc/stable/reference/generated/numpy.matmul.html)、[`ndarray.T`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.T.html)、[`np.mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)、[`operator precedence`](https://docs.python.org/3.13/reference/expressions.html#operator-precedence)。

---

## 练习 H — 训练循环

### H-1 初始化时传了样本数，而不是特征数

```python
initialize_parameters(X_train.shape[0])   # ❌ shape[0] 是 m（样本数）
initialize_parameters(X_train.shape[1])   # ✅ shape[1] 是 d（特征数）
```

### H-2 预先填 0 之后又 append

```python
loss_history = [0] * num_iterations   # ❌ 再 append，长度会变成 2 倍，前一半全是 0
loss_history = []                     # ✅ 空列表 + append
```

“预分配后按下标赋值”和“空列表 + append”只能选一种，不能混用。

### H-3 变量名大小写写错

`x_train` ≠ `X_train`，会报 `NameError`。Python 区分大小写。

### H-4 更新后的参数赋给了错误的变量（最关键）

```python
dW = W_new; db = b_new   # ❌ W 和 b 一直是初始的 0，模型完全没有学习
W = W_new; b = b_new     # ✅
```

迹象：每一轮的损失都是 0.693（log 2），一直不下降。

### H-5 没有 return

函数没有 `return` 时，Python 会返回 `None`，调用方解包时会报错。`return W, b, loss_history` 要和 `for` 对齐，写在循环外面。

官方文档：[`ndarray.shape`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.shape.html)、[`range`](https://docs.python.org/3.13/library/stdtypes.html#range)、[`list.append`](https://docs.python.org/3.13/tutorial/datastructures.html#more-on-lists)。

---

## 练习 I — 预测与准确率

### I-1 阈值比较少了等号

```python
y_hat > threshold    # ❌ 0.5 会被判成 0
y_hat >= threshold   # ✅ 题目约定恰好等于阈值时归为 1
```

边界条件要逐字看题目的约定，自检往往会专门测边界值。

### I-2 用异或计算准确率

```python
1 - np.mean(y_true ^ y_pred)          # 能算对，但只适用于整数，意图也不直观
float(np.mean(y_true == y_pred))      # ✅ 布尔数组求平均就是正确比例
```

可选：先 `assert y_true.shape == y_pred.shape`，防止 `(m, 1)` 和 `(m,)` 广播成 `(m, m)`。

官方文档：[`ndarray.astype`](https://numpy.org/doc/stable/reference/generated/numpy.ndarray.astype.html)、[`np.mean`](https://numpy.org/doc/stable/reference/generated/numpy.mean.html)、[`broadcasting`](https://numpy.org/doc/stable/user/basics.broadcasting.html)。

---

## 工具使用

### 编辑器里的代码没有保存

编辑器里改了代码，但 notebook 文件没有保存，磁盘上的版本还是旧的。

- 记得 `Cmd+S` 保存。
- 改完之前练习里的函数后，要**重新运行定义它的格子**，kernel 里的函数才会更新。
- 最稳妥的做法：Restart Kernel → Run All。

---

## 总结：反复出现的几类错误

1. **形状和维度**：`axis`、`keepdims`、`shape[0]` 和 `shape[1]`、`*` 和 `@`、多做一次 mean。写代码前先在纸上推一遍形状。
2. **算完没有接住**：没赋值、赋给了错误的变量、没有 return、`raise` 没删。
3. **返回类型**：约定返回 Python `float` 时，用 `float(...)` 包一层，不要返回 `(1, 1)` 数组。
4. **边界和数值稳定**：`>=` 还是 `>`、`log(0)`、除以 0。题目里写到的边界约定，自检基本都会测。
5. **作用域**：函数里不要读全局变量。notebook 的 kernel 状态会“帮你”掩盖这类 bug。
6. **API 参数**：先确认函数支不支持这个参数（`np.mean` 没有 `ddof`），以及参数顺序（`np.clip(数组, 下限, 上限)`）。
