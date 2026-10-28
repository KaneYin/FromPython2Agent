# Phase 2.1: 并行 Tool Calling 支持

Phase 1.5 留下的 F05：FC strategy 收到多个 tool_calls 时只执行第一个，warning 日志记录。Phase 2.1 把这个债还了。

## 目标

让 Agent 在单次 LLM 响应返回多个 tool_calls 时，**串行执行全部**，并把每个工具的 observation 都喂回模型。

明确不做的：
- 不做真·并行（ThreadPoolExecutor 之类），那是 Phase 3 的事
- 不改 Tool / Strategy / Memory 的对外接口
- 不动 TextReActStrategy（它天然单工具）

## 实现要点

### 1. agent.py 主循环改造

当前逻辑（伪代码）：
```python
if len(parsed.tool_calls) > 1:
    log.warning("...executing only the first")
tc = parsed.tool_calls[0]
observation = registry.get(tc.name).invoke(**tc.arguments)
memory.add_raw(strategy.format_observation_message(observation, tc))
trace.record_action(...)
```

改为：
```python
for tc in parsed.tool_calls:
    if tc.name not in registry:
        observation = f"Error: tool '{tc.name}' not found"
    else:
        observation = registry.get(tc.name).invoke(**tc.arguments)
    memory.add_raw(strategy.format_observation_message(observation, tc))
    trace.record_action(step, tc.name, tc.arguments, observation, tool_call_id=tc.call_id)
```

**关键点**：
- 一个 LLM step 内执行 N 个 tool_calls，trace 上算**一个 think 事件 + N 个 action 事件**
- budget.consume_step() 仍然只在 think 那一层调用一次，**不要每个 tool_call 算一步**
- 如果某个 tool 抛错（被 Tool.invoke 包成 error 字符串），不影响后续 tool_call 执行

### 2. Memory 顺序的协议正确性

OpenAI 协议要求：assistant message 带 N 个 tool_calls 时，后续必须紧跟 N 个 role="tool" 的 message，**tool_call_id 一一对应**。你的实现要保证：

- assistant message 一次性 add（包含所有 tool_calls）—— Phase 1.5 已经这么做了
- 紧接着 for 循环 add N 个 tool observation message，顺序与 tool_calls 一致
- 中间不能插入其他 message

写一个 `_validate_message_sequence` 内部方法，在 debug 模式下检查 memory 的协议合规性（生产模式跳过）。

### 3. Trace 渲染

`to_markdown()` 在同一 step 下渲染多个 action：

```
## Step 2 — think (...)
**Thought**: ...
**Tool Calls**: 2

### Step 2 — action #1
**Tool**: text_stats
**Input**: {...}
**Observation**: ...

### Step 2 — action #2
**Tool**: datetime_now
**Input**: {...}
**Observation**: ...
```

### 4. 验证

新建 `examples/test_parallel_tools.py`：

跑 Q6（"统计'hello world'有几个单词，再告诉我现在时间"）3 次，对比 Phase 1.5 数据：

| 指标 | Phase 1.5 | Phase 2.1 期望 |
|------|-----------|----------------|
| Steps | 2 | **1** |
| Tokens | ~1210 | 应略降 |
| Tool calls 执行数 | 1（丢 1）| 2（全执行）|
| Final answer 正确性 | 正确 | 正确 |

如果 step 数没从 2 降到 1，说明 MiniMax 这次没并行返回——这是模型行为差异，不是 bug，把现象记下来。

把 trace markdown 贴给我。

## 不要做的事

- ❌ 不要改 ToolRegistry / Tool 接口
- ❌ 不要做 async / thread pool
- ❌ 不要碰 TextReActStrategy
- ❌ 不要"顺手"加新工具

完成后停下，贴 Q6 的新 trace + 与 Phase 1.5 的对比数据。