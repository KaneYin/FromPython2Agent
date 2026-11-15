# 01 - Two-Layer Neural Network（NumPy 从零实现）

[English](README.md)

只用 NumPy 手写一个 `2 → 5 → 1` 的两层神经网络，在 Two Moons 数据集上做二分类。练习内容包括 Forward Propagation、Binary Cross-Entropy、Backpropagation、Numerical Gradient Checking 和 Batch Gradient Descent。

## 状态

练习版本。14 个核心函数保留签名、docstring 和 TODO，函数体待实现。公式、API 速查表、自检单元格和全部绘图代码已提供。不包含参考答案。

| Notebook | 语言 |
| --- | --- |
| `two_moons_two_layer_nn_zh.ipynb` | 中文 |
| `two_moons_two_layer_nn_en.ipynb` | English |

两份 notebook 的单元格一一对应，代码、自检和期望值相同。

## 环境与运行

在本目录执行：

```bash
uv sync
```

然后在 VS Code / Jupyter 中打开 `two_moons_two_layer_nn_zh.ipynb`，选择 `.venv/bin/python` 作为 kernel，从上往下运行。实现完一个函数后，运行紧随其后的自检单元格。

依赖：NumPy（模型）、scikit-learn（只用于 `make_moons` 和 `train_test_split`）、Matplotlib（绘图）、ipykernel。

## 内容

| Lab | 主题 | 待实现函数 |
| --- | --- | --- |
| 1 | 数据准备 | `standardize_features` |
| 2 | 参数初始化（He） | `initialize_parameters` |
| 3 | Forward Propagation | `relu`, `relu_derivative`, `sigmoid`, `forward` |
| 4 | Loss 与 Backpropagation | `compute_loss`, `backward`, `gradient_check` |
| 5 | 训练循环 | `update_parameters`, `train` |
| 6 | 评估与可视化 | `predict_proba`, `predict`, `accuracy` |
| 7 | 学习率 / 隐藏层宽度实验 | 无 |

已提供的观察图：数据散点图、He 初始化分布、激活函数曲线、梯度检查误差、Loss Curve、NN 与 Logistic Regression 的决策边界对比、每个隐藏神经元的激活图、决策边界随训练的演化、学习率对比、隐藏层宽度对比。

[返回 Deep learning](../README.md)
