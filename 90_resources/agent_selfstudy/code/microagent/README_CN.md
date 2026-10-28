# MicroAgent

一个从零实现的 Python ReAct Agent — 零框架依赖，全程可观测。

[English](README.md) | 中文

## 设计理念

**显式优于魔法。** 每一次 LLM 调用、工具执行、推理步骤都被记录在结构化的 Trace 中。不依赖 LangChain、LlamaIndex 等任何 Agent 框架，所有逻辑清晰可读。

## 亮点

**双推理策略** — Text ReAct 和 Function Calling 作为一等策略共存，一行代码切换：

```python
from microagent.strategies import FunctionCallingStrategy, TextReActStrategy

# Function Calling（默认，使用 OpenAI tools API 原生调用）
agent = Agent(llm=llm, tools=tools, strategy=FunctionCallingStrategy())

# Text ReAct（经典 Thought/Action/Observation 循环 + 正则解析）
agent = Agent(llm=llm, tools=tools, strategy=TextReActStrategy())
```

7 个 query x 3 次运行对比基准测试，FC 在典型工具调用场景下节省 15-50% token 和 30-60% 延迟。详见 [compare_strategies.py](examples/compare_strategies.py) 和 [traces/](examples/traces/)。

**LLM I/O 可视化** — 零依赖本地 Web 服务器，可视化每一次 LLM 调用和工具执行，支持折叠的请求/响应面板：

```bash
python -m microagent.viewer.server
# 浏览器打开 http://127.0.0.1:8765，暗色主题日志查看器
```

**Failure Modes 研究** — 不是 bug 列表，而是边界研究。每条失败记录区分"第一直觉"和"真实根因"，附 trace 证据。详见 [doc/phase1.5/FAILURE_MODES.md](doc/phase1.5/FAILURE_MODES.md)。

## 快速开始

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

设置环境变量运行完整示例：

```bash
# 方式一：.env 文件（推荐）
echo "LLM_BASE_URL=https://api.deepseek.com" > .env
echo "LLM_API_KEY=your-key" >> .env
echo "LLM_MODEL=deepseek-chat" >> .env
python examples/quickstart.py

# 方式二：环境变量
LLM_API_KEY=your-key python examples/quickstart.py
```

## 架构

```
┌──────────────────────────────────────────────────────┐
│                       Agent                          │
│                                                      │
│   run(query)                                         │
│     │                                                │
│     ▼                                                │
│   ┌──────────────┐                                   │
│   │   Strategy   │ ◄── TextReAct / FunctionCalling   │
│   │ (构建请求,   │                                   │
│   │  解析响应)   │                                   │
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
│                     工具调用记录到 trace               │
└──────────────────────────────────────────────────────┘
```

## 项目结构

```
microagent/
├── microagent/
│   ├── agent.py              # ReAct 主循环，策略驱动
│   ├── llm.py                # LLM 客户端 (httpx)，调用记录
│   ├── logger.py             # 结构化 JSONL 日志
│   ├── memory.py             # 短期记忆
│   ├── parser.py             # ReAct 正则解析
│   ├── prompts.py            # System prompt 模板
│   ├── trace.py              # 执行轨迹 (Markdown/JSON)
│   ├── budget.py             # 步数/token 预算控制
│   ├── inspect.py            # 调试辅助
│   ├── strategies/
│   │   ├── base.py           # ReasoningStrategy 抽象基类
│   │   ├── text_react.py     # Text ReAct 策略
│   │   └── function_call.py  # OpenAI Function Calling 策略
│   ├── tools/
│   │   ├── base.py           # Tool dataclass + 注册表
│   │   ├── calculator.py     # sympy 计算器工具
│   │   ├── text_stats.py     # 文本分析工具
│   │   └── datetime_now.py   # 当前时间工具
│   └── viewer/
│       ├── server.py         # 本地 Web 服务器 (stdlib)
│       └── index.html        # 暗色主题日志查看器
├── examples/
│   ├── quickstart.py         # 快速入门
│   ├── compare_strategies.py # 双策略对比基准测试
│   ├── traces/               # 保存的 trace 文件
│   ├── failure_modes.py      # 边缘 case 测试
│   └── test_tool_selection.py
├── tests/
│   ├── test_parser.py
│   ├── test_tools.py
│   └── test_agent.py         # 52 个测试，覆盖两种策略
└── pyproject.toml
```

## 核心模块说明

| 模块 | 职责 |
|------|------|
| `agent.py` | ReAct 主循环，策略驱动：提问 → 调 LLM → 解析 → 调工具 → 循环 |
| `llm.py` | 同步 httpx 客户端，调用记录，支持 tools/tool_choice 透传 |
| `strategies/` | 推理策略抽象：TextReAct（正则解析）和 FunctionCalling（原生 API）|
| `logger.py` | 结构化 JSONL 日志，记录每次 LLM 调用和工具执行 |
| `viewer/` | 零依赖本地 Web 可视化，暗色主题，折叠式请求/响应面板 |
| `parser.py` | 正则解析 LLM 输出，抗噪声（处理模型追加的 XML 标签）|
| `tools/` | calculator / text_stats / datetime_now，可扩展 |
| `trace.py` | 执行轨迹记录，支持 Markdown/JSON 输出，含策略标识 |
| `budget.py` | 步数/token 预算控制，超出优雅退出 |

## 路线图

- **Phase 2**: 多工具并行执行、RAG（文档检索增强）、成本估算
- **Phase 3**: Reflection（自我反思与纠错）、Planning（任务分解）
- **Phase 4**: Multi-Agent（多 Agent 协作）、Streaming 输出

## License

MIT
