# Agent loop

A draft demonstrating the cycle of requesting tool calls, executing tools, appending tool observations, and asking the model for its next action.

Status: **unfinished and syntax-blocked**. Several continuation lines of explanatory prose in `main.py` lack comment markers. No code was corrected during the organization pass.

## Current behavior and gaps

- `execute_tool()` returns canned time and weather strings and ignores its arguments.
- The main loop has no iteration limit, as already noted in the source.
- `OpenAI()` is constructed at module level. The draft specifies `Qwen3-0.6B` without configuring a matching service endpoint in the script; working provider/model configuration remains unverified.
- The file cannot currently reach the loop because parsing fails first. See the [review](../../docs/CODE_REVIEW.md) for the exact location.

## Environment

`pyproject.toml` declares Python `>=3.13` and the `openai` dependency; `.python-version` pins 3.13. `uv.lock` belongs to this project alone.

```sh
cd 05_agents/01_agent_loop
uv sync --locked
```

This installs dependencies only. There is no working run command until the draft is completed. The implementation, tool stubs, and loop remain unchanged.

[Repository home](../../README.md) · [Repository guide](../../docs/REPOSITORY_GUIDE.md)
