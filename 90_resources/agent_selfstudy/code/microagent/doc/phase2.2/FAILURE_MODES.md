## F07: PlanExecute 对不需工具的任务过度规划

Q1 "你好，介绍一下你自己" 在 PlanExecute 下生成 6-10 步计划，消耗 4888 tokens（FC 仅需 846）。
**根因**：Plan prompt 未指导"trivial 任务应生成单步 plan"。范式的结构性弱点：所有任务都被当作多步问题处理。
**Mitigation**: Plan prompt 加一条 "If the task can be answered without tools, generate exactly one step: 'Answer the user directly'"

## F08: MiniMax 在 Text ReAct 模式下混输私有工具调用格式
**Category**: 模型层
**Affected Strategy**: Text only（FC 不受影响，因为工具调用走 API 协议）
**现象**：Q6 多工具场景下，MiniMax 在标准 Action/Action Input 后额外输出 <minimax:tool_call> 私有格式。第二步完全只输出私有格式，parser 找不到 Action 或 Final Answer，datetime_now 工具从未被实际调用。
**教训**：国产模型普遍存在私有格式污染问题。Text ReAct 的 parser 对此零容忍，FC strategy 因格式由 API 协议保证而天然免疫。这是 FC 在国产模型上比 Text ReAct 更可靠的核心原因之一。
**缓解方案**：parser 加一步预处理，剥离 <minimax:tool_call>...</minimax:tool_call> 块后再做正则匹配。但这是治标——根本上，对 MiniMax 建议优先使用 FC strategy。