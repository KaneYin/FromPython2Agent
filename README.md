# FromPython2Agent

A personal learning workspace progressing from Python fundamentals to machine learning, deep learning, LLMs, retrieval, and agents. The two-digit folder prefixes define the learning order. Each runnable project keeps its own environment.

## Learning path

| Order | Folder | Contents and status |
| --- | --- | --- |
| 00 | [Python basics](00_python_basics/README.md) | Fourteen ordered notes and a partially completed strings exercise |
| 01 | [Machine learning](01_machine_learning/README.md) | Reserved for future implementations; no implementation added yet |
| 02 | [Deep learning](02_deep_learning/README.md) | Reserved for future implementations; no implementation added yet |
| 03 | [LLMs](03_llm/README.md) | Minimal chat examples, model-interface drafts, and a transformer study notebook |
| 04 | [RAG](04_rag/README.md) | A basic Ollama retrieval and generation demo |
| 05 | [Agents](05_agents/README.md) | A tool-calling agent-loop draft |

```text
FromPython2Agent/
├── 00_python_basics/
│   ├── 01_comments.md ... 14_collections.md
│   └── exercises/01_strings.py
├── 01_machine_learning/                  # Future implementations
├── 02_deep_learning/                     # Future implementations
├── 03_llm/
│   ├── 01_minimal_chat/
│   └── 02_transformer_from_scratch/
├── 04_rag/
│   └── 01_basic_rag/
├── 05_agents/
│   └── 01_agent_loop/
├── 90_resources/
│   ├── courses/cmu/
│   │   ├── 11_763_llm_inference/
│   │   ├── 11_768_ai_agents/
│   │   └── 11_868_llm_systems/
│   └── agent_selfstudy/
├── docs/
├── INDEX.md
└── README.md
```

`90_resources` holds course archives, papers, reading notes, and imported reference implementations that support multiple stages. Its prefix keeps that collection after the main learning path.

## Existing implementations

These implementation statuses come from the 2026-10-23 review. The 2026-10-26 organization changed paths and navigation; it did not rerun the demos or complete unfinished work.

| Project | Entry point | Recorded state |
| --- | --- | --- |
| [Minimal chat](03_llm/01_minimal_chat/README.md) | `without_abstraction/main.py`; abstraction draft in `main.py` | Direct-provider example and unfinished abstraction with import/runtime blockers |
| [Transformer study](03_llm/02_transformer_from_scratch/README.md) | `01_transformer_from_scratch.ipynb` | Tokenization/generation exploration; implementation section unfinished |
| [Basic RAG](04_rag/01_basic_rag/README.md) | `main.py` with `cat-facts.txt` | Flow previously checked with mocked Ollama; live models not tested |
| [Agent loop](05_agents/01_agent_loop/README.md) | `main.py` | Draft with a syntax error and canned tool results |

## Adding material

Use lowercase `snake_case` names and two-digit prefixes for lessons or independent projects, for example `01_linear_regression/` inside `01_machine_learning/`. Put new work in its topic stage, give it a README, and add it to that stage's index. Keep each runnable project's dependency files with that project. Imported projects retain their internal layout.

The stage numbers are stable categories; project numbers restart inside each stage. See the [repository guide](docs/REPOSITORY_GUIDE.md) for naming rules, the old-to-new path map, and environment details.

## Navigation and setup

- [Resource index](INDEX.md): topic links to existing courses, papers, notes, and reference implementations.
- [Resource collection](90_resources/README.md): course archives and self-study material.
- [Repository guide](docs/REPOSITORY_GUIDE.md): layout, naming, path migration, and project boundaries.
- [Code review and organization log](docs/CODE_REVIEW.md): historical findings and verification records.

There is no root install command. Follow the chosen project's README and run setup from that directory. The four personal model projects retain their Python 3.13 declarations and separate lockfiles. Existing `.venv` directories moved with their projects; console scripts may still contain old absolute paths and may require environment recreation.

Local credentials, environments, caches, PDFs, and some datasets/weights are ignored by Git. The local resource archive therefore contains files that a fresh clone will not supply. The RAG text dataset remains beside its script. The coursework `chess_app` retains its own Git checkout and source-verification requirements.
