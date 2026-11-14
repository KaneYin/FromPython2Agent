# Week 2 - Dependencies and Testing

[Previous week](01_api_contracts.md) | [Roadmap](../ROADMAP.md) | [Next week](03_images_and_docker.md)

## Practice in the browser

- [Dependencies - First Steps](https://www.fastapiinteractive.com/fastapi-basics/21-dependencies-first-steps)
- [Testing](https://www.fastapiinteractive.com/fastapi-basics/38-testing)
- [Async Dependencies & Lifespan](https://www.fastapiinteractive.com/fastapi-advanced-patterns/02-async-dependencies)

## Original workshop and adaptation

Read [Part 2, Exercise 2: lifespan events](../../../90_resources/courses/fastapi/ml_fastapi/README.md#exercise-2-lifespan-events). Its example initializes an MNIST model. This week's exercise adapts that lifecycle pattern to your Week 1 penguin model; the workshop does not supply the dependency-injection or fake-model tests described below.

## Added practice - control model creation

1. Introduce an application factory with an injectable model loader, for example `create_app(model_loader=...)`. Importing the module must not train a model or read the dataset.
2. In a [lifespan context manager](https://fastapi.tiangolo.com/advanced/events/), create the model before `yield`, keep it in application state, and release its resources after `yield`.
3. Add a model-provider dependency that reads the initialized model from the current request's application. Inject it into both routes with [Depends](https://fastapi.tiangolo.com/tutorial/dependencies/).
4. Keep request validation, HTTP handling, and the shared inference function separate. The fake should implement only the interface that inference actually uses.

The loader should supply everything inference needs, including label decoding if your model predicts encoded class IDs. A fake estimator alone is insufficient if inference still depends on a real global label encoder.

## Two distinct test layers

| Layer | Resource setup | Assertions |
| --- | --- | --- |
| Route tests | Supply a cheap fake loader to the application factory; override the model-provider dependency with a deterministic fake. | Validation, response shape, and shared route behavior; no real training or dataset access. |
| Startup test | Exercise the real lifespan implementation with a spy loader returning a fake model. Do not replace the lifespan itself. | Loader called once on entering the client context; two requests succeed; loader still called once; cleanup occurs after leaving the context. |

[Dependency overrides](https://fastapi.tiangolo.com/advanced/testing-dependencies/) replace dependencies resolved for a request. They do not replace code executed directly by lifespan. If route tests run the real training loader during startup, overriding the route dependency alone has not isolated the test. Supply the fake loader too, or use a deliberately separate startup-free app fixture for route tests.

Use a [TestClient context manager](https://fastapi.tiangolo.com/advanced/testing-events/) to run lifespan. Two requests must occur inside the same `with TestClient(app) as client:` block. Two separate client contexts represent two startups and may correctly call the loader twice. The requirement is once per application lifespan, not once globally across workers or restarts.

Reset `app.dependency_overrides` after each test, including failures, using fixture teardown or `try/finally`. See the [testing tutorial](https://fastapi.tiangolo.com/tutorial/testing/) for normal request assertions.

## Acceptance checks

- [ ] Import the app while real training and data access are configured to fail if called; importing still succeeds.
- [ ] Route tests return the fake's known species through both GET and POST.
- [ ] Week 1 validation cases still return 422 without invoking inference.
- [ ] Enter one `TestClient` context, send two valid requests, and assert loader call count is exactly one.
- [ ] Verify cleanup after leaving the client context.
- [ ] Verify dependency overrides do not leak into later tests.

Suggested learner files: `lab/penguins/models.py`, `lab/penguins/dependencies.py`, `lab/tests/test_penguin_routes.py`, and `lab/tests/test_penguin_lifespan.py`. Implement these as the week progresses; they are not pre-completed.
