# Transformer study from scratch

A personal notebook exploring GPT-2 tokenization, token-to-logit conversion, softmax probabilities, and greedy next-token generation with TransformerLens and PyTorch.

Status: **in progress**. The notebook includes exploratory generation cells and notes. The later transformer implementation / attention section ends with an empty code cell; a full transformer implementation has not been completed.

## Files and environment

- `01_transformer_from_scratch.ipynb`: notebook, including its existing outputs.
- `pyproject.toml` / `uv.lock`: separate project environment with PyTorch and TransformerLens; the development group includes `ipykernel`.
- `.python-version`: Python 3.13 pin.

```sh
cd 03_llm/02_transformer_from_scratch
uv sync --locked --group dev
```

Open the notebook in a notebook-capable editor and select this project's `.venv` Python kernel. The notebook requests GPT-2 through `TransformerBridge.boot_transformers("gpt2")`, so model access or an existing cache is required. Hardware compatibility and the installed dependency environment were not tested in this pass.

The review inspected all cells and validated the notebook JSON without executing cells, downloading weights, changing outputs, or filling the unfinished implementation. On 2026-10-26, the project directory and notebook filename were normalized; the notebook contents were preserved.

[Repository home](../../README.md) · [Code review](../../docs/CODE_REVIEW.md)
