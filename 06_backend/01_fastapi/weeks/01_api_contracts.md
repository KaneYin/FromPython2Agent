# Week 1 - API Contracts

[Roadmap](../ROADMAP.md) | [Next week](02_dependencies_and_testing.md)

## Practice in the browser

- [Body - Fields](https://www.fastapiinteractive.com/fastapi-basics/08-body-fields)
- [Response Model - Return Type](https://www.fastapiinteractive.com/fastapi-basics/11-response-model)
- [Handling Errors](https://www.fastapiinteractive.com/fastapi-basics/17-handling-errors)

If request bodies or query parameters are new, first complete [Request Body](https://www.fastapiinteractive.com/fastapi-basics/04-request-body) and [Query Parameters](https://www.fastapiinteractive.com/fastapi-basics/03-query-parameters).

## Original workshop

Read [Part 1, Exercise 2: prediction on demand](../../../90_resources/courses/fastapi/ml_fastapi/README.md#exercise-2-prediction-on-demand), then [Exercise 3: query parameters validation](../../../90_resources/courses/fastapi/ml_fastapi/README.md#exercise-3-query-parameters-validation).

Use [penguins.csv](../../../90_resources/courses/fastapi/ml_fastapi/data/penguins.csv). The model uses `bill_length_mm` and `flipper_length_mm`, in that order. The completed upstream references are [main_1_2.py](../../../90_resources/courses/fastapi/ml_fastapi/example/main_1_2.py) and [main_1_3.py](../../../90_resources/courses/fastapi/ml_fastapi/example/main_1_3.py); try the exercises before consulting them.

Work in [lab/penguins/main.py](../lab/penguins/main.py). Keep training and prediction in separate functions so Week 2 can move initialization without rewriting inference.

## Added practice - define one API contract

Use the following local contract consistently for both endpoints. The upper bounds are practice limits chosen for this lab, not biological guarantees or values required by the workshop.

| Item | Local contract |
| --- | --- |
| Canonical paths | `GET /predict` and `POST /predict`, without a trailing slash |
| `bill` | Required finite number in millimeters; `0 < bill <= 100` |
| `flipper` | Required finite number in millimeters; `0 < flipper <= 500` |
| GET input | Query parameters `bill` and `flipper` |
| POST input | JSON object with the same field names |
| Successful response | 200; response model with a `species` field containing `Adelie`, `Chinstrap`, or `Gentoo` |
| Validation failure | 422 for a missing field, a non-numeric value, or a value outside the declared bounds |
| Inference | One shared function used by both routes; no duplicated training or prediction pipeline |

Use `Query` for query constraints and Pydantic `Field` for body constraints. See [numeric validation](https://fastapi.tiangolo.com/tutorial/path-params-numeric-validations/), [Body - Fields](https://fastapi.tiangolo.com/tutorial/body-fields/), and [Pydantic numeric constraints](https://docs.pydantic.dev/latest/api/standard_library_types/#floats). Declare a [response model](https://fastapi.tiangolo.com/tutorial/response-model/) rather than relying only on an untyped dictionary.

Default validation may coerce numeric strings. Use a clearly invalid value such as `"not-a-number"` for the type-error check; rejecting JSON `"45.0"` is a separate strict-validation policy. Query values arrive as text, so JSON strictness and query parsing require different consideration. See [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/).

Do not convert request-validation errors into 200 responses. Use [HTTPException](https://fastapi.tiangolo.com/tutorial/handling-errors/) for application failures that require a chosen HTTP status.

## Requests to try after implementation

Run the server from [lab/](../lab/README.md), then use a second terminal:

```sh
curl -i 'http://127.0.0.1:8000/predict?bill=45&flipper=200'

curl -i -X POST 'http://127.0.0.1:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{"bill":45,"flipper":200}'

curl -i -X POST 'http://127.0.0.1:8000/predict' \
  -H 'Content-Type: application/json' \
  -d '{"bill":45}'
```

## Acceptance checks

| Case | Exercise both GET and POST | Expected |
| --- | --- | --- |
| Ordinary input | `bill=45`, `flipper=200` | 200; a valid `species`; equal predictions for equal inputs |
| Missing field | Omit each required field in turn | 422 |
| Invalid type | Replace each input with `not-a-number` | 422 |
| Lower bound | Try zero and a negative number for each input | 422 |
| Upper bound | Try `bill=100.1` or `flipper=500.1` | 422 |
| Included upper bound | Try `bill=100`, `flipper=500` | 200 |
| Non-finite number | Try query `NaN` or `Infinity`; reject it explicitly | 422 |
| Shared inference | Inspect the call path of both routes | Both delegate to the same inference function |

- [ ] Check `/docs` for required fields, numeric constraints, and response schema.
- [ ] Check `/predict` directly without following redirects; avoid passing a 307 redirect as a successful validation test.
- [ ] Save request/response evidence and the validation cases under [lab/tests/](../lab/tests/README.md).
