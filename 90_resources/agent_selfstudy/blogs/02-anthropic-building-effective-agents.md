# Building Effective Agents

- **作者**：Erik Schluntz、Barry Zhang（Anthropic）
- **发布时间**：2024 年 12 月
- **原文链接**：https://www.anthropic.com/research/building-effective-agents
- **类型**：官方工程实践指南

## 中文摘要

Anthropic 基于与数十个客户团队共建 Agent 的一手经验，提出了一个反直觉但极具影响力的结论：**最成功的落地案例用的不是复杂框架，而是简单、可组合的模式**。文章首先划清关键概念：workflows（LLM 与工具按预定义代码路径编排）vs agents（LLM 自主决定流程与工具使用），并给出"何时用/何时不用"的判断标准——优先最简方案，只在收益明确时增加复杂度。接着从简到繁列出七种常见模式：augmented LLM、prompt chaining、routing、parallelization、orchestrator-workers、evaluator-optimizer，以及完全自主的 agents，每种都配了适用场景与实例。最后给出三条核心原则：保持设计简单、让规划步骤透明、精心设计工具文档与测试（ACI）。附录还讨论了客服与编程两个真实落地场景，以及如何为 Agent 写好工具。

## 为什么值得读

这是从"论文/博客"走向"生产"的分水岭文章，直接塑造了 2025 年 Agent 工程的主流话语；它的模式分类（routing、orchestrator-workers 等）被无数教程引用；对框架的克制态度（建议先直接调 LLM API，理解底层再考虑框架）能帮自学者避开"学框架而非学原理"的坑。

## 代码 / 仓库出处

- 文中提到 Anthropic 官方 **cookbook**（platform.claude.com）中有各模式的示例实现。
- 以自家实现为例：SWE-bench 编程 Agent、"computer use" 参考实现（原文链接至 GitHub）。
- 提及的第三方框架：Claude Agent SDK、Strands Agents SDK（strandsagents.com）、Rivet、Vellum——仅作点评，未深入。
