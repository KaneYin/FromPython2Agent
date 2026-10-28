# smolagents-codeagent-demo 学习笔记（基于 smolagents 的 CodeAgent 实战 demo）

> 上游仓库：https://github.com/botextractai/ai-huggingface-smolagents
>
> 说明：smolagents 主仓库（https://github.com/huggingface/smolagents）体积较大，按任务要求只记录链接不 clone；本仓库是一个基于它的极简实战 demo。

## 这个仓库实现了什么

**一句话**：用 HuggingFace `smolagents` 的 `CodeAgent` 做一个"联网调研 + 画地图"的多智能体小系统：manager agent 指挥 web agent 搜"全球人口最多的 10 个城市及 12 月气温"，最后用 Plotly 画成地理图存为 `saved_map.png`。

**一段话**：这是理解 **CodeAgent vs ToolCallingAgent** 区别最直观的例子。传统 tool-calling agent 让 LLM 一次输出一个 JSON 函数调用；而 smolagents 的 CodeAgent 让 LLM 直接写一整段 Python 代码（一次规划多个工具调用），由框架的沙箱执行器运行——通常更少 LLM 轮次、更低延迟和成本。demo 里展示了两种自定义工具写法（`@tool` 装饰器函数式、`Tool` 子类式）、多 agent 协作（manager + 专职搜索的 web_agent）、`agent.visualize()` 打印 agent 树、以及授权 import 白名单等安全机制。整个逻辑收敛在单个 `main.py`（217 行）里。

## 核心文件

| 文件 | 作用 |
|---|---|
| `main.py` | 全部逻辑（217 行）：定义工具 → 建模型 → 建 manager/web 双 CodeAgent → 跑任务 → 画 Plotly 地图 |
| `requirements.txt` | 依赖：`smolagents==1.14.0`、`tavily-python`（搜索）、`plotly`/`kaleido`（画图）、`markdownify` 等 |
| `readme.md` | 教程：CodeAgent 原理、安全执行机制、需要的 API key |
| `.env.example` | 需要填 `OPENAI_API_KEY` 和 `TAVILY_API_KEY` |
| `readme_images/` | 效果截图 |

## 怎么运行

依赖：Python、`pip install -r requirements.txt`；需要 OpenAI API key + Tavily 搜索 API key（免费额度即可）。

```bash
pip install -r requirements.txt
cp .env.example .env   # 填入 OPENAI_API_KEY 和 TAVILY_API_KEY
python main.py         # 跑完在项目根目录生成 saved_map.png
```

核心代码骨架（`main.py` 提炼）：

```python
from smolagents import CodeAgent, OpenAIServerModel, tool, Tool

@tool
def web_search(query: str) -> str:
    """Searches the web for your query."""
    ...  # 用 TavilyClient 搜索

class VisitWebpageTool(Tool):   # 类式工具：name/description/inputs/output_type + forward()
    ...

model = OpenAIServerModel(model_id="gpt-4o", api_key=...)
web_agent = CodeAgent(tools=[web_search, VisitWebpageTool()], model=model, ...)
manager_agent = CodeAgent(tools=[], model=model, managed_agents=[web_agent],
                          additional_authorized_imports=["plotly", "pandas", ...])
manager_agent.run("返回全球人口最多的10个城市、人口（百万，两位小数）、12月日均温…")
```

## 关键设计点

1. **CodeAgent 的核心思想**：action = 一段 Python 代码而不是单个 JSON tool call。LLM 一次写完"查数据→算→画图"的完整代码，框架执行——适合多步工具链任务，轮次少、容错高（代码里能自己处理异常）。
2. **两种工具定义方式**：`@tool` 装饰器（函数 + docstring 即工具，适合简单工具）vs `Tool` 子类（显式 `inputs` schema + `forward()`，适合复杂/可复用工具）。
3. **多智能体分工**：`managed_agents=[web_agent]` 让 manager 把"上网搜"委托给专职 web_agent，自己专注汇总和画图；`manager_agent.visualize()` 可打印 agent 树。
4. **安全执行**：smolagents 自研 Python 执行器有 import 白名单（默认只放行 `re/math/datetime/numpy` 等），白名单外需 `additional_authorized_imports` 显式授权；更高安全要求可用 Docker/E2B 沙箱。
5. **prompt 即任务描述**：`request_cities` 字符串直接描述输出格式（"人口百万、两位小数"），CodeAgent 靠 system prompt 约束代码风格——工具描述写得越清楚，agent 表现越好。
