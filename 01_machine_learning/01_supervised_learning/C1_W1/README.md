# C1_W1: 不依赖课程辅助库的版本

本目录的 3 个 notebook 现在直接使用 NumPy 和 Matplotlib 绘图，不需要缺失的课程文件 `lab_utils_uni.py`、`deeplearning.mplstyle` 或 `images/`。原来的 `compute_cost`、`compute_gradient`、`gradient_descent` 代码保持不变。

这里要区分两类依赖：NumPy 和 Matplotlib 是常见的第三方库，也不是 Python 标准库；`plt_intuition` 等则是课程自行封装的函数，并不是 Matplotlib 自带的 API。本次去掉的是后者。完全限制为 Python 标准库可以实现数值计算，但不适合这些 notebook 的科学绘图需求。

## 如何运行

1. 打开本目录任意一个 notebook。
2. 在 VS Code/Jupyter 中选择 `C1_W1/.venv/bin/python` 对应的 kernel。
3. Restart Kernel，然后 Run All。
4. 修改绘图 cell 中的参数并重跑该 cell，观察结果。

绘图默认使用静态输出，不需要 `%matplotlib widget`、`ipympl` 或 `ipywidgets`。环境配置和 lockfile 保持原样，没有安装新依赖。原有旧输出和执行编号已清空，以免显示旧课程函数生成的图。

`Cost_function_intuitive.ipynb` 与 `C1_W1_Lab03_Cost_function_Soln.ipynb` 都是 cost function 内容，保留两个文件并同步替换绘图。`C1_W1_Lab04_Gradient_Descent_Soln.ipynb` 演示梯度下降。原先缺失的课程图片引用已移除，相关解释和新生成的图保留在 notebook 中。

## 替换了什么

| 原有依赖/调用 | 当前实现 | 使用方式 |
| --- | --- | --- |
| `lab_utils_uni.plt_intuition` | cell 内定义的 `plot_cost_intuition`，直接使用 `scatter`、`plot`、`vlines` | 修改 `w` 和 `b`；左图看预测和残差，右图看固定 `b` 时的 cost 曲线 |
| `plt_stationary` + `plt_update_onclick` | 显式计算参数网格，用 `contour` 和 `plot_surface` 绘图 | 修改 `w_selected`、`b_selected` 后重跑，替代点击选点 |
| `soup_bowl` | 直接绘制 `z = u**2 + v**2` | 展示对称的凸碗形；明确区分它与真实 housing-data cost |
| `plt_gradients` | 调用原有 `compute_cost` / `compute_gradient`，再画切线和 `quiver` 箭头 | 左图固定 `b=100`，右图显示两个参数的梯度方向 |
| `plt_contour_wgrad` | cell 内定义的 `plot_descent_path` | 把真实的 `p_hist` 叠加到 cost 等高线上，包含起点和抽样更新箭头 |
| `plt_divergence` | 参数随迭代变化的折线图 + cost 的 `semilogy` 图 | 同时观察 `w`、`b` 的振荡和 cost 增长，替代原来的 3D 展示 |
| `plt_house_x` | 删除未使用的 import | 原 notebook 中没有调用它 |
| `deeplearning.mplstyle` | Matplotlib 自带设置与少量 `rcParams` | 不需要课程样式文件 |

静态图不保留原来的滑块、点击回调和交互旋转。参数修改后需要重跑 cell，但绘图和计算过程都能直接看到，也便于导出和复现。

## 更合适的实现建议

### 先保留循环，理解后再向量化

当前的 `compute_cost` 循环适合逐项对应公式，因此没有改写。理解后，可以另外尝试一个等价实现：

```python
def compute_cost_vectorized(x, y, w, b):
    predictions = w * x + b
    errors = predictions - y
    return np.mean(errors ** 2) / 2
```

这适用于当前 notebook 的非空一维 NumPy 数组 `x` 和 `y`，且二者长度相同。注意除以 `2`：课程使用的是 half MSE，而不是普通 MSE。

同理，梯度可写为：

```python
errors = w * x + b - y
dj_dw = np.mean(errors * x)
dj_db = np.mean(errors)
```

### 绘图 cell 展开计算，重复使用时再封装

当前只把重复使用的直觉图和训练轨迹图封装为 notebook 内可见的函数。其余图直接展开，使“生成候选参数 -> 计算预测 -> 计算 cost -> 绘图”这条过程可以逐行阅读。以后跨多个 notebook 复用时，再考虑抽取自己的 `plotting.py`。

参数网格通过 `np.meshgrid` 生成。代码中的 `W[..., np.newaxis]` 把 `(N_b, N_w)` 扩展成 `(N_b, N_w, 1)`，与 `(m,)` 的样本数组运算得到 `(N_b, N_w, m)` 的误差。`mean(..., axis=-1)` 只对样本求平均，保留每组参数对应的 cost。这使用了 [NumPy broadcasting](https://numpy.org/doc/stable/user/basics.broadcasting.html)。当前数据量很小，适合一次计算；数据变大后应控制网格大小或分批计算。

等高线与三维曲面分别使用 Matplotlib 的 [`Axes.contour`](https://matplotlib.org/stable/api/_as_gen/matplotlib.axes.Axes.contour.html) 和 [`Axes3D.plot_surface`](https://matplotlib.org/stable/api/toolkits/mplot3d/axes3d.html#mpl_toolkits.mplot3d.axes3d.Axes3D.plot_surface)。

### 想要滑块时，再加一个可选的交互层

如果 Jupyter 前端支持 widgets，可以在任意一个 cost notebook 的 `plot_cost_intuition` 定义之后，另开一个 cell：

```python
from ipywidgets import FloatSlider, fixed, interact

# Explicitly use the original two-point data; later cells change x_train/y_train.
_ = interact(
    plot_cost_intuition,
    x=fixed(np.array([1.0, 2.0])),
    y=fixed(np.array([300.0, 500.0])),
    w=FloatSlider(value=200, min=0, max=400, step=10, continuous_update=False),
    b=fixed(100.0),
)
```

这让 [`ipywidgets.interact`](https://ipywidgets.readthedocs.io/en/stable/examples/Using%20Interact.html) 在参数变化时重新调用同一个绘图函数，适合固定 `b=100` 后探索 `w`。它通过重新生成静态图工作，不需要启用 `%matplotlib widget`。如果前端不支持 widgets，继续使用默认的参数修改方式即可。
