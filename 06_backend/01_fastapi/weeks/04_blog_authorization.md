# Week 4 - Blog Models, Sessions, and Authorization

[Previous week](03_images_and_docker.md) | [Roadmap](../ROADMAP.md)

## Practice and implement in the browser

Use [Build a Blog API with Authentication](https://www.fastapiinteractive.com/fastapi-blog-auth):

| Lesson | Focus |
| --- | --- |
| [01 - Data Models Deep Dive](https://www.fastapiinteractive.com/fastapi-blog-auth/01-data-models-deep-dive) | Input/output schemas and relationships |
| [02 - Database Connection](https://www.fastapiinteractive.com/fastapi-blog-auth/02-database-connection) | Database models, sessions, and persistence |
| [04 - Authorization Levels](https://www.fastapiinteractive.com/fastapi-blog-auth/04-authorization-levels) | Author identity and permission checks |
| [06 - Error Handling Pro](https://www.fastapiinteractive.com/fastapi-blog-auth/06-error-handling-pro) | Consistent failure responses |

If authentication is not already working, complete [03 - User Authentication](https://www.fastapiinteractive.com/fastapi-blog-auth/03-user-authentication). Useful Basics prerequisites are [Security - First Steps](https://www.fastapiinteractive.com/fastapi-basics/27-security-first-steps), [Get Current User](https://www.fastapiinteractive.com/fastapi-basics/28-get-current-user), and [OAuth2 with JWT Tokens](https://www.fastapiinteractive.com/fastapi-basics/30-oauth2-jwt-tokens).

These are browser-course lessons, not exercises from the ML workshop. Follow the actual route names, schema fields, and test tools provided by the browser lab. Do not invent a local clone of its private runtime or assume that all lessons share one persistent application.

## Connect the pieces

1. Identify the database post model, public response schema, and update schema. Ownership should come from the authenticated identity when creating a post, rather than from an editable client field.
2. Provide a database session through a dependency with a defined lifetime. Follow the [official SQL database tutorial](https://fastapi.tiangolo.com/tutorial/sql-databases/) and [dependencies with yield](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/).
3. Resolve the logged-in user through an authentication dependency. [Get Current User](https://fastapi.tiangolo.com/tutorial/security/get-current-user/) explains dependency composition; use [OAuth2 with JWT](https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/) for the complete token example when needed.
4. Load the stored post, compare its stored author ID with the authenticated user's ID, and reject an unauthorized modification before applying changes or committing a transaction.
5. Follow the course's rejection status. If its contract is unspecified, choose 403 for an authenticated non-author. If the course intentionally hides resource existence with 404, test and document that policy. Keep this distinct from authentication failures.

The current FastAPI SQL tutorial uses SQLModel, while the browser Database Connection lesson describes SQLAlchemy and async operations. Transfer the session-lifetime principle without mixing sync `Session` methods and `AsyncSession` methods. See [SQLAlchemy async sessions](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html).

## Added practice - cross-user modification test

Use a fresh database or isolated transaction for the test. Create two ordinary users, Alice and Bob, with author permissions and no administrator role.

| Step | Action | Required evidence |
| --- | --- | --- |
| Arrange | Alice creates a post through the authenticated API. | Saved post ID, Alice's author ID, original title/content |
| Author update | Authenticate as Alice and update that post. | Success response; a new database read shows the updated values |
| Snapshot | Capture the post's persisted fields after Alice's update. | Baseline for the forbidden-update assertion |
| Cross-user update | Authenticate as Bob; submit a different title/content for the same post. | Request reaches authorization and returns the documented rejection status |
| Verify persistence | Query the post again with a fresh database session. | Every persisted field matches the snapshot; Bob's changes were not committed |

Send a valid update payload in Bob's request. A 422 from an invalid body does not prove that author permissions are enforced. Similarly, an expired or missing token only checks authentication. Use a fresh read because an ORM identity-map cache can conceal what was actually committed.

Use [HTTPException and error handlers](https://fastapi.tiangolo.com/tutorial/handling-errors/) to align failures with the API contract. If the lab supports pytest, use its test harness; otherwise run the same sequence through its request client and inspect stored data. Save your exported code and evidence under [lab/blog/](../lab/blog/README.md).

## Acceptance checks

- [ ] Data models, database-session handling, and authenticated identity are connected in the browser lab.
- [ ] An ordinary author can modify their own post.
- [ ] Another authenticated ordinary user receives the expected rejection for a valid update request.
- [ ] A fresh database query confirms all persisted post fields remain unchanged after the rejected request.
- [ ] Any administrator bypass is tested separately and does not invalidate the ordinary-user test.
