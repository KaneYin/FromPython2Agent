# Course Clarifications

These notes accompany the unmodified [workshop snapshot](../../../90_resources/courses/fastapi/ml_fastapi/README.md). They explain how its original examples map to this learning path.

| Potential ambiguity | Clarification and reference |
| --- | --- |
| Which lessons are official FastAPI material? | FastAPI Interactive is a third-party exercise site. Use [FastAPI's official tutorial](https://fastapi.tiangolo.com/tutorial/) to confirm framework behavior. |
| Why do browser lesson numbers differ from URL prefixes? | The homepage's display order and historical URL slugs differ. Follow the linked lesson titles; do not generate URLs from display numbers. |
| Is the penguin JSON POST part of the workshop? | No. Part 1 supplies a query-based GET. JSON POST and the shared response contract are added practice. See [Request Body](https://fastapi.tiangolo.com/tutorial/body/). |
| Why does upstream use `result` rather than `species`? | `result` is the original response key. This lab deliberately specifies `species` in a [response model](https://fastapi.tiangolo.com/tutorial/response-model/). |
| Why are some URLs `/predict/` and others `/predict`? | Upstream uses a trailing slash. This lab chooses `/predict` as canonical; exercise that path directly so redirect handling cannot hide a mismatch. |
| Is Part 2, Exercise 2 a penguin exercise? | It uses MNIST. Week 2 applies its [lifespan](https://fastapi.tiangolo.com/advanced/events/) idea to the earlier penguin model. |
| Will overriding Depends prevent startup training? | It only changes dependency resolution. A loader called directly by lifespan still runs; inject a fake loader for isolated route tests. See [overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) and [testing lifespan](https://fastapi.tiangolo.com/advanced/testing-events/). |
| Does one model load mean once for every process forever? | No. Check once per app lifespan. New contexts, workers, reloads, and restarts create additional lifespans. |
| Does a mounted directory automatically save the model? | No. Part 2, Exercise 4 adds file saving. Its following extra challenge covers discovery and reuse at startup. See [Keras serialization](https://keras.io/guides/serialization_and_saving/). |
| Does the upstream persistence example already reuse files on restart? | No. Its lifespan calls training unconditionally and its in-memory filename list starts empty. Implement the extra challenge before the container recreation check. |
| Does a container require a mounted volume to write files? | Containers have a writable layer. A missing target directory can prevent saving; a mount is needed here to retain artifacts after container removal. See [Docker storage](https://docs.docker.com/engine/storage/). |
| Why not mount the whole project as upstream does? | A source-tree bind mount can hide copied image files. The local exercise mounts only `/code/models`. See [bind-mount behavior](https://docs.docker.com/engine/storage/bind-mounts/). |
| Is BackgroundTasks a durable training queue? | No. It is in-process background work. The [official guide](https://fastapi.tiangolo.com/tutorial/background-tasks/) explains when heavier task systems are useful. |
| Does Get Current User enforce post ownership? | No. It supplies identity. Compare it with the stored author and test unauthorized updates before committing. See [Get Current User](https://fastapi.tiangolo.com/tutorial/security/get-current-user/). |
| Can I copy SQLModel code directly into the blog's async SQLAlchemy session? | Match the session type and execution model. The [FastAPI database tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/) and [SQLAlchemy AsyncIO guide](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) use different APIs. |

## Original workshop examples

| File | Original section |
| --- | --- |
| `example/main_1_1.py` | Part 1, Exercise 1: introductory routes |
| `example/main_1_2.py` | Part 1, Exercise 2: penguin prediction |
| `example/main_1_3.py` | Part 1, Exercise 3: positive numeric query inputs |
| `example/main_2_1.py` | Part 2, Exercise 1: MNIST background training |
| `example/main_2_2.py` | Part 2, Exercise 2: lifespan and image prediction |
| `example/main_2_3.py` | Part 2, Exercise 3: retraining with uploaded data; optional for this roadmap |
| `example/main_2_4.py` | Part 2, Exercise 4: saved-model artifacts; prerequisite for the added recreation check |
| `Dockerfile` | Part 3: container build/run starting point |

All paths in this table are relative to [ml_fastapi/](../../../90_resources/courses/fastapi/ml_fastapi/). Its top-level `main.py` is intentionally an empty learner entry point. The `example/` files are worked references and can trigger training or dataset downloads when imported; do not use them as test fixtures without inspecting them first.
