# Toolformer vs Agents: A Deep Learning Perspective

- **作者**：Rashmi（Medium 独立作者）
- **发布时间**：2026 年 1 月
- **原文链接**：https://medium.com/@rashmi18patel/toolformer-vs-agents-a-deep-learning-perspective-e1f60af29694
- **类型**：论文解读 / 概念辨析（Toolformer: Language Models Can Teach Themselves to Use Tools, Schick et al. 2023）

## 中文摘要

文章从深度学习视角厘清了"让 LLM 用工具"的两种根本不同路线。**Toolformer 路线**是"把工具使用学进网络内部"：模型在普通文本中插入候选 API 调用（如计算器、搜索引擎、翻译、日历、问答系统），真实执行这些调用，再用"是否降低了后续 token 的预测 loss"这个自监督信号做过滤，只保留真正有帮助的调用去微调模型。于是模型自己学会了"何时调用、调用哪个、如何整合返回结果"，且不需要人类标注工具使用数据——6.7B 的 GPT-J 学会用工具后，在多个 zero-shot 任务上超过了大得多的 GPT-3。**Agent 路线**则是"把工具使用编排在网络外部"：planner/router/executor 等控制逻辑通过 prompt、多步循环、记忆来决定何时调工具（如 ReAct）。作者强调两者互补而非对立：Toolformer 是 learned-and-static（学进权重、单次非交互调用），ReAct 是 prompted-and-interactive（prompt 驱动、可观察可循环）；而今天的 function calling / tool calling API 实际上同时借鉴了两边——Toolformer 式的"何时调用"的学习直觉，加上 ReAct 式的交互循环，再由 LLMCompiler 这类编排层做调度并行化。

## 为什么值得读

中文社区对 Toolformer 的讨论远少于 ReAct，但理解"工具能力可以被训练进权重"对把握现代模型 tool calling 的由来至关重要；这篇把"模型内学习 vs 系统外编排"的设计空间讲得非常干净，22 分钟篇幅但信息密度高，读完会对整个工具使用技术版图有立体认知。

## 代码 / 仓库出处

- 无配套代码仓库，定位是论文解读。
- 原论文：Toolformer: Language Models Can Teach Themselves to Use Tools（Timo Schick et al., arXiv:2302.04761，原文内链）。
- 文中以 `<CALL:Calculator("2+2")>` / `<RESULT:4>` 这类示意格式说明工具调用 token 的嵌入方式（示意，非真实代码）。
