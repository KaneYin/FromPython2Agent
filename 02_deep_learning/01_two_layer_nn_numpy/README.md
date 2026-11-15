# 01 - Two-Layer Neural Network (NumPy from scratch)

[中文说明](README_zh.md)

Build a `2 → 5 → 1` two-layer neural network by hand with NumPy only, and use it for binary classification on the Two Moons dataset. The exercise covers Forward Propagation, Binary Cross-Entropy, Backpropagation, Numerical Gradient Checking, and Batch Gradient Descent.

## Status

The 14 core functions keep their signatures, docstrings, and TODOs. Formulas, an API quick reference, self-check cells, and all plotting code are provided.

| Notebook | Language | Contents |
| --- | --- | --- |
| `two_moons_two_layer_nn_zh.ipynb` | Chinese | The author's in-progress solutions, with outputs |
| `two_moons_two_layer_nn_en.ipynb` | English | Blank exercise version |

The two notebooks match cell for cell, with the same self-checks and expected values. The Chinese solutions are a learner's own attempt, not a checked reference solution. To get a blank Chinese notebook, run this from the repository root:

```bash
git show 5f52464:02_deep_learning/01_two_layer_nn_numpy/two_moons_two_layer_nn_zh.ipynb > two_moons_two_layer_nn_zh_exercise.ipynb
```

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
