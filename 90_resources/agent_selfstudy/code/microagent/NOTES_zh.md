# microagent 学习笔记（极简 ReAct Agent，从零实现）

> 上游仓库：https://github.com/ql0xdev/MicroAgent（MIT；README 有中文版 `README_CN.md`）
>
> 设计哲学：Explicit over magic —— 零框架依赖，每次 LLM 调用、工具执行、推理步骤都记录在结构化 trace 里。

## 这个仓库实现了什么

**一句话**：一个零框架依赖、手写的极简 ReAct agent：LLM 客户端（httpx 直调 OpenAI 兼容接口）+ 工具注册表 + 可插拔推理策略 + 主循环，附带完整测试和 LLM I/O 可视化。

**一段话**：这是"理解 agent 本质"最好的小仓库之一：没有 LangChain/LlamaIndex，全部自己写。核心抽象只有 5 个：`LLMClient`（httpx 发请求）、`ToolRegistry`（工具注册与渲染进 prompt）、`Memory`（对话历史）、`ReasoningStrategy`（怎么"想"）、`Agent`（主循环：想→调工具→记 observation→重复）。最有特色的是**双推理策略**：`TextReActStrategy`（经典 Thought/Action/Observation 文本循环，正则解析）和 `FunctionCallingStrategy`（OpenAI 原生 tools API）并存，一行代码切换，仓库还带了两者 7×3 的 token/延迟对比 benchmark。另有 `Budget`（步数/token 上限）、`Trace`（执行轨迹转 Markdown/JSON）、零依赖的本地 web 可视化（`python -m microagent.viewer.server` 看每次 LLM 请求/响应），以及 `doc/phase1.5/FAILURE_MODES.md` 记录的失败模式边界研究。

## 核心文件

| 文件 | 作用 |
|---|---|
| `microagent/agent.py` | 主循环：`Agent.run(query)` 串起 strategy/memory/tools/budget，产出 `AgentResult(answer, trace, finished, stop_reason)` |
| `microagent/strategies/base.py` | `ReasoningStrategy` 抽象：`build_request()`（组装 LLM 请求）+ `parse_response()`（解析出工具调用） |
| `microagent/strategies/text_react.py` | 文本 ReAct 策略：Thought/Action/Action Input 格式，`stop=["Observation:"]` 截断 |
| `microagent/strategies/function_call.py` | Function Calling 策略：OpenAI tools 参数原生调用 |
| `microagent/strategies/plan_execute.py` | Plan-Execute 策略（先规划后执行） |
| `microagent/prompts.py` | ReAct system prompt 模板（Thought/Action/Observation 格式约束 + 规则） |
| `microagent/parser.py` | 文本 ReAct 输出的正则解析器 |
| `microagent/llm.py` | httpx 直调的 LLM 客户端，记录每次调用（给 viewer 用） |
| `microagent/memory.py` | 短期记忆：维护 messages 列表 |
| `microagent/budget.py` | 步数/token 预算控制，防死循环和烧钱 |
| `microagent/trace.py` | 执行轨迹：结构化事件，可转 Markdown/JSON |
| `microagent/tools/` | `base.py`（Tool dataclass + ToolRegistry）、`calculator.py`（sympy 计算）、`text_stats.py`、`datetime_now.py` |
| `microagent/viewer/` | 零依赖本地 web 服务 + 深色日志查看器，可视化每次 LLM I/O |
| `examples/quickstart.py` | 最小可运行 demo；`compare_strategies.py` 是双策略对比 benchmark |
| `tests/` | 52 个测试，覆盖两种策略的解析、工具、主循环 |

## 怎么运行

依赖：Python + `httpx` 等极少依赖（`pyproject.toml` / `uv.lock`），需要一个 OpenAI 兼容的 LLM API（示例用 DeepSeek）。

```bash
# 方式一：.env 文件（推荐）
echo "LLM_BASE_URL=https://api.deepseek.com" > .env
echo "LLM_API_KEY=你的key" >> .env
echo "LLM_MODEL=deepseek-chat" >> .env
python examples/quickstart.py

# 最小代码（README Quickstart）
from microagent.agent import Agent
from microagent.llm import LLMClient
from microagent.tools.base import ToolRegistry
from microagent.tools.calculator import calculator_tool

llm = LLMClient(base_url="https://api.deepseek.com", api_key="sk-xxx", model="deepseek-chat")
tools = ToolRegistry(); tools.register(calculator_tool)
agent = Agent(llm=llm, tools=tools)
result = agent.run("123 * 456 等于多少？")
print(result.answer)             # 56088
print(result.trace.to_markdown())

# 看 LLM 每次调用的可视化
python -m microagent.viewer.server   # 打开 http://127.0.0.1:8765
```

## 关键设计点

1. **策略模式解耦"怎么想"**：`ReasoningStrategy` 接口把"组装请求"和"解析响应"抽象出来，TextReAct / FunctionCalling / PlanExecute 可互换——理解了这点就理解了 agent 框架的内核。
2. **文本 ReAct 靠 prompt 工程 + stop 序列**：system prompt 强制 `Thought:/Action:/Action Input:` 格式，`stop=["Observation:"]` 让模型一次只输出一步，`Observation:` 由框架填入工具结果后继续——这就是 ReAct 论文的工程实现。
3. **Budget 是生产级必需品**：`max_steps` / `max_tokens` 双上限 + `stop_reason`（final_answer/max_steps/max_tokens），没有它 agent 会无限循环烧钱。
4. **可观测性优先**：`Trace` 记录每一步 thought/action/observation，`LLMClient` 记录每次请求响应，viewer 可视化——debug agent 不靠 print 靠 trace。
5. **失败模式研究**：`doc/phase1.5/FAILURE_MODES.md` 区分"第一直觉"和"根因"，配合 `MICROAGENT_DEBUG=1` 的消息序列校验（tool_call_id 对齐检查），是很好的工程习惯示范。
