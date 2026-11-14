# 04 - LSTM：在同一个记忆问题上替换 RNN cell

复用 [03 - RNN](../03_rnn_memory_pytorch/README.md) 的数据、划分和训练循环，手写 LSTM cell（输入门、遗忘门、候选信息、输出门和 cell state），与 `nn.LSTMCell` 核对，并在 T = 10 / 30 / 100 上和 RNN 对比。最后观察门值和 cell state 随时间的变化。

## 状态

练习版本。5 个函数 / 方法保留签名、docstring 和 TODO，函数体待实现。公式（含 LSTM 的 BPTT 和 cell state 加法路径的梯度）、API 速查表（含 NumPy / PyTorch / TensorFlow 对比）、自检单元格和全部绘图代码已提供。数据生成、训练循环和 RNN 对照模型直接复用上一个实验，已写好。本目录不包含参考答案。

长序列的结果是**实验观察**，受初始化、学习率和训练预算影响。Notebook 同时对比了遗忘门偏置 0 和 1 两种初始化，结果请以你自己运行的为准。

## 环境与运行

在本目录执行：

```bash
uv sync
```

然后在 VS Code / Jupyter 中打开 `lstm_memory_zh.ipynb`，选择 `.venv/bin/python` 作为 kernel，从上往下运行。Notebook 固定在 CPU 上运行，完整实验（3 种模型 × T = 10 / 30 / 100，各 20 轮）约需三到五分钟。

依赖：PyTorch、NumPy、Matplotlib、ipykernel。

## 内容

| Lab | 主题 | 待实现函数 |
| --- | --- | --- |
| 1 | LSTM 的一步和整个序列 | `LSTMClassifier.__init__`, `lstm_step`, `forward` |
| 2 | 与 `nn.LSTMCell` 核对单步输出 | `copy_weights_to_lstmcell` |
| 3 | T = 10 / 30 / 100，对比 RNN 与两种遗忘门初始化 | 无 |
| 4 | cell state 的加法路径与梯度 | 无 |
| 5 | 门值、cell state 随时间的变化 | `gate_trace_to_numpy` |

覆盖的概念：cell state 与 hidden state、四个门的作用、为什么门用 Sigmoid、候选信息用 Tanh、加法路径对梯度传递的影响、遗忘门偏置初值。

已提供的观察图：LSTM 一步的数据流、三种模型在三种序列长度下的准确率与 loss、各时间步的梯度范数（RNN 与不同 `forget_bias` 的 LSTM）、正负样本上的门值与 cell state 轨迹。

[返回 Deep learning](../README.md)
