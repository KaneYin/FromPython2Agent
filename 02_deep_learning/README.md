# 02 - Deep learning

Neural-network foundations and implementations. Transformer-specific work belongs in `03_llm/`.

| Project | Entry point | Status |
| --- | --- | --- |
| [02 - CNN on MNIST (NumPy conv → PyTorch)](02_cnn_mnist_pytorch/README.md) | `cnn_mnist_zh.ipynb` | Exercise version with TODOs (17 functions); includes NumPy conv2d/maxpool, PyTorch CNN, training pipeline, feature maps and error analysis |
| [03 - RNN: remember the first signal](03_rnn_memory_pytorch/README.md) | `rnn_memory_zh.ipynb` | Exercise version with TODOs (7 functions); hand-written RNN, BPTT, gradient clipping, T = 10 / 30 / 100 |
| [04 - LSTM: same memory task](04_lstm_memory_pytorch/README.md) | `lstm_memory_zh.ipynb` | Exercise version with TODOs (5 functions); hand-written LSTM checked against `nn.LSTMCell`, gate/cell-state observation |

The two-layer NumPy network (`01_two_layer_nn_numpy`) lives on the `exercise/two-layer-nn-zh` and `exercise/two-layer-nn-en` branches. Possible next additions include automatic differentiation, deeper networks, GRU, and optimizers such as Momentum and Adam. Add them as independently numbered projects with a local README and any required environment files.

[Previous: Machine learning](../01_machine_learning/README.md) | [Next: LLMs](../03_llm/README.md) | [Repository home](../README.md)
