# 项目：MicroAgent —— 从零实现的 ReAct Agent

## 项目背景与目标

我要从零实现一个 Python AI Agent 项目，**纯练手 + 开源作品**。目标是吃透 Agent 底层原理，所以代码必须显式、可读、可观测，不依赖任何 Agent 框架。

这一轮我们只做 **Phase 1：最小可跑的 ReAct Agent**。后续 Phase 会加 RAG、Reflection、Multi-Agent 等，但这一轮**严格控制范围**，不要超前实现。

## 硬性约束（违反任何一条都算失败）

1. **禁止引入任何 Agent 框架**：LangChain、LlamaIndex、LangGraph、AutoGen、CrewAI 等一律不许 import
2. **禁止使用 `openai` SDK**：直接用 `httpx` 调 OpenAI-compatible 的 `/v1/chat/completions` 接口（DeepSeek、通义、Ollama 都用这个协议）
3. **禁止流式输出**：第一版同步阻塞
4. **禁止过度抽象**：不要给 Memory 写抽象基类、不要搞插件系统、不要 Factory Pattern。能用 dataclass + 函数解决的就别上类层级
5. **每个文件 < 200 行**，超了就拆
6. **Python 3.12+**，强类型注解（`from __future__ import annotations` 全开）
7. **依赖最小化**：`httpx`、`pydantic`（仅用于配置）、`sympy`（计算器用）。除此之外每加一个依赖必须先问我

## 目录结构（严格遵守）

```
microagent/
├── microagent/
│   ├── __init__.py
│   ├── agent.py          # ReAct 主循环
│   ├── llm.py            # LLM 客户端（httpx 实现）
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base.py       # Tool dataclass + 注册表
│   │   └── calculator.py # 第一版唯一工具
│   ├── memory.py         # 短期记忆，就是个 list 的包装
│   ├── prompts.py        # System prompt 模板（动态拼接工具列表）
│   ├── parser.py         # ReAct 输出解析
│   ├── trace.py          # 执行轨迹记录（重点）
│   └── budget.py         # token / step 预算控制
├── examples/
│   └── quickstart.py
├── tests/
│   ├── test_parser.py
│   ├── test_tools.py
│   └── test_agent.py     # 用 mock LLM
├── pyproject.toml
└── README.md
```

## 实现分四轮，每轮结束后停下来等我 review，不要自己一口气写完

---

### 第一轮：LLM 客户端 + Tool 基础设施

**实现文件**：`llm.py`、`tools/base.py`、`tools/calculator.py`、`tests/test_tools.py`

**llm.py 要点**：
- `LLMClient` 类，构造参数：`base_url`、`api_key`、`model`、`timeout=60`
- 方法：`chat(messages: list[dict], stop: list[str] | None = None, temperature: float = 0.0) -> LLMResponse`
- `LLMResponse` dataclass：`content: str`、`usage: dict`（含 prompt_tokens / completion_tokens / total_tokens）、`latency_ms: float`
- 用 `httpx.Client`（同步），不要用 async
- 失败时抛 `LLMError`，包含原始响应体方便调试
- 不要做重试逻辑（Phase 1 不要）

**tools/base.py 要点**：
```python
@dataclass
class Tool:
    name: str
    description: str         # 给 LLM 看的，要写清楚用途和何时使用
    parameters: dict          # JSON Schema 格式，对齐 MCP / OpenAI function calling
    func: Callable[..., str]  # 返回值必须是字符串
    
    def invoke(self, **kwargs) -> str:
        # 必须 try/except，把异常转成字符串返回
        # 格式：f"Error: {type(e).__name__}: {e}"
        # 这样 Agent 才能感知到错误并重试
```

外加一个 `ToolRegistry`，就是 `dict[str, Tool]` 的简单包装，提供 `register`、`get`、`list_all`、`render_for_prompt`（输出工具列表的文本表示，给 system prompt 用）。

**tools/calculator.py 要点**：
- 用 `sympy.sympify` 解析表达式，**严禁 eval**
- 支持基本算术 + 常见数学函数
- parameters 严格按 JSON Schema 写

**tests/test_tools.py**：测 calculator 正常计算、除零、非法表达式、注入攻击尝试

完成后停下，告诉我："第一轮完成，等待 review"。

---

### 第二轮：Memory + Prompt + Parser

**实现文件**：`memory.py`、`prompts.py`、`parser.py`、`tests/test_parser.py`

**memory.py 要点**：
- 就一个 `Memory` 类，内部 `list[dict]`
- 方法：`add_user(text)`、`add_assistant(text)`、`add_observation(text)`、`to_messages() -> list[dict]`、`clear()`
- observation 在转 messages 时作为 `role="user"` 注入，内容前缀 `"Observation: "`（这是 ReAct 惯例，让模型理解上下文）
- 不要做摘要、不要做窗口、不要 RAG。就是个 list

**prompts.py 要点**：

System prompt 用以下模板（**严格按这个格式，不要自由发挥**）：

```
You are a helpful AI assistant that uses tools to answer questions.

You have access to the following tools:

{tool_descriptions}

Use the following format strictly:

Thought: your reasoning about what to do next
Action: the name of the tool to use, must be one of [{tool_names}]
Action Input: a single-line JSON object with the tool arguments

After you see the Observation, continue with another Thought/Action/Action Input cycle.

When you have enough information to answer, output:

Thought: your final reasoning
Final Answer: your answer to the user

Rules:
- Output ONE Thought + Action + Action Input per turn, then STOP and wait for Observation
- Action Input must be valid JSON on a single line
- If a tool returns an error, reason about it and try a different approach
- Do not fabricate Observations; they will be provided to you
```

`build_system_prompt(registry: ToolRegistry) -> str` 动态拼接。

**parser.py 要点**：

```python
@dataclass
class ParsedStep:
    thought: str
    is_final: bool
    final_answer: str | None = None
    action: str | None = None
    action_input: dict | None = None
    parse_error: str | None = None  # 解析失败时填，agent 会把这个作为 observation 反馈
```

`parse(text: str) -> ParsedStep` 用正则。关键边界：
- 多个 Action 块：只取第一个
- Action Input 不是合法 JSON：`parse_error` 填上错误说明，**不要抛异常**
- 既没 Action 也没 Final Answer：`parse_error="No Action or Final Answer found"`
- Final Answer 优先于 Action（同时存在时取 Final Answer）

**tests/test_parser.py**：每个边界 case 都要测。

完成后停下。

---

### 第三轮：Agent 主循环 + Trace + Budget

**实现文件**：`agent.py`、`trace.py`、`budget.py`、`tests/test_agent.py`

**trace.py 要点**：

```python
@dataclass
class TraceEvent:
    step: int
    type: Literal["think", "action", "observation", "final", "error", "budget_exceeded"]
    timestamp: float          # time.time()
    content: dict             # 灵活字段
    tokens: dict | None = None
    latency_ms: float | None = None

class Trace:
    events: list[TraceEvent]
    
    def add(self, event: TraceEvent) -> None: ...
    def to_markdown(self) -> str: ...   # 必须实现，README 要用
    def to_json(self) -> list[dict]: ...
    def summary(self) -> dict:          # {total_steps, total_tokens, total_latency_ms, finished: bool}
```

`to_markdown` 输出样例（要美观可读）：
```
# Agent Trace

**Query**: 123 * 456 等于多少？
**Steps**: 2 | **Tokens**: 543 | **Latency**: 1823ms

## Step 1 — think (412 tokens, 821ms)
**Thought**: 我需要用 calculator 工具计算 ...
**Action**: `calculator`
**Action Input**: `{"expression": "123 * 456"}`

## Step 1 — observation
```
56088
```

## Step 2 — final (131 tokens, 1002ms)
**Final Answer**: 123 × 456 = 56088
```

**budget.py 要点**：

```python
@dataclass
class Budget:
    max_steps: int = 10
    max_total_tokens: int | None = None
    
    _steps_used: int = 0
    _tokens_used: int = 0
    
    def consume_step(self) -> None: ...
    def consume_tokens(self, n: int) -> None: ...
    def exceeded(self) -> tuple[bool, str | None]: ...  # 返回是否超出 + 原因
```

成本控制 Phase 1 先不做（不同模型定价不一，留给 Phase 2）。

**agent.py 主循环（核心）**：

```python
class Agent:
    def __init__(
        self,
        llm: LLMClient,
        tools: ToolRegistry,
        memory: Memory | None = None,
        budget: Budget | None = None,
    ):
        ...
    
    def run(self, query: str) -> AgentResult:
        # AgentResult: dataclass, 字段：answer: str | None, trace: Trace, finished: bool, stop_reason: str
        ...
```

主循环逻辑（**严格按这个顺序**）：

```
1. memory.add_user(query)
2. trace 开始
3. for step in 1..max_steps:
   a. 检查 budget，超了就记录 budget_exceeded 事件并退出
   b. messages = [system_prompt] + memory.to_messages()
   c. response = llm.chat(messages, stop=["Observation:"])
      —— stop 参数极其重要，防止模型自己幻觉 Observation
   d. trace 记录 think 事件（带 tokens 和 latency）
   e. budget.consume_tokens(response.usage.total_tokens)
   f. parsed = parser.parse(response.content)
   g. memory.add_assistant(response.content)
   h. 如果 parsed.parse_error:
      —— 把 parse_error 作为 observation 喂回去，让模型自我修正
      observation = f"Error parsing your output: {parsed.parse_error}. Please follow the format strictly."
      memory.add_observation(observation)
      trace 记录 observation 事件
      continue
   i. 如果 parsed.is_final:
      trace 记录 final 事件
      return AgentResult(answer=parsed.final_answer, finished=True, ...)
   j. 如果 parsed.action 不在 registry:
      observation = f"Error: tool '{parsed.action}' not found. Available: {tool_names}"
      memory.add_observation(observation)
      trace 记录 observation
      continue
   k. observation = tools.get(parsed.action).invoke(**parsed.action_input)
   l. memory.add_observation(observation)
   m. trace 记录 action + observation 事件
   n. budget.consume_step()
4. 循环结束没拿到 final answer，返回 finished=False，stop_reason="max_steps"
```

**tests/test_agent.py**：用 mock LLM（不真调 API），按预设脚本返回 think/action 序列，验证：
- 单步直接 Final Answer
- 两步工具调用
- 工具报错后重试
- parse_error 后重试
- max_steps 触发退出

完成后停下。

---

### 第四轮：examples + README + 真实验收

**实现文件**：`examples/quickstart.py`、`README.md`、`pyproject.toml`

**quickstart.py**：从环境变量读 `LLM_BASE_URL` / `LLM_API_KEY` / `LLM_MODEL`，注册 calculator，跑 3 个真实 query，每个跑完打印 `trace.to_markdown()`。

**README.md 必须包含**：
- 一句话介绍 + design philosophy（显式、可观测、零框架依赖）
- Quickstart（5 行代码跑起来）
- 架构图（用 ASCII art 或者 mermaid，**不要找外部图床**）
- 一个完整的 trace 样例（直接贴 markdown 输出）
- Roadmap（Phase 2/3/4 的计划，列出来但标 TODO）
- 不要写 LICENSE 之外的法律声明，不要写 emoji 满天飞

**pyproject.toml**：用 hatchling 或 setuptools，Python >=3.11，依赖只有 httpx / pydantic / sympy（dev 依赖加 pytest）。

完成后告诉我，我自己跑验收清单：
1. `agent.run("123 * 456 等于多少？")` 返回正确结果
2. `agent.run("先算 12 * 8，再把结果加 100")` 两步工具调用
3. 故意构造让 calculator 报错的 query，看 Agent 是否重试
4. `agent.run("你好")` 直接 Final Answer，不调工具
5. 设 max_steps=2，喂复杂任务，看是否优雅停止
6. 每次跑完 `trace.to_markdown()` 输出完整可读

---

## 现在开始第一轮

确认理解了上面所有约束后，开始实现第一轮（llm.py + tools/base.py + tools/calculator.py + tests/test_tools.py）。完成后停下等我 review，**不要继续第二轮**。

如果有任何地方不清楚，先问我，不要自己脑补决定。