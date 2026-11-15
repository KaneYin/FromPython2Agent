# 01 - Two-Layer Neural Network (NumPy from scratch)

[中文说明](README_zh.md)

Build a `2 → 5 → 1` two-layer neural network by hand with NumPy only, and use it for binary classification on the Two Moons dataset. The exercise covers Forward Propagation, Binary Cross-Entropy, Backpropagation, Numerical Gradient Checking, and Batch Gradient Descent.

## Status

Exercise version. The 14 core functions keep their signatures, docstrings, and TODOs; the bodies are left for you to write. Formulas, an API quick reference, self-check cells, and all plotting code are provided. No reference solution is included.

| Notebook | Language |
| --- | --- |
| `two_moons_two_layer_nn_zh.ipynb` | Chinese |
| `two_moons_two_layer_nn_en.ipynb` | English |

The two notebooks match cell for cell, with the same code, self-checks, and expected values.

## Setup and running

From this directory:

```bash
uv sync
```

Then open `two_moons_two_layer_nn_en.ipynb` (or `two_moons_two_layer_nn_zh.ipynb`) in VS Code / Jupyter, pick `.venv/bin/python` as the kernel, and run from top to bottom. After implementing a function, run the self-check cell right after it.

Dependencies: NumPy (the model), scikit-learn (only for `make_moons` and `train_test_split`), Matplotlib (plots), ipykernel.

## Contents

| Lab | Topic | Functions to implement |
| --- | --- | --- |
| 1 | Dataset preparation | `standardize_features` |
| 2 | Parameter initialization (He) | `initialize_parameters` |
| 3 | Forward Propagation | `relu`, `relu_derivative`, `sigmoid`, `forward` |
| 4 | Loss and Backpropagation | `compute_loss`, `backward`, `gradient_check` |
| 5 | Training loop | `update_parameters`, `train` |
| 6 | Evaluation and visualization | `predict_proba`, `predict`, `accuracy` |
| 7 | Learning-rate / hidden-width experiments | None |

Plots provided for observation: data scatter plots, He initialization distribution, activation curves, gradient-check errors, loss curve, NN vs. Logistic Regression decision boundaries, per-neuron hidden activation maps, decision-boundary evolution during training, learning-rate comparison, and hidden-width comparison.

[Back to Deep learning](../README.md)
