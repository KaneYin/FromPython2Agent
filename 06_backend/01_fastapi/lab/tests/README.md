# Learner Test Plan

Write the tests as part of the exercises. This directory intentionally contains guidance rather than completed solutions or tests that pass by skipping unfinished work.

| Suggested file | What it should establish |
| --- | --- |
| `test_penguin_contract.py` | Week 1's valid requests, shared predictions, required fields, bounds, non-numeric inputs, and response schema |
| `test_penguin_routes.py` | Week 2's dependency override supplies a known fake result to both routes without real training or dataset reads |
| `test_penguin_lifespan.py` | One loader call across two requests inside one client context; teardown releases the resource |
| `test_mnist_uploads.py` | Week 3's valid sample, corrupt file, missing field, and documented dimension policy |
| Browser lab test/export | Week 4's ordinary author success and authenticated non-author rejection, followed by a fresh database read |

Use [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/), [Dependency Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/), and [Testing Lifespan](https://fastapi.tiangolo.com/advanced/testing-events/).

Keep model accuracy or actual training separate from HTTP route tests. In Week 3, a fake can test upload validation cheaply; the Docker recreation acceptance still requires a real saved model and a real container run.

From `lab/`, after implementing tests:

```sh
uv run pytest tests -q
```
