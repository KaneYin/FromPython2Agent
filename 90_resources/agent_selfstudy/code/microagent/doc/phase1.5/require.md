# Phase 1.5: LLM I/O Inspection + 多工具 + 失败模式研究

Phase 1 的主循环跑通了，但我们现在要把它从"能跑"打磨到"能讲、能调、能展示"。这一轮**不加新能力**（不要碰长期记忆、规划、Reflection），专心做三件事：

1. **LLM I/O 可观测**：把每次 LLM 调用的完整 request/response 录下来，渲染到 trace
2. **加 2 个工具**：让"工具选择"问题真实存在，方便后续研究多工具行为
3. **失败模式系统性测试**：跑一批边界 case，产出 FAILURE_MODES.md 文档

每件事都按"先实现，再验证，再产出文档"的节奏来。

---

## Part 1: LLM I/O Inspection（核心，先做这个）

### 1.1 在 LLMClient 中加调用录制

`llm.py` 改造：

````python
@dataclass
class LLMCallRecord:
    call_id: str                  # uuid4().hex[:8]
    timestamp: float              # time.time()
    
    # Request
    model: str
    messages: list[dict]          # 完整 messages 数组，原样保存，不做任何加工
    stop: list[str] | None
    temperature: float
    
    # Response
    raw_response: dict            # 完整 LLM 返回 JSON，原样保存
    content: str
    finish_reason: str | None     # 从 raw_response 提取，"stop" / "length" / "stop_sequence" 等
    matched_stop: str | None      # 如果 finish_reason 是 stop_sequence 类，记录匹配到的字符串
    usage: dict                   # {prompt, completion, total}
    
    latency_ms: float
````

`LLMClient` 内部维护一个 `_call_records: list[LLMCallRecord]`，每次 `chat()` 调用后 append。提供两个方法：

- `get_records() -> list[LLMCallRecord]`：返回当前所有记录
- `clear_records()`：清空（Agent 每次 run 开始前调用）

**重要**：
- `raw_response` 和 `messages` 必须原样保存，不要"美化"
- 不要做任何脱敏，这是调试工具不是生产日志
- 不要在 `chat()` 内部 print，所有可视化由 trace 层负责

### 1.2 把 LLMCallRecord 关联到 Trace

`agent.py` 修改：

- Agent 在 `run()` 开始时调 `llm.clear_records()`
- 每次 `llm.chat()` 调用后，把最新一条 `LLMCallRecord` 关联到对应的 `think` 事件
- `TraceEvent.content` 中加一个字段 `llm_call_id`，指向具体的 record
- `Trace` 类持有所有 `LLMCallRecord`：`Trace.llm_calls: list[LLMCallRecord]`

### 1.3 to_markdown() 渲染 LLM I/O

每个 `think` 事件下面，追加一个**可折叠的 LLM I/O 详情区块**，用 markdown 的 `<details>` 标签：

````markdown
## Step 2 — think (prompt=415, completion=76, total=491, 2594ms)
**Thought**: 计算 10 * 2
**Action**: `calculator`
**Action Input**: `{"expression": "10 * 2"}`

<details>
<summary>📤 LLM Request (call_id: a3f9c2)</summary>

**Model**: `deepseek-chat` | **Temperature**: 0.0 | **Stop**: `["Observation:"]`

**Messages** (4 total):

```json
[
  {"role": "system", "content": "..."},
  {"role": "user", "content": "..."},
  {"role": "assistant", "content": "..."},
  {"role": "user", "content": "Observation: 10"}
]
```

</details>

<details>
<summary>📥 LLM Response (call_id: a3f9c2)</summary>

**Finish reason**: `stop` | **Matched stop**: `Observation:`

**Content**:
````
Thought: 计算 10 * 2
Action: calculator
Action Input: {"expression": "10 * 2"}
````

</details>
````

**渲染要求**：
- messages 中的 system content 如果超过 500 字符，可以截断显示（标注 `[truncated, N chars total]`），但完整内容仍要在 trace.to_json() 里
- messages 数组用 `json.dumps(ensure_ascii=False, indent=2)` 输出，保持中文可读
- 不要省略任何 message 条目

### 1.4 加一个 inspect helper

新文件 `microagent/inspect.py`，提供两个工具函数：

````python
def print_call(record: LLMCallRecord, show_messages: bool = True) -> None:
    """终端友好的单次调用打印，用于交互式调试"""
    ...

def diff_messages(prev: list[dict], curr: list[dict]) -> str:
    """对比两次调用的 messages，返回新增部分的可读描述
    
    例如：'+1 assistant message, +1 user observation, system unchanged'
    """
    ...
````

`diff_messages` 第一版不要做字符级 diff，就做条目级别：
- 共同前缀长度
- 新增的条目列表（role + content 前 80 字符）

### 1.5 验证

跑 `examples/quickstart.py`，确认：
- 每个 step 的 markdown 里都有可折叠的 LLM I/O 区块
- messages 数组完整、JSON 合法、中文不乱码
- finish_reason 和 matched_stop 正确填充

完成后停下，告诉我 "Part 1 完成"，**先不要做 Part 2**。

---

## Part 2: 加 2 个工具（让"工具选择"成为真实问题）

### 2.1 加 `text_stats` 工具

`microagent/tools/text_stats.py`：

- 输入：`{"text": str}`
- 功能：返回字符数、词数（中英文混合用简单规则：英文按空格分，中文按字符数）、行数
- 输出格式：`"chars=N, words=N, lines=N"`

### 2.2 加 `datetime_now` 工具

`microagent/tools/datetime_now.py`：

- 输入：`{"timezone": str}`，可选，默认 `"Asia/Shanghai"`
- 功能：返回当前时间
- 输出格式：`"2026-05-20 14:32:18 Asia/Shanghai"`
- 用标准库 `zoneinfo`，不要引入 pytz

### 2.3 注册到 quickstart

`examples/quickstart.py` 注册三个工具：calculator、text_stats、datetime_now。

### 2.4 跑工具选择测试

新建 `examples/test_tool_selection.py`，跑以下 query，记录每个 query 的 trace：

````
queries = [
    "现在几点？",
    "帮我算 sqrt(2) 的近似值",
    "统计这段话的字数：'人工智能正在改变世界'",
    "今天日期加上 365 等于多少？",  # 这个会考察"工具配合"
    "我想知道'hello world'有几个单词，再告诉我现在的时间",  # 多步多工具
    "你好",  # 不该调任何工具
]
````

不写自动断言，**输出每个 query 的：finished、stop_reason、step count、used_tools 列表**。让我人工 review。

完成后停下，告诉我 "Part 2 完成"，把这 6 个 query 的 summary 输出贴给我。

---

## Part 3: 失败模式系统性测试

等 Part 1 和 Part 2 我都 review 过之后再做这一部分。

### 3.1 新建 `examples/failure_modes.py`

跑以下边界 case，每个 case 记录 Agent 行为（不要做自动断言，输出 trace 给我看）：

| ID | Case 描述 | Query / 构造方法 |
|----|----------|------------------|
| F1 | 工具名大小写错误 | 在 system prompt 里加一句让模型故意用 `Calculator`（首字母大写） |
| F2 | Action Input 缺字段 | 模型可能自己产生，构造一个引导性 query 如 "随便算一下"|
| F3 | Action Input 多余字段 | "计算 1+1，并指定精度为 10 位" |
| F4 | 工具返回超长文本 | mock 一个工具返回 5000 字符 |
| F5 | 模型在 Thought 里直接算出答案不调工具 | "算一下 2+2" 这种太简单的 |
| F6 | 模型一次输出两个 Action 块 | 用 mock LLM 强制构造 |
| F7 | 模型输出完全不符合格式 | mock LLM 直接返回 "我觉得答案是 42" |
| F8 | 工具持续报错 | mock 一个永远抛错的工具，看 Agent 几步后会放弃 |
| F9 | 模型自己幻觉 Observation | 测试 stop 参数是否真的生效 |
| F10 | 极长 query（>2000 字符）| 看上下文膨胀 |

每个 case 涉及 mock LLM 的，用一个简单的 `ScriptedLLM` 类（按预设序列返回固定响应）。

### 3.2 产出 docs/FAILURE_MODES.md

模板：

````markdown
# Agent Failure Modes Study

This document records edge-case behaviors of MicroAgent observed during Phase 1.5 testing.

## F1: Tool name case mismatch

**Setup**: ...
**Query**: ...
**Expected behavior**: ...
**Actual behavior**: ...
**Verdict**: ✅ Handled gracefully / ⚠️ Suboptimal / ❌ Broken
**Notes**: ...

---

## F2: ...
````

每个 case 都要填，Verdict 用三档：
- ✅ 处理优雅（错误反馈、重试、合理放弃）
- ⚠️ 能跑但行为可改进
- ❌ 真的崩了或死循环

**这份文档是 Phase 1.5 最重要的产出，比代码本身更值钱**。它证明你不是"跑通就 ok"，而是真的研究过 Agent 的失败边界。

完成后告诉我 "Part 3 完成"，把 FAILURE_MODES.md 贴给我，**先别写 DESIGN_NOTES.md**——我看完失败模式之后，咱俩一起讨论设计决策，再写 DESIGN_NOTES。

---

## 不要做的事

- ❌ 不要加新功能（长期记忆、规划、Reflection、新解析格式都不要碰）
- ❌ 不要重构现有目录
- ❌ 不要"顺手优化"任何看起来不爽但没列在上面的事
- ❌ 不要写流式
- ❌ 不要引入新依赖（除非确实需要 zoneinfo 之外的东西，先问我）

---

## 现在开始 Part 1

确认理解后开始 Part 1（LLM I/O Inspection），完成后停下等我 review。