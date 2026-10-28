# Phase 2.2: Plan-and-Execute Strategy

新增第三种推理范式：静态 Plan-and-Execute。与现有 TextReActStrategy / FunctionCallingStrategy 平级。

## 核心设计

**两阶段执行**：

1. **Plan 阶段**：一次 LLM call 生成完整执行计划（纯文本格式）
2. **Execute 阶段**：按 plan 逐步执行，每步走 function calling 调工具

**静态版本**：plan 一旦生成不可更改，不做 replan。Replan 留到 Phase 2.2.2。

## 实现位置

新文件 `microagent/strategies/plan_execute.py`，类名 `PlanExecuteStrategy`，name = `"plan_execute"`。

## 详细设计

### 1. 内部状态

PlanExecuteStrategy 是有状态的（不同于前两个无状态 strategy）：

```python
@dataclass
class PlanStep:
    index: int           # 1-indexed
    description: str     # plan 这一步的自然语言描述
    completed: bool = False
    result: str | None = None  # execute 后的工具返回


class PlanExecuteStrategy(ReasoningStrategy):
    name = "plan_execute"
    
    def __init__(self):
        self._plan: list[PlanStep] | None = None
        self._current_step_idx: int = 0
        self._plan_generated: bool = False
    
    def reset(self) -> None:
        """Agent 每次 run 开始前调用"""
        self._plan = None
        self._current_step_idx = 0
        self._plan_generated = False
```

**关键**：Agent.run() 开头要调 strategy.reset()（如果 strategy 有这个方法）。在 Agent 基类里加一个 hasattr 检查即可，不强制其他 strategy 实现。

### 2. Plan 阶段的 prompt 模板

Plan 阶段的 system prompt：

```
You are a planning assistant. Given a user task and available tools, generate a step-by-step plan to accomplish the task.

Available tools:
{tool_descriptions}

Output format (strict):

Plan:
1. <one concrete action, mentioning which tool if applicable>
2. <next action>
3. ...

Rules:
- Each step must be a single concrete action
- If a step needs a tool, name the tool explicitly
- Plan must be linear (no branches, no conditionals)
- Maximum 8 steps
- The final step should produce the answer to the user
- Do not execute the plan, only generate it
```

User message 就是用户原始 query。

**注意**：Plan 阶段**不传 tools 字段**（function calling 关闭），让模型纯文本输出。

### 3. Plan 解析

`_parse_plan(text: str) -> list[PlanStep]`：

- 用正则匹配 `^\d+\.\s+(.+)$` 提取每个步骤
- 如果解析不出任何步骤，返回空 list（agent 会兜底报错）
- 不做语义校验，把 description 原文存下来

### 4. Execute 阶段的 prompt 构造

每个 execute step 调用 LLM 时，messages 结构：

```
system: "You are executing step N of a multi-step plan. Use the provided tool to accomplish this specific step. If the step doesn't need a tool, respond with the answer directly."

user: "Original task: <user query>

Full plan:
1. ... [completed: result=...]
2. ... [completed: result=...]
3. ... ← CURRENT STEP: <plan[2].description>
4. ...

Execute step 3 only."
```

**关键**：
- 把已完成步骤的 result 内联进 plan，让模型有上下文
- 当前步骤用 `← CURRENT STEP` 标记
- 后续未完成步骤也展示，让模型知道全局
- Execute 阶段**开启 function calling**（传 tools 字段）

### 5. build_request 的分支逻辑

```python
def build_request(self, memory, registry):
    if not self._plan_generated:
        # Plan 阶段
        messages = [
            {"role": "system", "content": PLAN_SYSTEM_PROMPT.format(...)},
            {"role": "user", "content": <用户 query, 从 memory 第一条取>},
        ]
        return messages, {}  # 不传 tools
    
    # Execute 阶段
    current_step = self._plan[self._current_step_idx]
    messages = [
        {"role": "system", "content": EXECUTE_SYSTEM_PROMPT},
        {"role": "user", "content": self._render_execute_prompt()},
    ]
    tools = [...]  # 同 FunctionCallingStrategy
    return messages, {"tools": tools, "tool_choice": "auto"}
```

**注意**：Execute 阶段每次都重新构造 messages，**不累积历史**——历史信息通过 plan 状态（已完成步骤的 result）传递。这是 Plan-and-Execute 比 ReAct 省 token 的关键。

### 6. parse_response 的分支逻辑

```python
def parse_response(self, response):
    if not self._plan_generated:
        # Plan 阶段：解析 plan
        plan_steps = self._parse_plan(response.content)
        if not plan_steps:
            return ParsedStep(
                thought=None, is_final=False,
                parse_error="Failed to parse plan from LLM output",
            )
        
        self._plan = plan_steps
        self._plan_generated = True
        
        # Plan 阶段不算作 final，也不调工具
        # 返回一个特殊 ParsedStep，让 agent 主循环跳过工具执行直接进入下一轮
        return ParsedStep(
            thought=f"Generated plan with {len(plan_steps)} steps",
            is_final=False,
            tool_calls=[],  # 空 list，表示这一步不调工具
        )
    
    # Execute 阶段：复用 FunctionCallingStrategy 的解析逻辑
    # ... 提取 tool_calls ...
    
    # 判断是否所有 plan step 都完成了
    if self._current_step_idx >= len(self._plan) - 1 and <没有更多 tool_calls>:
        return ParsedStep(
            thought=...,
            is_final=True,
            final_answer=response.content,
        )
```

### 7. Agent 主循环的兼容性改造

agent.py 需要小改：

**改造 1**：run() 开头调 strategy.reset()（如果有）

```python
if hasattr(strategy, "reset"):
    strategy.reset()
```

**改造 2**：处理 `tool_calls=[]` 的情况（plan 阶段产物）

当前主循环看到 `parsed.tool_calls` 是空 list 会怎样？需要明确：

```python
if parsed.is_final:
    return ...

if not parsed.tool_calls:
    # Plan 阶段刚生成完计划，直接进入下一轮 Execute
    # 不消耗 step budget（或者消耗，看你怎么定义）
    # 建议：plan 阶段算 1 step（公平对比）
    continue
```

**改造 3**：Execute 步骤完成后，让 strategy 推进 _current_step_idx

新增一个 strategy 钩子方法：

```python
class ReasoningStrategy:
    def on_step_completed(self, observations: list[str]) -> None:
        """工具执行完后调用，让 strategy 更新内部状态。默认 no-op。"""
        pass
```

PlanExecuteStrategy 重写：

```python
def on_step_completed(self, observations):
    if not self._plan_generated:
        return
    # Execute 步骤完成
    if self._current_step_idx < len(self._plan):
        self._plan[self._current_step_idx].completed = True
        self._plan[self._current_step_idx].result = "\n".join(observations)
        self._current_step_idx += 1
```

agent.py 在 tool 执行循环结束后调：

```python
if hasattr(strategy, "on_step_completed"):
    strategy.on_step_completed([obs for obs in step_observations])
```

### 8. Trace 渲染

`trace.py` 在渲染 plan_execute strategy 时，增加 plan 可视化区块：

think 事件 content 里加 `"plan_phase": "planning" | "executing"` 字段。

第一次 think（plan 阶段）渲染时：

```markdown
## Step 1 — think (planning) (...)
**Generated Plan**:
1. ...
2. ...
3. ...
```

后续 think（execute 阶段）渲染时：

```markdown
## Step 2 — think (executing step 1/3) (...)
**Current Plan Step**: ...
**Action**: ...
```

### 9. quickstart.py 加示例

```python
from microagent.strategies import PlanExecuteStrategy

agent = Agent(llm=llm, tools=registry, strategy=PlanExecuteStrategy())
result = agent.run("先算 12 * 8，再把结果加 100")
print(result.trace.to_markdown())
```

## 验证脚本

新建 `examples/compare_three_strategies.py`：

跑 7 个 query × 3 strategies × 3 runs，输出对比表：

```
queries = [
    "你好，介绍一下你自己",
    "123 * 456 等于多少？",
    "先算 12 * 8，再把结果加 100",
    "现在几点？",
    "帮我算 sqrt(-1)，告诉我结果",
    "统计'hello world'有几个单词，再告诉我现在时间",
    "今天日期加上 365 天是哪天？",
]
```

输出格式参考 Phase 1.5 的 compare_strategies.py，列名加一列 strategy：

```
Query | Strategy       | Done | Steps | Tokens | Latency
------|----------------|------|-------|--------|--------
Q1    | FC             | 3/3  | 1     | 495    | 1172
Q1    | Text           | 3/3  | 1     | 617    | 2593
Q1    | PlanExecute    | ?/3  | ?     | ?      | ?
...
```

把每个 query 的第一次 PlanExecute trace 保存到 `examples/phase2.2/traces/q{idx}_plan_execute.md`。

跑完把对比表 + Q7 的 plan_execute trace 贴给我（**Q7 是关键 case，看 plan-and-execute 能否救回 Text 0/3 这个失败**）。

## 不要做的事

- ❌ 不要做 replan（动态版留到 2.2.2）
- ❌ 不要改 TextReActStrategy 或 FunctionCallingStrategy
- ❌ 不要在 plan 阶段调工具
- ❌ 不要让 Plan-and-Execute 共享 Memory 累积（execute 阶段每次重建 messages）
- ❌ 不要"顺手优化"现有代码

## 完成标准

1. PlanExecuteStrategy 实现完整，3 种 strategy 都能跑 Q1-Q7
2. compare_three_strategies.py 跑通，输出对比矩阵
3. Q7 的 plan_execute trace 完整，能看到 plan 文本 + 每步 execute
4. 原有单元测试全绿，原有 quickstart.py / compare_strategies.py 不受影响

完成后停下，把对比矩阵 + Q7 plan_execute trace 贴给我。