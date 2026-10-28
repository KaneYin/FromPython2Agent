# Repository guide

## Learning stages

The 2026-10-26 layout uses stable topic stages with a second level of ordering for lessons and implementations.

| Prefix | Stage | What belongs here |
| --- | --- | --- |
| `00` | [Python basics](../00_python_basics/README.md) | Language notes, standard-library practice, and small exercises |
| `01` | [Machine learning](../01_machine_learning/README.md) | Classical ML implementations and experiments; currently reserved |
| `02` | [Deep learning](../02_deep_learning/README.md) | Neural-network foundations and implementations; currently reserved |
| `03` | [LLMs](../03_llm/README.md) | Chat interfaces, tokenization, transformers, training, and inference implementations |
| `04` | [RAG](../04_rag/README.md) | Embeddings, retrieval, indexing, and retrieval-augmented generation projects |
| `05` | [Agents](../05_agents/README.md) | Tool loops, planning, memory, agent evaluation, and orchestration implementations |
| `90` | [Resources](../90_resources/README.md) | Course archives, papers, reading notes, and imported reference projects |

The sequence communicates a learning route. A small API demo can still be explored before completing every earlier stage. Existing code remains learning work with the limitations recorded in the [2026-10-23 review](CODE_REVIEW.md).

## Naming and future additions

1. Use two digits followed by a lowercase `snake_case` description: `01_linear_regression/`, `02_logistic_regression/`, or `03_tokenization/`.
2. Restart project numbering inside each stage. A stage number names the broad topic; a child number orders that topic's lessons or implementations.
3. Append new material with the next unused child number. Keep the current stage numbers stable; `06` through `89` remain available for future stages.
4. Keep related notes, data, entry points, and dependency files inside their project. Small Python exercises can remain in `00_python_basics/exercises/`.
5. Give each independent project a README with its purpose, current status, setup, and run location. Update its stage README; add useful concept/resource links to `INDEX.md`.
6. Preserve upstream package names, assignment layouts, filenames used by imports, attribution, and licenses inside imported projects. Course codes such as `11_768` identify courses rather than learning stages.

Python notes use `01` through `14` in their existing suggested learning order. The strings exercise is now `exercises/01_strings.py`. Their contents were preserved. Existing chat implementation module names were retained because they are implementation details and include unfinished import work.

## Path migration

| Previous path | Current path |
| --- | --- |
| `00_python_basics/` | Same stage; its notes now have ordered `01_` through `14_` filenames |
| `01_minimal_chat/` | `03_llm/01_minimal_chat/` |
| `01_minimal_chat/WithoutAbstraction/` | `03_llm/01_minimal_chat/without_abstraction/` |
| `0_LLM/01_TransofrmersFromScratch/` | `03_llm/02_transformer_from_scratch/` |
| `01_Transformer_From_Scratch.ipynb` in that project | `01_transformer_from_scratch.ipynb` in the renamed project |
| `03_RAG/DemoRAG/` | `04_rag/01_basic_rag/` |
| `Agent_loop/` | `05_agents/01_agent_loop/` |
| `cmu-11763-llm-inference/` | `90_resources/courses/cmu/11_763_llm_inference/` |
| `cmu-agents-11-768/` | `90_resources/courses/cmu/11_768_ai_agents/` |
| `OpenCourse/CMU/11868-LLM-Systems/` | `90_resources/courses/cmu/11_868_llm_systems/` |
| `agent-selfstudy/` | `90_resources/agent_selfstudy/` |
| `00_python_basics/exercises/python_string_demo.py` | `00_python_basics/exercises/01_strings.py` |

No compatibility symlinks were added. Reopen moved files and update any bookmarks or editor launch configurations outside this repository that refer to previous paths.

### Python note filenames

| Previous filename | Current filename |
| --- | --- |
| `Comments.md` | `01_comments.md` |
| `Python Variables.md` | `02_variables.md` |
| `字符串.md` | `03_strings.md` |
| `Python List.md` | `04_lists.md` |
| `Python Tuples.md` | `05_tuples.md` |
| `Python Dictionaries.md` | `06_dictionaries.md` |
| `比较运算符与判断语句.md` | `07_comparisons_and_conditionals.md` |
| `Loop in Python.md` | `08_loops.md` |
| `Function.md` | `09_functions.md` |
| `Python Classes.md` | `10_classes.md` |
| `Python typing Module.md` | `11_typing.md` |
| `several function in python.md` | `12_builtin_functions.md` |
| `Collection API.md` | `13_collection_api.md` |
| `collections.md` | `14_collections.md` |

## Environments and working directories

This repository is a collection of separate projects. There is no root dependency environment or root test suite. Keep each project's manifest and lockfile separate; organization does not require dependency resolution or lockfile regeneration.

| Project | Setup/run location | Notes |
| --- | --- | --- |
| Python exercise | Repository root: `python3 00_python_basics/exercises/01_strings.py` | Standard library; unfinished exercise behavior retained |
| Minimal chat | `03_llm/01_minimal_chat/` | See its [README](../03_llm/01_minimal_chat/README.md); the abstraction remains blocked |
| Transformer study | `03_llm/02_transformer_from_scratch/` | Separate notebook kernel and environment; existing outputs retained |
| Basic RAG | `04_rag/01_basic_rag/` | Launch here so `cat-facts.txt` resolves; requires its configured Ollama models |
| Agent loop | `05_agents/01_agent_loop/` | Syntax-blocked draft; dependencies alone do not complete it |

For example, the RAG project's locked setup remains:

```sh
cd 04_rag/01_basic_rag
uv sync --locked
```

Setup can download dependencies; running a demo can contact its model service. Neither was performed during this path reorganization.

Existing `.venv` directories were moved intact with their projects. Activation scripts and executable shebangs can embed the old absolute location. If an existing environment refers to the previous path, recreate that project's environment through its normal setup before using its console scripts, and reselect its notebook kernel. No environment files or installed dependencies were rewritten during organization.

## Coursework and imported references

| Location within `90_resources/` | Role |
| --- | --- |
| `courses/cmu/11_768_ai_agents/Homework/HW1/` | Personal coursework working copy with the nested `chess_app` Git checkout |
| `agent_selfstudy/code/assignment-1/` | Separate annotated reference copy; its `chess_app/` directory is empty |
| `agent_selfstudy/code/assignment-2/` | Assignment scaffold with its own instructions and environment |
| `agent_selfstudy/code/microagent/` | Reference implementation and local notes |
| `agent_selfstudy/code/deep-research/` | TypeScript reference project with a separate npm environment |
| `agent_selfstudy/code/smolagents-codeagent-demo/` | Reference demo with its own requirements |
| `courses/cmu/11_763_llm_inference/code/` | Imported examples and unfinished homework starters |
| `courses/cmu/11_868_llm_systems/repos/` | Imported LLM Systems assignments and examples |

The two HW1 copies contain different `src/assignment/agent/base.py` files. They remain separate. Imported layouts and relative paths within each collection were retained.

The coursework `chess_app` remains a real nested Git checkout. Its source verifier checks its commit and clean working tree against the task definition. Its Git metadata was preserved; the parent repository's ignore rule now targets its new location. A fresh clone of this parent repository does not supply that checkout/history; follow the assignment's source setup requirements separately.

## Version control and preservation

- Personal source, notes, notebooks, manifests, and lockfiles remain eligible for tracking.
- `.env` variants, keys, local tool state, environments, caches, and dependencies retain their ignore rules. Sanitized `.env.example` templates remain eligible.
- PDF/data/weight/output exclusions still apply. Archived resources on disk do not all appear in a fresh clone.
- Path-specific data exclusions now target `90_resources/courses/cmu/11_868_llm_systems/repos/`.
- `04_rag/01_basic_rag/cat-facts.txt` stays beside its script and remains eligible for tracking.
- Source code, notebook contents, unfinished implementations, dependency declarations, and lockfiles were preserved. Navigation documents and path-specific ignore entries were updated.
- Pre-existing staged content was retained. Moves are unstaged filesystem changes; nothing was staged or committed by this organization pass.
