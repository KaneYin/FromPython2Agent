# Official Reference Index

Use these references to resolve a specific implementation question. FastAPI Interactive and the ML workshop are third-party learning materials; the links below point to the projects' own documentation.

## Week 1 - Request and response contracts

| Question | Official documentation |
| --- | --- |
| How is a JSON body declared? | [FastAPI: Request Body](https://fastapi.tiangolo.com/tutorial/body/) |
| Where do numeric bounds and descriptions belong? | [FastAPI: Body - Fields](https://fastapi.tiangolo.com/tutorial/body-fields/), [numeric validations](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/) |
| How do query constraints work? | [FastAPI: Query Parameters and String Validations](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/) |
| How do finite numbers and coercion work? | [Pydantic: float constraints](https://docs.pydantic.dev/latest/api/standard_library_types/#floats), [strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) |
| How do I constrain the returned schema? | [FastAPI: Response Model - Return Type](https://fastapi.tiangolo.com/tutorial/response-model/) |
| What produces validation failures or explicit HTTP errors? | [FastAPI: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) |
| How is the penguin estimator assembled? | [scikit-learn: Pipeline](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html), [KNeighborsClassifier](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.KNeighborsClassifier.html), [LabelEncoder](https://scikit-learn.org/stable/modules/generated/sklearn.preprocessing.LabelEncoder.html) |

## Week 2 - Lifecycle and test isolation

| Question | Official documentation |
| --- | --- |
| When is an expensive model initialized and released? | [FastAPI: Lifespan Events](https://fastapi.tiangolo.com/advanced/events/) |
| How do routes obtain a shared resource? | [FastAPI: Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/) |
| Where can application-scoped state live? | [Starlette: Storing state on the app instance](https://starlette.dev/applications/#storing-state-on-the-app-instance) |
| How are route dependencies replaced in a test? | [FastAPI: Testing Dependencies with Overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) |
| How do I send test requests? | [FastAPI: Testing](https://fastapi.tiangolo.com/tutorial/testing/) |
| How do tests actually execute startup and shutdown? | [FastAPI: Testing Events](https://fastapi.tiangolo.com/advanced/testing-events/), [Starlette: TestClient](https://starlette.dev/testclient/) |
| How can a loader call count be observed? | [Python: unittest.mock](https://docs.python.org/3/library/unittest.mock.html) |

## Week 3 - Files, background work, and containers

| Question | Official documentation |
| --- | --- |
| How do multipart uploads and UploadFile work? | [FastAPI: Request Files](https://fastapi.tiangolo.com/tutorial/request-files/) |
| When does a background task run, and what are its limits? | [FastAPI: Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/), [async and concurrency](https://fastapi.tiangolo.com/async/) |
| How are images decoded? | [Pillow: Image.open](https://pillow.readthedocs.io/en/stable/reference/Image.html#PIL.Image.open) |
| What shape and normalization does MNIST use? | [Keras: Simple MNIST convnet](https://keras.io/examples/vision/mnist_convnet/) |
| How is a model saved and restored? | [Keras: Serialization and saving](https://keras.io/guides/serialization_and_saving/) |
| How do I build a FastAPI image? | [FastAPI: Docker](https://fastapi.tiangolo.com/deployment/docker/), [Dockerfile reference](https://docs.docker.com/reference/dockerfile/) |
| How does a model directory survive container removal? | [Docker: Bind mounts](https://docs.docker.com/engine/storage/bind-mounts/), [docker run](https://docs.docker.com/reference/cli/docker/container/run/) |

## Week 4 - Persistence and identity

| Question | Official documentation |
| --- | --- |
| How should database sessions be scoped? | [FastAPI: SQL Databases](https://fastapi.tiangolo.com/tutorial/sql-databases/), [dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/) |
| What changes for async SQLAlchemy sessions? | [SQLAlchemy: AsyncIO support](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) |
| How is an authenticated identity injected? | [FastAPI: Get Current User](https://fastapi.tiangolo.com/tutorial/security/get-current-user/) |
| Where is the complete bearer-token example? | [FastAPI: OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) |
| How do I return a permission failure? | [FastAPI: Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) |

Authentication establishes identity. The comparison between that identity and a post's stored author is application authorization logic that you must implement and test; a current-user dependency alone does not enforce ownership.

## Environment setup

- [uv: Working on projects](https://docs.astral.sh/uv/guides/projects/)
- [uv: Managing Python versions](https://docs.astral.sh/uv/guides/install-python/)
- [FastAPI: Development CLI](https://fastapi.tiangolo.com/fastapi-cli/)

The workshop pins its 2024 dependency versions and recommends Python 3.12. The lab retains those application pins for compatibility. Official documentation is live and may show newer APIs; check the installed version before copying a newer example.
