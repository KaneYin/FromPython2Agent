# Four-Week Roadmap

For each week, complete the browser lessons, implement the local or browser lab, and record evidence for the acceptance checks. All checkboxes start unchecked.

| Week | Browser practice | Implementation | Acceptance |
| --- | --- | --- | --- |
| [1 - API contracts](weeks/01_api_contracts.md) | Body - Fields; Response Model - Return Type; Handling Errors | Workshop Part 1, Exercises 2-3. Build penguin `GET /predict`, then add JSON `POST /predict`, bounds, and a response model. | Valid requests return 200 with `species`; missing, out-of-range, and non-numeric inputs return 422. Both routes use one inference function. |
| [2 - Dependencies and testing](weeks/02_dependencies_and_testing.md) | Dependencies - First Steps; Testing; Async Dependencies & Lifespan | Adapt Workshop Part 2, Exercise 2's MNIST lifespan pattern to penguins. Supply the model with `Depends`; test routes with a fake model and test startup separately. | Route tests do not train a real model. Two requests within one `TestClient` context cause one model-load call. |
| [3 - Image inference and Docker](weeks/03_images_and_docker.md) | Request Files; Background Tasks | Workshop Part 2, Exercises 1-2, then Part 3, Exercises 1-2. Add the persistence prerequisite from Part 2, Exercise 4 and its restart challenge before the recreation check. | A valid image produces a digit prediction; corrupt bytes return a defined 4xx. Remove and recreate the container with the same model-directory mount; reuse the saved model. |
| [4 - Backend specialization](weeks/04_blog_authorization.md) | Blog track: Data Models Deep Dive; Database Connection; Authorization Levels; Error Handling Pro. Complete authentication prerequisites as needed. | Connect post models, a database session, and author permissions inside the browser lab. Add a cross-user modification test. | An author can edit their post. A different authenticated user is rejected, and a fresh database read confirms the post is unchanged. |

## Progress

| Week | Browser lessons | Implementation | Acceptance evidence |
| --- | --- | --- | --- |
| 1 | [ ] | [ ] | [ ] |
| 2 | [ ] | [ ] | [ ] |
| 3 | [ ] | [ ] | [ ] |
| 4 | [ ] | [ ] | [ ] |

The original workshop remains [here](../../90_resources/courses/fastapi/ml_fastapi/README.md). Added practice is identified explicitly in each guide; it is not presented as an original workshop requirement.
