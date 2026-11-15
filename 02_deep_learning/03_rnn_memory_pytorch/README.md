# 03 - RNN：读完整个序列，记住第一个信号

用 PyTorch 的张量运算手写一个最简单的 RNN（不用 `nn.RNN`），在自己生成的序列任务上训练：第一个数字随机为 ±1，后面是 Uniform(-1, 1) 的干扰，网络读完整个序列后判断第一个数字的正负。观察序列长度 T = 10 / 30 / 100 时的训练难度。

## 状态

练习版本。7 个函数 / 方法保留签名、docstring 和 TODO，函数体待实现。公式（含 BPTT、梯度消失 / 爆炸、梯度裁剪）、API 速查表（含 NumPy / PyTorch / TensorFlow 对比）、自检单元格和全部绘图代码已提供。本目录不包含参考答案。

## 环境与运行

在本目录执行：

```bash
uv sync
```

然后在 VS Code / Jupyter 中打开 `rnn_memory_zh.ipynb`，选择 `.venv/bin/python` 作为 kernel，从上往下运行。序列模型的张量很小，Notebook 固定在 CPU 上运行，完整实验（T = 10 / 30 / 100 各 20 轮）在普通笔记本上约需一分钟。

依赖：PyTorch、NumPy、Matplotlib、ipykernel。

## 内容

| Lab | 主题 | 待实现函数 |
| --- | --- | --- |
| 1 | 生成序列数据 | `generate_sequences` |
| 2 | RNN 的一步和整个序列 | `SimpleRNN.__init__`, `rnn_step`, `forward` |
| 3 | BPTT 与每个时间步的梯度范数 | `hidden_grad_norms` |
| 4 | 训练流程：梯度裁剪、记录裁剪前梯度范数 | `train_epoch`, `evaluate` |
| 5 | T = 10 / 30 / 100 实验与记录 | 无 |

覆盖的概念：hidden state、时间步之间的参数共享、many-to-one、BPTT、梯度消失与梯度爆炸、梯度裁剪。

已提供的观察图：样本序列、三个时间步的展开计算图、共享参数梯度等于各时间步贡献之和、各时间步的梯度范数、三种序列长度的 loss / 准确率 / 梯度范数曲线。

下一步：[04 - LSTM](../04_lstm_memory_pytorch/README.md)。

[返回 Deep learning](../README.md)
