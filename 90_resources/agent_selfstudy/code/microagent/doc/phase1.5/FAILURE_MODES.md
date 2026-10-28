# Failure Modes: MicroAgent 边界研究档案

## 文档说明

这是 MicroAgent 项目的 Agent 边界研究记录。记录的不是 bug，而是 Agent 在特定条件下可复现的异常行为模式及其真实根因。每条记录区分"第一直觉"和"真实根因"，体现调试深度。

**这不是**：bug tracker、功能测试报告、模型评测榜单。

**失败分类层级**：

| 层级 | 定义 | 示例 |
|------|------|------|
| 环境层 | 运行时依赖、操作系统差异、网络问题 | 缺少 tzdata 包 |
| 工具层 | 工具实现缺陷、schema 定义不当、参数边界 | 参数校验遗漏 |
| Prompt 层 | 提示词设计导致的模型行为偏差 | 格式约束过强/过弱 |
| 模型层 | LLM 本身的能力边界或 quirks | 非标准 JSON 输出 |
| 框架层 | MicroAgent 自身的架构限制 | 不支持并行 tool calling |

**测试环境基线**：
- LLM：vLLM 部署的 MiniMax 2.5（minimax-2.5-proxy）
- 测试脚本：`examples/compare_strategies.py`，每个 query 跑 3 次
- OS：Windows 11，Python 3.12.13
- 运行日期：2026-05-21

---

## Failure 分类总览

| ID | 标题 | Category | Affected Strategy | Severity | Status |
|----|------|----------|-------------------|----------|--------|
| F01 | Windows 缺 tzdata 导致 datetime_now 全部失败 | 环境层 | Both | High | Fixed |
| F03 | 复合日期推理失败 | 模型层 + 工具层 | Both | Medium | Known limitation |
| F04 | Text 模式多工具场景 step 数不稳定 | Prompt 层 | Text | Medium | Known limitation |
| F05 | FC 模式收到多个 tool_calls 仅执行第一个 | 框架层 | FC | Low | Design choice |

---

## F01: Windows 缺 tzdata 导致 datetime_now 工具全部失败

**Category**: 环境层
**Affected Strategy**: Both
**Discovered**: 2026-05-21, `examples/compare_strategies.py` Q4
**Severity**: High
**Status**: Fixed

### 现象

Query "现在几点？"，3 次运行结果：FC 1/3 通过、Text 0/3 通过。FC 唯一成功的那次是模型放弃工具直接用自身知识回答。每次工具调用都返回 `ZoneInfoNotFoundError`，模型尝试了 `Asia/Shanghai`、`UTC`、`America/New_York` 三种时区全部失败，最终耗尽 step 上限。

### 第一直觉（错误判断）

怀疑 function calling 对零参数 / 全可选参数工具支持差，或者模型不会正确调用 datetime_now。

### 真实根因

Windows 上的 `zoneinfo` 模块依赖 `tzdata` 包才能解析 IANA 时区名。项目环境未安装此包，导致 `ZoneInfo("Asia/Shanghai")`、`ZoneInfo("UTC")` 全部抛 `ZoneInfoNotFoundError`。模型的工具调用本身是正确的（先试默认时区、再试 UTC、再试美东），重试逻辑合理，只是工具执行层始终报错。

Trace 证据（`examples/traces/q4_FunctionCallingStrategy.md`）：
```
Step 1 — observation: Error: ZoneInfoNotFoundError: 'No time zone found with key Asia/Shanghai'
Step 2 — observation: Error: ZoneInfoNotFoundError: 'No time zone found with key UTC'
Step 3 — observation: Error: ZoneInfoNotFoundError: 'No time zone found with key America/New_York'
```

### 修复

`pyproject.toml` 添加条件依赖：`tzdata; sys_platform == 'win32'`。安装后三个时区全部正常返回。

### 工程教训

1. Trace 必须包含工具的真实返回值——如果没有 observation 里的 `ZoneInfoNotFoundError`，这个问题会定位成"模型不会调工具"。
2. "模型重试" 不等于 "模型不会"。模型在反复尝试不同时区是合理的错误恢复行为。
3. Windows + `zoneinfo` 是已知陷阱，必须显式声明 tzdata 依赖。

### 相关 Trace

- `examples/traces/q4_FunctionCallingStrategy.md`
- `examples/traces/q4_TextReActStrategy.md`

---

## F03: 复合日期推理失败（"今天日期加 365 天"）

**Category**: 模型层 + 工具层
**Affected Strategy**: Both（FC 2/3, Text 0/3）
**Discovered**: 2026-05-21, `examples/compare_strategies.py` Q7
**Severity**: Medium
**Status**: Known limitation

### 现象

Query "今天日期加上 365 天是哪天？"，3 次运行：FC 2/3 通过（steps 6-10），Text 0/3 通过（steps 恒为 10，撞 max_steps）。FC 的成功也极不稳定，token 消耗在 4133-7928 之间波动。

### 第一直觉（错误判断）

假设 text ReAct 的显式 CoT（Thought 段）在复合推理场景下应该比 FC 更可靠，因为模型能"看到"自己的推理过程。

### 真实根因

工具集不完备——项目有 `datetime_now`（获取当前时间）和 `calculator`（数学计算），但没有日期算术工具（如 `date_add`）。模型需要自己编排两步工具调用（获取日期 -> 计算加法），但"当前日期"的格式（`2026-05-21`）和"365 天加法"之间的转换没有工具支撑，模型需要在大脑里完成格式拆解和日历计算。

Text 模式在这个场景下表现更差，不是因为 CoT 无效，而是 text ReAct 的格式约束（每步必须输出 Thought + Action + Action Input）在模型不确定该调用什么工具时增加了认知负担——模型会花更多 step 在"思考该用什么工具"上，加速消耗 step 预算。

### 修复 / 当前处理

未修。这是工具集完备度问题，不是策略问题。Phase 2 计划补充日期算术工具。

### 工程教训

1. Agent 能力上限 = 推理能力 x 工具集完备度。推理再强，缺工具就是缺工具。
2. FC 在工具集不完备时比 Text 更鲁棒——因为 FC 没有 Thought 段的格式开销，模型可以把 step 预算用在更多试错上。
3. 复合推理的不稳定性（steps 6-10）是模型层问题，框架层无法消除。

### 相关 Trace

- `examples/traces/q7_FunctionCallingStrategy.md`
- `examples/traces/q7_TextReActStrategy.md`

---

## F04: Text 模式多工具场景 step 数不稳定

**Category**: Prompt 层
**Affected Strategy**: Text only
**Discovered**: 2026-05-21, `examples/compare_strategies.py` Q6
**Severity**: Medium
**Status**: Known limitation

### 现象

Query "统计'hello world'有几个单词，再告诉我现在时间"，3 次运行：Text 模式 steps 在 2-5 之间漂移，tokens 1463-3678，latency 8563-19188ms。同条件 FC 模式稳定在 2 steps、tokens 1206-1215、latency 6110-6516ms。

### 第一直觉（错误判断）

怀疑模型在多工具组合下"想多了"——规划能力不足导致不必要的中间步骤。

### 真实根因

Text ReAct 的 prompt 模板没有显式指导多工具场景的策略。当前 prompt 只说"Output ONE Thought + Action + Action Input per turn"，但没有说"如果任务明确需要多个工具，可以紧凑地逐步调用"。模型在 Thought 阶段会尝试规划，有时直接行动（2 steps），有时先思考再行动（3-5 steps），收敛速度取决于模型对 prompt 的理解。

FC 模式天然不受此影响，因为 function calling 协议不要求模型在调用工具前输出文本推理。

### 修复 / 当前处理

未修。这是 prompt 设计的权衡点：加强约束（如"直接调用，不要过度思考"）可能在简单场景提速，但会损害复杂推理任务的表现。当前保持弱约束。

### 工程教训

1. Prompt 工程的"约束强度"是连续光谱，没有一刀切答案。
2. 多工具场景的 step 不稳定是 text ReAct 范式的结构性弱点，不是 bug。
3. FC 模式在此场景的优势来自协议层面——不是"更好"，而是"约束更少"。

### 相关 Trace

- `examples/traces/q6_TextReActStrategy.md`
- `examples/traces/q6_FunctionCallingStrategy.md`

---

## F05: FC 模式收到多个 tool_calls，框架仅执行第一个

**Category**: 框架层
**Affected Strategy**: FC only
**Discovered**: 2026-05-21, `examples/compare_strategies.py` Q6
**Severity**: Low
**Status**: Design choice（Phase 2 计划支持串行全执行）

### 现象

Q6 "统计单词+时间"的 FC 运行中，MiniMax 在单次响应中返回 2 个 tool_calls（text_stats + datetime_now）。框架打印 Warning "Got 2 tool_calls, executing only the first"，仅执行第一个工具调用，丢弃第二个。后续 step 再调用第二个工具，最终结果正确但多花了 1 步。

### 第一直觉（错误判断）

怀疑模型行为不符合协议——一次不该返回多个 tool_calls。

### 真实根因

Parallel tool calling 是 OpenAI Chat Completions API 的合法行为。MiniMax 正确识别了两个独立子任务并尝试并行调用。这是 Phase 1.5 框架主动的设计选择：串行实现优先，只取 `tool_calls[0]`。框架行为与设计一致，只是能力滞后于模型能力。

### 修复 / 当前处理

Phase 2 计划串行执行所有 tool_calls（遍历列表而非只取第一个）。Phase 3 计划支持真正的并行执行。

### 工程教训

1. 框架能力滞后于模型能力是常态。关键是让滞后可观测——Warning 日志比静默丢弃好。
2. 并行 tool calling 是真实场景需求，不是边缘 case。
3. 框架架构应该"接受但不崩溃"，而非"拒绝并报错"。

### 相关 Trace

- `examples/traces/q6_FunctionCallingStrategy.md`

---

## Appendix A: tools schema 的隐性 token 成本

### 实验设计

同一 query（"你好"），同一 model，仅变量为是否携带 tools 参数。tools 包含 3 个工具（calculator / text_stats / datetime_now）的完整 JSON schema。

### 数据

| 条件 | prompt_tokens | completion_tokens | total |
|------|:---:|:---:|:---:|
| 无 tools | 24 | 29 | 53 |
| 带 3 tools | 306 | 27 | 333 |
| **Delta** | **+282** | -2 | **+280** |

### 结论

1. tools schema **每次 LLM 调用**都作为 prompt 的一部分提交并计费，不是"只出现一次"。多轮对话中，schema 在每一轮的 prompt_tokens 中都存在。
2. FC 模式节省总 token 的主因是 **completion 更紧凑 + 步数往往更少**，不是 schema 摊销。
3. FC 的优势带域是"工具调用次数少但每次节省多"。在超长对话 / 极多轮工具调用场景下，schema 的重复成本可能反超 completion 的节省，需要按具体场景评估。
4. Text ReAct 的 system prompt（工具描述 + 格式说明 + 规则）同样每轮重复，但通常比 tools schema 短。两者都是固定成本，差异在绝对值。
