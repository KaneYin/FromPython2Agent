# 02 - CNN on MNIST（NumPy 卷积 → PyTorch 分类器）

先用 NumPy 手写单通道卷积和池化，用固定的小矩阵手算并与 `nn.Conv2d` 对照，再用 PyTorch 搭建、训练、保存并测试一个 CNN，识别 MNIST 手写数字。目标测试准确率约 98%。

## 状态

练习版本。17 个函数 / 方法保留签名、docstring 和 TODO，函数体待实现。公式、API 速查表（含 NumPy / PyTorch / TensorFlow 对比）、自检单元格和全部绘图代码已提供。本目录不包含参考答案。

## 环境与运行

在本目录执行：

```bash
uv sync
```

然后在 VS Code / Jupyter 中打开 `cnn_mnist_zh.ipynb`，选择 `.venv/bin/python` 作为 kernel，从上往下运行。首次运行 Lab 4 会把 MNIST 下载到 `data/`（约 11 MB，已被 `.gitignore` 排除）。训练自动使用 CUDA / Apple MPS / CPU 中可用的一个。

依赖：PyTorch、torchvision、NumPy、Matplotlib、ipykernel。

## 内容

| Lab | 主题 | 待实现函数 |
| --- | --- | --- |
| 1 | NumPy 卷积 / 池化（逐步加入 padding、stride） | `conv_output_size`, `conv2d_forward`, `maxpool2d_forward`, `conv2d_multi_channel`（进阶） |
| 2 | 对照 `nn.Conv2d`；参数量、感受野 | `torch_conv_from_numpy`, `conv_param_count`, `receptive_field` |
| 3 | 搭建 CNN，逐层检查 shape，梯度检查 | `SimpleCNN.__init__`, `SimpleCNN.forward` |
| 4 | 数据加载、训练、验证、保存、测试；先过拟合 32 张图 | `make_dataloaders`, `train_one_epoch`, `evaluate`, `save_checkpoint`, `load_checkpoint`, `fit` |
| 5 | 第一层 feature maps、分类错误的图片、混淆矩阵 | `get_first_layer_feature_maps`, `get_misclassified` |
| 6 | NumPy 与 PyTorch 速度对比，进阶研究清单 | 无 |

覆盖的概念：局部连接、参数共享、输入输出通道、stride、padding、感受野、池化、logits 与 CrossEntropyLoss、train / eval 模式、验证集与测试集的分工。

已提供的观察图：卷积窗口逐步滑动、池化演示、局部连接与全连接的参数量对比、每层输出 shape 表、过拟合 32 张图的 loss、训练 / 验证曲线、第一层卷积核与 feature maps、分类错误图片、混淆矩阵。

[返回 Deep learning](../README.md)
