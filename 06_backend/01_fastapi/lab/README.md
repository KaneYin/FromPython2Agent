# Local Lab

Implement Weeks 1-3 here. Week 4 uses the browser lab; [blog/](blog/README.md) is available for your own exports and evidence.

## Environment

Run all commands in this directory, not at the repository root:

```sh
cd 06_backend/01_fastapi/lab
uv python install 3.12
uv sync --locked
```

The default environment includes the workshop's pinned FastAPI, pandas, and scikit-learn versions, plus pytest and HTTPX for testing. TensorFlow and Pillow are optional until Week 3:

```sh
uv sync --locked --extra mnist
```

The original workshop recommends Python 3.12 and pins TensorFlow 2.17.0. This lab uses Python 3.12 to match that baseline instead of the browser runtime's Python 3.13. The `mnist` extra requires a platform supported by that TensorFlow release. See [uv Python setup](https://docs.astral.sh/uv/guides/install-python/) and [TensorFlow pip installation](https://www.tensorflow.org/install/pip).

## Run the application bootstraps

For Weeks 1-2:

```sh
uv run fastapi dev penguins/main.py
```

For Week 3, stop the first server and run:

```sh
uv run --extra mnist fastapi dev mnist/main.py
```

Open `http://127.0.0.1:8000/docs`. Initially the applications have no business routes. Add prediction, validation, lifecycle, and dependency code as you complete the weekly guides. Importing these starter modules does not train models.

## Data and model paths

The original data stays in the [source snapshot](../../../90_resources/courses/fastapi/ml_fastapi/data/). There is no need to download it again for penguin inference or image-upload tests.

| Data | Path from this directory |
| --- | --- |
| Penguin table | `../../../90_resources/courses/fastapi/ml_fastapi/data/penguins.csv` |
| Ten MNIST test images | `../../../90_resources/courses/fastapi/ml_fastapi/data/test_image/` |
| Optional retraining archive | `../../../90_resources/courses/fastapi/ml_fastapi/data/train_img.zip` |
| Generated local models | `models/` |

Resolve data paths relative to a known project/source location in your code rather than depending on whichever directory launches pytest. For example, this lab root is `Path(__file__).resolve().parents[1]` inside `penguins/main.py`, and the parent repository is three parents above that lab root. See [pathlib](https://docs.python.org/3/library/pathlib.html).

Keras' original training function downloads the main MNIST dataset separately through `keras.datasets.mnist.load_data()` on first use. The small bundled test images and retraining archive are not a replacement for that full dataset.

## Tests

Follow the [test plan](tests/README.md). After writing your tests:

```sh
uv run pytest tests -q
```

There are no completed prediction tests or skipped placeholder tests in the starter. An initial pytest run may report that no tests were collected. Week 2's route and lifespan tests should run without TensorFlow or real model training.

## Working with the original examples

Read the upstream files as references and implement your work here. If you want to execute the original examples unchanged, copy the entire [upstream snapshot](../../../90_resources/courses/fastapi/ml_fastapi/) to a separate scratch directory, use its own `requirements.txt`, and run from that copy's root so its `data/` paths resolve. Its root `main.py` is a placeholder; select an example before using its original launch command.

The local bootstrap's package structure differs from upstream's single-file Docker layout. Follow [Week 3](../weeks/03_images_and_docker.md) when writing your Dockerfile, and keep generated `.keras` files in [models/](models/README.md).
