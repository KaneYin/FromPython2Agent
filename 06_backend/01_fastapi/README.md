# FastAPI Learning Lab

A four-week path combining browser exercises, a real local server, and targeted official documentation. Implement the exercises in [lab/](lab/README.md). The application bootstraps contain no prediction endpoints or completed exercise solutions.

## Start here

1. Read the [roadmap](ROADMAP.md).
2. Set up the [local lab](lab/README.md) with Python 3.12.
3. Follow [Week 1: API contracts](weeks/01_api_contracts.md), then continue in order.
4. Use the [official reference index](docs/OFFICIAL_REFERENCES.md) whenever a concept is unclear.

## Learning materials

| Material | Location | Role |
| --- | --- | --- |
| FastAPI Interactive | [Browser lessons](https://www.fastapiinteractive.com/) | Third-party practice environment; lesson links appear in each weekly guide |
| Cheuk Ting Ho's ML workshop | [Local source](../../90_resources/courses/fastapi/ml_fastapi/README.md) / [GitHub](https://github.com/Cheukting/ml_fastapi) | Original instructions, examples, penguin data, MNIST samples, Dockerfile, and MIT license |
| FastAPI documentation | [Official tutorial](https://fastapi.tiangolo.com/tutorial/) | Authoritative explanation of framework behavior |
| Local lab | [Setup and commands](lab/README.md) | Your own implementations and tests, separate from the imported source |

The workshop was cloned and imported at commit `580960359997ba830d9af18d7ff8555f2d270ae0`. Its 26 source files are unchanged. [Provenance and checksums](../../90_resources/courses/fastapi/UPSTREAM.json) make the snapshot reproducible. Nested Git metadata is excluded so the parent repository can track the actual source and data.

## Original work and added practice

Weekly guides label the workshop's exact part and exercise numbers. The JSON `POST /predict`, response contract, dependency-injection adaptation, fake-model tests, startup call-count test, corrupt-image handling, container recreation check, and cross-user update test are local extensions of the supplied roadmap.

The workshop's MNIST `POST /predict/` is an original upload exercise. It is different from the added JSON `POST /predict` for penguins. See [course clarifications](docs/COURSE_NOTES.md) for differences in paths, response names, lifecycle, persistence, and Docker behavior.

Week 4 stays in the browser lab. Save your own exported files in [lab/blog/](lab/blog/README.md) if you want a local record; the third-party browser application's source is not copied here.

## Repository map

```text
06_backend/01_fastapi/
├── README.md
├── ROADMAP.md
├── weeks/
│   ├── 01_api_contracts.md
│   ├── 02_dependencies_and_testing.md
│   ├── 03_images_and_docker.md
│   └── 04_blog_authorization.md
├── docs/
│   ├── OFFICIAL_REFERENCES.md
│   └── COURSE_NOTES.md
└── lab/
    ├── pyproject.toml
    ├── uv.lock
    ├── penguins/main.py
    ├── mnist/main.py
    ├── blog/README.md
    ├── models/README.md
    └── tests/README.md

90_resources/courses/fastapi/
├── README.md
├── UPSTREAM.json
└── ml_fastapi/             # Unmodified upstream source snapshot
```

Source and lesson links were checked on 2026-11-07. Browser exercise completion, ML training, and Docker acceptance checks are learner tasks, not completed outcomes of this repository setup.
