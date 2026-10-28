# Phase 1 收尾修复

Phase 1 主循环跑通了，但有几个细节问题需要在进入 Phase 2 之前修干净。**这一轮只做修复 + 补测试，不要新增任何功能。**

## 修复清单

### 1. Trace 中所有结构化字段统一用 JSON 序列化

**问题**：现在 `to_markdown()` 输出的 Action Input 是 `{'expression': '123 * 456'}`（Python dict 的 repr，单引号），不是合法 JSON。

**要求**：
- `trace.py` 中所有涉及 dict 输出的地方，统一用 `json.dumps(obj, ensure_ascii=False)`
- 特别是 Action Input、observation（如果是结构化数据的话）、to_json() 输出
- 中文不要被转义成 `\uXXXX`

### 2. Token 统计口径统一

**问题**：每步显示的 tokens 和 summary 总 tokens 对不上（例：410+458=868 但总数 1326）。原因是混用了 prompt_tokens / completion_tokens / total_tokens。

**要求**：
- `TraceEvent.tokens` 字段明确为 `{"prompt": int, "completion": int, "total": int}` 三个值
- `to_markdown()` 中每步显示格式改为：`(prompt=410, completion=48, total=458, 2125ms)`
- `Trace.summary()` 中的 `total_tokens` 等于所有 think 事件的 `tokens["total"]` 之和
- 只在 `think` 事件上记 tokens，`final` / `action` / `observation` 事件的 tokens 字段为 None

### 3. think 和 final 事件归类调整

**问题**：现在同一次 LLM 调用，既产生 think 事件又产生 final 事件，两个事件显示同样的 tokens/latency，重复且误导。

**要求**：
- 改为：每次 LLM 调用只产生**一个** `think` 事件，带完整的 tokens 和 latency
- `final` 事件类型保留，但只记录 `{"answer": str}`，不带 tokens / latency（None）
- `action` 事件同理，不带 tokens / latency
- `to_markdown()` 中 final 事件渲染时不再显示 tokens 和 latency

### 4. 修复完以上三点后，跑两个之前漏掉的验收 case

写一个 `examples/test_edge_cases.py`，跑以下两个 case 并打印 trace：

**Case A：错误恢复**
```python
agent.run("帮我算 sqrt(-1)，告诉我结果")
```
预期：calculator 返回 error，Agent 读到后应该 reason 出"这是虚数 / 无法计算"并给出合理的 Final Answer，而不是死循环或崩溃。

**Case B：max_steps 优雅停止**
```python
# 构造 budget，max_steps=2
budget = Budget(max_steps=2)
agent = Agent(llm=..., tools=..., budget=budget)
agent.run("先算 5+5，再算结果乘 2，再算结果减 3，再算结果除以 2")
```
预期：跑满 2 步后停止，`AgentResult.finished=False`，`stop_reason="max_steps"`（或类似的明确字符串），trace 末尾有 `budget_exceeded` 事件。

### 5. 检查 stop_reason 的取值是否规范

现在 `AgentResult.stop_reason` 见到的有 `"final_answer"`。要求统一为以下枚举值之一（用字符串字面量即可，不需要 Enum）：
- `"final_answer"` —— 正常完成
- `"max_steps"` —— 步数超限
- `"max_tokens"` —— token 超限（如果 budget 配了）
- `"error"` —— 其他异常（这一版可能用不到，先留着）

在 `agent.py` 顶部用注释列出这几个常量值，方便后续维护。

---

## 不要做的事

- ❌ 不要重构现有目录结构
- ❌ 不要新增工具
- ❌ 不要改 prompt 模板
- ❌ 不要加 retry / 流式 / 异步
- ❌ 不要"顺手优化"任何看起来不爽但没列在上面的地方，先问我

---

## 完成标准

1. 跑原来的 `quickstart.py`，trace 输出格式更清晰，Action Input 是合法 JSON，token 数对得上
2. 跑新增的 `test_edge_cases.py`，两个 case 都符合预期，把 trace 输出贴给我
3. 原有的所有单元测试仍然通过（`pytest tests/` 全绿）
