"""Learner entry point. Follow weeks/03_images_and_docker.md."""

from fastapi import FastAPI

app = FastAPI(title="MNIST Image Prediction Lab")

# TODO: Implement multipart POST /predict and documented image validation.
# TODO: Initialize a model in lifespan and explore BackgroundTasks.
# TODO: Save models and load an existing artifact before training a new one.
# TODO: Add a Dockerfile for this package and mount only the models directory.
# Import TensorFlow in the model-loading/training layer when it is needed.
