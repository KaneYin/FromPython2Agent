# Minimal chat

Personal experiments moving from a direct model-provider integration toward a shared chat-model interface.

Status: **work in progress**. The abstraction entry point currently fails to import a missing `model` package. Its draft adapters and message types also contain runtime blockers. The source is preserved as learning work; see the [review](../../docs/CODE_REVIEW.md) for verified findings.

## Files

| File | Role | State |
| --- | --- | --- |
| `without_abstraction/main.py` | Direct LangChain agent using Ollama | Reference demo; second-turn history currently omits assistant replies |
| `main.py` | Async chat loop using the proposed interface | Imports `model.base`, `model.litellm_model`, and `model.types`, which are not present |
| `ChatModel.py` | `Protocol` for a model adapter | Draft with unresolved type imports |
| `dataclass.py` | Message, usage, and response records | Draft with an incorrect dataclass import |
| `LiteLLMModel.py` | Async LiteLLM adapter | Draft with missing types and a `choise` typo |
| `baseChatModel.py` | Separate LangChain `BaseChatModel` experiment | Incomplete provider request and result construction |

The similarly named root-level files are not the `model/` package expected by `main.py`. They have not been renamed or repackaged during organization.

## Environment and direct example

The project pins Python 3.13 and has its own `pyproject.toml` and `uv.lock`.

```sh
cd 03_llm/01_minimal_chat
uv sync --locked
# With an Ollama service and the qwen3.5:9b model already available:
uv run --locked python without_abstraction/main.py
```

Type `exit` to end the direct example. It invokes the configured model on each question. Its provider responses were mocked during review; live execution was not tested.

The abstraction draft selects `openai/gpt-4o-mini`, but it remains blocked before any request. Completing its package structure, type imports, and adapters is future learning work, not part of the repository organization pass.

[Repository home](../../README.md) · [Repository guide](../../docs/REPOSITORY_GUIDE.md)
