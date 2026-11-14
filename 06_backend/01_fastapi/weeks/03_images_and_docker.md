# Week 3 - Image Inference and Docker

[Previous week](02_dependencies_and_testing.md) | [Roadmap](../ROADMAP.md) | [Next week](04_blog_authorization.md)

## Practice in the browser

- [Request Files](https://www.fastapiinteractive.com/fastapi-basics/15-request-files)
- [Background Tasks](https://www.fastapiinteractive.com/fastapi-basics/35-background-tasks)

## Original workshop

Work through these sections in order:

| Section | Local source | Purpose |
| --- | --- | --- |
| Part 2, Exercise 1: background task | [Instructions](../../../90_resources/courses/fastapi/ml_fastapi/README.md#exercise-1-background-task), [example](../../../90_resources/courses/fastapi/ml_fastapi/example/main_2_1.py) | Trigger MNIST training and inspect training state |
| Part 2, Exercise 2: lifespan events | [Instructions](../../../90_resources/courses/fastapi/ml_fastapi/README.md#exercise-2-lifespan-events), [example](../../../90_resources/courses/fastapi/ml_fastapi/example/main_2_2.py) | Initialize before serving and add image prediction |
| Part 3, Exercise 1: Creating images and running containers | [Instructions](../../../90_resources/courses/fastapi/ml_fastapi/README.md#exercise-1-creating-images-and-running-containers), [Dockerfile](../../../90_resources/courses/fastapi/ml_fastapi/Dockerfile) | Package and run the server |
| Part 3, Exercise 2: Mounting volumes | [Instructions](../../../90_resources/courses/fastapi/ml_fastapi/README.md#exercise-2-mounting-volumes) | Retain model artifacts outside a container |

Work in [lab/mnist/main.py](../lab/mnist/main.py). This is a separate application from the penguin API, so both may use `/predict` without mixing JSON and multipart contracts.

## Added practice - validate image input

Use a multipart `POST /predict` with field name `file`, not the Week 1 JSON body. See [Request Files](https://fastapi.tiangolo.com/tutorial/request-files/), including the `python-multipart` dependency. The lab's `fastapi[standard]` dependency includes form-upload support.

For this lab, define corrupt-image input as 400 with a JSON `detail` message. Missing the required upload field still produces FastAPI's 422. An uploaded filename or MIME type is not proof that its bytes decode as an image. Catch expected decoding errors such as Pillow's `UnidentifiedImageError` and raise [HTTPException](https://fastapi.tiangolo.com/tutorial/handling-errors/); avoid a catch-all handler that hides model failures. See [Pillow Image.open](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.open).

Use the ten [test images](../../../90_resources/courses/fastapi/ml_fastapi/data/test_image/) first. Define how you handle dimensions: either reject non-28-by-28 input with a documented 4xx or explicitly resize it. The workshop's preprocessing produces a normalized grayscale array with shape `(1, 28, 28, 1)`; preserve the training/inference convention. See the [official Keras MNIST example](https://keras.io/examples/vision/mnist_convnet/).

Run from `lab/`, then try:

```sh
curl -i -X POST 'http://127.0.0.1:8000/predict' \
  -F 'file=@../../../90_resources/courses/fastapi/ml_fastapi/data/test_image/test_img0.png'

curl -i -X POST 'http://127.0.0.1:8000/predict' \
  -F 'file=@pyproject.toml;type=image/png;filename=broken.png'
```

## Persistence prerequisite for the recreation check

Part 2, Exercises 1-2 keep models in memory. A model-directory mount alone does not persist those objects. Before attempting the added restart check, study [Part 2, Exercise 4: avoid race condition](../../../90_resources/courses/fastapi/ml_fastapi/README.md#exercise-4-avoid-race-condition), [main_2_4.py](../../../90_resources/courses/fastapi/ml_fastapi/example/main_2_4.py), and the extra challenge immediately after that exercise.

Implement these learner steps:

1. Save a completed model in `lab/models/` using Keras' `.keras` format.
2. At startup, discover valid saved artifacts in that directory and select one by a documented deterministic rule.
3. Load an existing model when present; train only when no usable model exists. The upstream example itself always trains on startup, so simply copying it does not satisfy the restart check.
4. Record the selected artifact and whether startup loaded or trained. Preserve a known artifact's checksum and modification time as acceptance evidence.

See [Keras saving and loading](https://keras.io/guides/serialization_and_saving/). Saving files is not by itself a complete concurrent-training coordination strategy; concurrent writes and model selection need their own design if you pursue the optional retraining exercises.

## Build a local Docker image

Install the lab's `mnist` extra locally if you want to run training outside Docker. For the image, create `lab/Dockerfile` based on the original workshop Dockerfile and the [official FastAPI Docker guide](https://fastapi.tiangolo.com/deployment/docker/).

Your Dockerfile must copy the MNIST package and dependency manifest, install the `mnist` extra, set its working directory to `/code`, create `/code/models`, and start the server on port 8000 at `0.0.0.0`. Use an exec-form command so lifespan receives shutdown signals. See the [Dockerfile reference](https://docs.docker.com/reference/dockerfile/).

The upstream Dockerfile copies only `main.py` and binds port 80. Adapt it to this lab's package layout. No completed Dockerfile is supplied for this exercise.

After implementing it, run these commands from `lab/`:

```sh
docker build -t fastapi-mnist-lab .

docker run -d --name fastapi-mnist-lab -p 8000:8000 \
  --mount "type=bind,source=$(pwd)/models,target=/code/models" \
  fastapi-mnist-lab

docker logs fastapi-mnist-lab
```

The host `models/` directory already exists in the scaffold. Mount just that directory, rather than the whole source tree. A [bind mount](https://docs.docker.com/engine/storage/bind-mounts/) retains files on the host and hides files already present at the same image path. A container can write to its writable layer without a mount; persistence after container removal is the reason for this exercise's mount.

## Added practice - remove and recreate the container

Wait until startup completes. Upload a valid image, record the selected model artifact, and run `shasum -a 256 models/<artifact>.keras` with your actual filename. Then:

```sh
docker stop fastapi-mnist-lab
docker rm fastapi-mnist-lab

docker run -d --name fastapi-mnist-lab -p 8000:8000 \
  --mount "type=bind,source=$(pwd)/models,target=/code/models" \
  fastapi-mnist-lab

docker logs fastapi-mnist-lab
```

Repeat the upload and artifact check. This procedure removes the exercise container and leaves the host model directory in place. Do not delete the model directory between runs.

## Acceptance checks

- [ ] Valid sample image returns 200 with a digit prediction in the documented response schema.
- [ ] A fake image containing text returns 400 with `detail`; a missing upload returns 422.
- [ ] Non-28-by-28 images follow the documented resize or rejection policy.
- [ ] Startup makes the initial model available before prediction requests are served.
- [ ] After container recreation, logs show that an existing artifact was loaded, without a new training run.
- [ ] The selected artifact's checksum and modification time remain unchanged; prediction still succeeds.

[BackgroundTasks](https://fastapi.tiangolo.com/tutorial/background-tasks/) is useful for exploring response timing. Heavy model training may warrant a separate task worker; calling a synchronous trainer inside `async def` does not make it non-blocking. This distinction is explained in the official guide's caveat and [FastAPI's async guide](https://fastapi.tiangolo.com/async/).
