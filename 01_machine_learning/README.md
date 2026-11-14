# 01 - Machine learning

Classical supervised learning, implemented step by step in NumPy and checked against scikit-learn. The labs follow course 1 (Supervised Machine Learning), weeks 1–3, of the [Machine Learning Specialization](https://www.coursera.org/specializations/machine-learning-introduction). Each week folder has its own `pyproject.toml` and `uv.lock`; run `uv sync` inside the folder you want to use.

## Supervised learning labs

| Week | Topics | Notebooks |
| --- | --- | --- |
| [C1 W1](01_supervised_learning/C1_W1/README.md) | Cost function, gradient descent for one-variable linear regression | `C1_W1_Lab03_Cost_function_Soln`, `C1_W1_Lab04_Gradient_Descent_Soln`, `Cost_function_intuitive` |
| [C1 W2](01_supervised_learning/C1_W2/) | Multiple linear regression, feature scaling and learning rate, feature engineering and polynomial regression, scikit-learn gradient descent | `C1_W2_Lab02`–`Lab05`, `C1_W2_Linear_Regression` |
| [C1 W3](01_supervised_learning/C1_W3/) | Classification, sigmoid, decision boundary, logistic loss and cost, gradient descent, scikit-learn, overfitting, regularization | `C1_W3_Lab01`–`Lab09`, `C1_W3_Logistic_Regression`, `01_student_pass_logistic_regression_exercises` |

A TODO version of the logistic regression exercise, with API references and self-checks, lives on the [`exercise/logistic-regression-todo`](https://github.com/KaneYin/FromPython2Agent/tree/exercise/logistic-regression-todo) branch.

## Other projects

| Project | Contents |
| --- | --- |
| [VGG from scratch](VGG/README.md) | A VGG-style convolutional network built in PyTorch (`VGG_from_scrach.ipynb`, `main.py`) |

## Next

Possible additions include clustering, decision trees and model-evaluation exercises. Add them as independently numbered projects, such as `02_unsupervised_learning/`, with a local README and their own environment files.

[Previous: Python basics](../00_python_basics/README.md) | [Next: Deep learning](../02_deep_learning/README.md) | [Repository home](../README.md)
