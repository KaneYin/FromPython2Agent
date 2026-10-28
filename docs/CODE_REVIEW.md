# Code review and organization log

Review date: 2026-10-23. Findings describe the saved local files inspected in this pass, including existing uncommitted work.

Paths in this historical review were updated to the 2026-10-26 layout. Runtime findings and historical validation counts below were not rerun during that path reorganization. See the final section for the new organization record.

## Scope

Reviewed the nine personal Python files, four personal project manifests and lockfile root metadata, the transformer notebook's cells, repository structure, and navigation. Inventoried the imported collections and inspected their project documentation, representative assignment placeholders, both HW1 copies, and the coursework source-verification logic.

The broader check parsed 432 Python files outside environments, caches, dependencies, and `chess_app` directories. Imported reference code received a syntax/inventory check, not a complete behavioral or dependency audit. No external model requests, package installations, GPU runs, cloud sandboxes, or upstream updates were performed. No credential contents were inspected.

## Runtime blockers in unfinished personal code

These were recorded and deliberately left unchanged, as requested. They describe the present drafts, not regressions introduced by the organization work.

| Priority | Location | Finding and effect | Evidence |
| --- | --- | --- | --- |
| P1 | [Chat entry point](../03_llm/01_minimal_chat/main.py#L3) | Imports `model.base`, `model.litellm_model`, and `model.types`, but the repository has no `model/` package. Running the abstraction entry point stops before the chat loop. | Reproduced `ModuleNotFoundError: No module named 'model'` with the existing Python 3.13 environment. |
| P1 | [Message types](../03_llm/01_minimal_chat/dataclass.py#L1) | `from dataclass import dataclass` imports this same local module instead of the standard-library `dataclasses` module. The type definitions cannot load. | Direct local import reproduced `ImportError`. |
| P1 | [Chat protocol](../03_llm/01_minimal_chat/ChatModel.py#L6) and [LiteLLM adapter](../03_llm/01_minimal_chat/LiteLLMModel.py#L14) | `Message` and `ModelResponse` are referenced without imports; `Usage` is also absent from the adapter. Under the pinned Python 3.13, the first missing annotation name blocks class creation. The adapter later uses `choise` instead of `choice`. | Isolated definitions reproduced `NameError: Message`; supplying temporary probe-only types and a fake completion reproduced `NameError: choise`. No source was edited. |
| P1 | [LangChain adapter](../03_llm/01_minimal_chat/baseChatModel.py#L26) | `_generate()` stores a bound method as the message role, never calls Ollama or defines `response`, and uses `generation=` rather than `generations=` in `ChatResult`. | Calling `_generate()` with a real LangChain `HumanMessage` reproduced `NameError: response`. The installed `ChatResult` fields are `generations` and `llm_output`; the other defects were verified by inspection. |
| P1 | [Agent-loop draft](../05_agents/01_agent_loop/main.py#L80) | Explanatory prose at lines 81, 87, and 98 is not commented, so the file cannot parse. It also retains canned tool results, ignored arguments, and an unbounded loop. | Parsing stops at line 81 with `SyntaxError`; the remaining limitations are explicit in the source. |

## Behavior and portability findings

These remain unchanged too. The RAG happy path works with mocked model responses; the findings concern other execution conditions.

| Priority | Location | Finding and effect | Evidence |
| --- | --- | --- | --- |
| P2 | [Direct chat history](../03_llm/01_minimal_chat/without_abstraction/main.py#L33) | Only user messages are saved between calls. Assistant replies are printed but never appended, so follow-up questions do not include prior assistant answers. | A two-turn fake agent received roles `user,user` on the second call. |
| P2 | [RAG dataset loading](../04_rag/01_basic_rag/main.py#L5) | `cat-facts.txt` is opened relative to the process working directory. Launching the script from the repository root fails before indexing. | Root-directory launch via `runpy` reproduced `FileNotFoundError`. The project README now documents the required working directory. |
| P2 | [RAG import side effects](../04_rag/01_basic_rag/main.py#L21) | Module import immediately embeds all 150 rows. Importing a helper therefore requires model service access and repeats the indexing work. | Import-mode execution with fake Ollama recorded 150 embedding calls without invoking `main()`. |
| P2 | [Cosine similarity](../04_rag/01_basic_rag/main.py#L26) | Zero-norm vectors divide by zero. Different-length vectors are silently accepted by `zip()` and produce an invalid similarity comparison. | Reproduced `ZeroDivisionError`; `[1,0,1]` versus `[1,0]` returned approximately `0.7071` instead of rejecting incompatible dimensions. |

## Unfinished learning material preserved

| Area | Current state |
| --- | --- |
| Python strings | Exercise comments and implementations still differ in places: exercise 4 omits the expected `!`, and exercise 10 appends extra values to its formatted output. No exercise answers or comments were changed. |
| Transformer notebook | Tokenization, logits, softmax, and greedy generation cells are present. The later transformer/attention implementation section ends in an empty code cell. Existing outputs were preserved; the notebook was not executed. |
| Both AI Agents HW1 copies | Explicit TODOs and `NotImplementedError` remain in the agent loop, prompt construction, skills, and tools. Their `base.py` files differ, so they were not deduplicated. |
| Inference HW3 speculative decoding | [Starter `specdec.py`](../90_resources/courses/cmu/11_763_llm_inference/code/homework3/specdec/specdec.py#L65) has an empty greedy-decoding branch and fails parsing at line 68. This is an existing starter-code gap and was not filled. |
| Other imported projects | Their original exercises, environments, tests, attribution, and local notes remain intact. Syntax passing is not a completion or correctness claim. |

## Repository findings addressed

| Finding | Organization change | Reason |
| --- | --- | --- |
| No workspace README or clear project status | Added root navigation and this `docs/` folder. | Distinguishes personal learning code from course archives and imported projects without breaking paths. |
| Three empty personal project READMEs | Added status, file roles, prerequisites, and known blockers for minimal chat, agent loop, and transformer study. | Gives each project an honest entry point without completing its implementation. |
| RAG README lacked execution prerequisites | Appended local setup, exact model names, required working directory, and validation limits. | Explains how the existing script expects to run while preserving its conceptual notes. |
| Existing resource index omitted personal demos and LLM Systems from its overview | Expanded the overview and linked the new repository documentation. | Keeps the topic index useful without replacing its existing learning material. |
| `.env.bak` was eligible for Git additions | Ignore `.env.*`, with an exception for `.env.example`; add the same template exception to the imported deep-research project's overriding ignore rule. | Keeps local environment backups out of future additions while retaining setup templates. The existing backup was retained and its contents were not inspected. |
| Tool state depended on global ignores or remained eligible for additions | Added repository rules for `.claude/settings.local.json`, `.cmuxterm/`, and `node_modules/`. | Makes local-artifact handling portable to another checkout; files on disk were retained. |

Existing PDF/data/output exclusions were retained. No application, exercise, notebook, dependency manifest, lockfile, imported implementation, or nested checkout was changed. The pre-existing staged `.gitignore` remains staged at its original content; this pass's additional ignore edits are unstaged. Nothing was staged or committed.

## Validation

| Check | Result |
| --- | --- |
| Personal Python syntax | 8 of 9 files parse; `05_agents/01_agent_loop/main.py` is the known draft failure. |
| Broad Python syntax inventory | 430 of 432 files parse with Python 3.13 grammar. The other failure is the imported HW3 starter listed above. |
| Project metadata and notebooks | All 9 discovered `pyproject.toml` files parse as TOML; all 24 discovered notebooks parse as JSON. This does not execute their cells. |
| Personal lockfile metadata | The four personal project entries contain the dependency names declared in their manifests and the same Python requirement. No resolver or package installation was run. |
| Runtime blocker probes | Missing chat package, local dataclass import, missing annotation types, adapter response variable, and adapter typo reproduced with Python 3.13.5. Completion responses were mocked. |
| RAG happy path | Mocked full script run indexed 150 rows, embedded one query, sent retrieved context and the user query, and printed streamed chunks. Identical and orthogonal vector checks passed. |
| RAG and direct-chat edge cases | Working-directory failure, import-time indexing, cosine edge cases, and missing assistant history reproduced as listed above. |
| Coursework nested checkout | Existing `chess_app` HEAD matched task `base_commit` (`4aaabca1194ef5f175ccae4fecf902bc71cc303b`); its working tree was clean. |
| Organization checks | All 44 local documentation links resolve. Repository-only ignore checks confirm local artifacts are ignored and source/templates remain eligible. Edited documentation has no trailing whitespace; scoped `git diff --check` passes. The whole-worktree check reports only pre-existing whitespace in `baseChatModel.py`, which was left untouched. |

System Python 3.14.6 performed the initial broad syntax scan with the Python 3.13 grammar setting. A native Python 3.13.5 pass confirmed the same file counts and two existing syntax failures; that interpreter also ran the chat runtime probes. The imported `homework2/basic_deepresearch/mcp_agents/evaluation_utils/utils.py` emitted an existing invalid-escape `SyntaxWarning` for `\%`, without failing parsing. Real Ollama/OpenAI availability, model quality, notebook execution, assignment suites, and imported-project runtime behavior remain unverified.

## Implementation log

1. Recorded the original Git state and SHA-256 fingerprints of 1,799 existing regular files outside environments, dependency trees, Git metadata, and caches.
2. Reviewed the saved personal implementations and notebook, inventoried imported projects, and reproduced the findings without external model requests.
3. Added documentation and navigation in place. Retained all original directory names to preserve imports, local environments, notebooks, and coursework source paths.
4. Extended local-artifact ignore rules and made the deep-research template exception explicit. Preserved existing resource exclusions and left local files on disk.
5. Checked the final documentation, ignore behavior, existing-file preservation, and Git staging state.

Completion verification: of 1,799 original files fingerprinted, only the five edited documentation files and two ignore files changed. Three new documentation files were added. No original file was removed; all original source, notebook, manifest, and lockfile fingerprints match. The Git index fingerprint is unchanged, including the pre-existing staged `.gitignore` version.

## 2026-10-26: Numbered learning path

Scope: rename and move existing material into a learning sequence that also accommodates future Python, ML, LLM, and agent implementations. The path mapping and naming rules are in `docs/REPOSITORY_GUIDE.md`.

### Changes and rationale

1. Established the main stages `00_python_basics`, `01_machine_learning`, `02_deep_learning`, `03_llm`, `04_rag`, and `05_agents`. Topic numbers remain stable while child project numbers restart inside each stage.
2. Created README-only ML and deep-learning stages to reserve their positions without presenting planned work as completed implementations.
3. Grouped minimal chat and transformer study under LLMs; grouped the RAG and agent-loop demos under their corresponding stages. Normalized project/folder names and corrected the transformer directory typo.
4. Numbered the fourteen Python notes in their existing recommended order, renamed the strings exercise, and normalized the notebook filename. Kept implementation module names, source contents, and notebook cells/outputs unchanged.
5. Consolidated course archives and the self-study collection under `90_resources`, moving collections intact to preserve their internal paths, assignment layouts, and environments.
6. Updated root navigation, the resource index, project README paths, historical review links, and the three path-specific ignore entries. Added six stage/resource READMEs. No source fixes, dependency updates, staging, or commits were performed.

There were 29 explicit rename/move operations. Verification snapshots and the move manifest were kept outside the repository in a temporary working directory.

### Verification for this reorganization

| Check | Result |
| --- | --- |
| Original file inventory | All 1,802 original files are present at their mapped paths; 1,791 remain byte-identical. Only ten existing navigation documents and `.gitignore` changed. Six new READMEs bring the inventory to 1,808 files. |
| Original directories and modes | All 326 inventoried directories, including empty directories, remain at their mapped paths. Original regular-file permissions are unchanged. Excluded dependency, environment, cache, and Git directories remain present. |
| Implementation preservation | All 437 inventoried Python files, 24 notebooks, 10 `pyproject.toml` files, 8 `uv.lock` files, and the npm manifest/lockfile remain byte-identical, including pre-existing local edits. |
| Notebook structure | All 24 notebooks parse as JSON and contain their cell arrays; no cells were executed. |
| Navigation | All 148 relative links in the updated/new navigation and moved collection indexes resolve. All 36 explicit local paths in `INDEX.md` resolve. Historical old paths remain only in the migration table. |
| Ignore behavior | All 26 checks pass for source, templates, local credentials, environments, tool state, the RAG dataset, archived data, and the nested checkout. |
| Git state | The parent Git index fingerprint is unchanged. The nested `chess_app` retains HEAD `4aaabca1194ef5f175ccae4fecf902bc71cc303b` and a clean tree. |

### Environment relocation and limits

All five existing `.venv` directories moved with their projects. Header inspection confirmed installed scripts containing the old absolute paths in each environment. These generated environments were retained without rewriting installed files. Recreate an affected project's environment and reselect its notebook kernel before using its console scripts at the new location.

The checks above validate organization and preservation. Application behavior, existing syntax/import blockers, model services, and imported assignment suites were not rerun. The historical runtime findings above remain historical evidence.
