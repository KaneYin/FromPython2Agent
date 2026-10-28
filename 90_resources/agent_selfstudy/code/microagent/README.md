# MicroAgent

English | [中文](README_CN.md)

A minimal ReAct Agent implemented from scratch in Python — zero framework dependency, fully observable.

**Design Philosophy**: Explicit over magic. Every LLM call, tool invocation, and reasoning step is recorded in a structured trace. No LangChain, no LlamaIndex, no hidden abstractions.

## Highlights

**Dual Reasoning Strategy** — Text ReAct and Function Calling coexist as first-class strategies, switchable with one line of code:

```python
from microagent.strategies import FunctionCallingStrategy, TextReActStrategy

# Function Calling (default, uses OpenAI tools API natively)
agent = Agent(llm=llm, tools=tools, strategy=FunctionCallingStrategy())

# Text ReAct (classic Thought/Action/Observation loop with regex parsing)
agent = Agent(llm=llm, tools=tools, strategy=TextReActStrategy())
```

Benchmarked side-by-side across 7 queries x 3 runs. FC saves 15-50% tokens and 30-60% latency on typical tool-calling tasks. See [compare_strategies.py](examples/compare_strategies.py) and [traces/](examples/traces/).

**LLM I/O Viewer** — Zero-dependency local web server visualizes every LLM call and tool invocation with collapsible request/response panels:

```bash
python -m microagent.viewer.server
# Opens http://127.0.0.1:8765 with dark-theme log viewer
```

**Failure Modes Research** — Not a bug list, but a boundary study. Each failure distinguishes "first instinct" vs "root cause" with trace evidence. See [doc/phase1.5/FAILURE_MODES.md](doc/phase1.5/FAILURE_MODES.md).

## Quickstart

```python
from microagent.agent import Agent
from microagent.llm import LLMClient
from microagent.tools.base import ToolRegistry
from microagent.tools.calculator import calculator_tool

llm = LLMClient(base_url="https://api.deepseek.com", api_key="sk-xxx", model="deepseek-chat")
tools = ToolRegistry()
tools.register(calculator_tool)
agent = Agent(llm=llm, tools=tools)
result = agent.run("123 * 456 等于多少？")
print(result.answer)        # 56088
print(result.trace.to_markdown())
```

Set environment variables and run the full demo:

```bash
# Option 1: .env file (recommended)
echo "LLM_BASE_URL=https://api.deepseek.com" > .env
echo "LLM_API_KEY=your-key" >> .env
echo "LLM_MODEL=deepseek-chat" >> .env
python examples/quickstart.py

# Option 2: environment variables
LLM_API_KEY=your-key python examples/quickstart.py
```

## Architecture

```
┌──────────────────────────────────────────────────────┐
│                       Agent                          │
│                                                      │
│   run(query)                                         │
│     │                                                │
│     ▼                                                │
│   ┌──────────────┐                                   │
│   │   Strategy   │ ◄── TextReAct / FunctionCalling   │
│   │ (build req,  │                                   │
│   │  parse resp) │                                   │
│   └──────┬───────┘                                   │
│          │                                            │
│   ┌──────▼───────┐    ┌──────────┐                   │
│   │  Memory      │◄──►│   LLM    │                   │
│   │ (对话历史)    │    │ (httpx)  │                   │
│   └──────────────┘    └──────────┘                   │
│         ▲                    ▲                        │
│         │                    │                        │
│   ┌─────┴──────┐    ┌───────┴──────┐    ┌──────────┐ │
│   │  Budget    │    │    Tools     │    │  Trace   │ │
│   │(步数/token)│    │(calculator,  │    │(执行轨迹)│ │
│   └────────────┘    │ text_stats,  │    └──────────┘ │
│                     │ datetime_now)│          ▲       │
│                     └──────┬───────┘          │       │
│                            │                  │       │
│                            └──────────────────┘       │
│                     tool calls logged to trace        │
└──────────────────────────────────────────────────────┘
```

## Project Structure

```
microagent/
├── microagent/
│   ├── agent.py              # ReAct main loop, strategy-driven
│   ├── llm.py                # LLM client (httpx), call recording
│   ├── logger.py             # Structured JSONL logging
│   ├── memory.py             # Short-term memory
│   ├── parser.py             # ReAct regex parser
│   ├── prompts.py            # System prompt templates
│   ├── trace.py              # Execution trace (Markdown/JSON)
│   ├── budget.py             # Step/token budget control
│   ├── inspect.py            # Debug helpers
│   ├── strategies/
│   │   ├── base.py           # ReasoningStrategy ABC
│   │   ├── text_react.py     # Text ReAct (Phase 1)
│   │   └── function_call.py  # OpenAI Function Calling
│   ├── tools/
│   │   ├── base.py           # Tool dataclass + ToolRegistry
│   │   ├── calculator.py     # sympy-based math tool
│   │   ├── text_stats.py     # Text analysis tool
│   │   └── datetime_now.py   # Current time tool
│   └── viewer/
│       ├── server.py         # Local web server (stdlib)
│       └── index.html        # Dark-theme log viewer
├── examples/
│   ├── quickstart.py         # Quick start demo
│   ├── compare_strategies.py # Side-by-side benchmark
│   ├── traces/               # Saved trace files
│   ├── failure_modes.py      # Edge case tests
│   └── test_tool_selection.py
├── tests/
│   ├── test_parser.py
│   ├── test_tools.py
│   └── test_agent.py         # 52 tests, covers both strategies
└── pyproject.toml
```

## Roadmap

- **Phase 2**: Multi-tool parallel execution, RAG, cost estimation
- **Phase 3**: Reflection, Planning, task decomposition
- **Phase 4**: Multi-Agent collaboration, Streaming output

## License

MIT
