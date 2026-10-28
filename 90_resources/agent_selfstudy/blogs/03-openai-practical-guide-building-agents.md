# A Practical Guide to Building Agents

- **作者**：OpenAI
- **发布时间**：2025 年 3 月
- **原文链接**：https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/
- **类型**：官方指南（另有 30+ 页 PDF 版：cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf）

## 中文摘要

OpenAI 把来自真实客户部署的经验提炼成一份面向产品与工程团队的实战手册。开篇先给 Agent 下操作性定义：**用 LLM 管理工作流执行、在护栏内动态选择工具、能独立完成任务的系统**——并明确把简单聊天机器人、单轮 LLM 调用排除在外。接着回答"何时值得造 Agent"：复杂判断型决策、规则已臃肿到难以维护、重度依赖非结构化数据，三者都不沾就别用 Agent。设计基础归纳为三支柱：**模型**（先用最强模型建 baseline，再按需换小模型降本）、**工具**（数据型/动作型/编排型三类，工具本身也要标准化、可复用）、**指令**（用现有 SOP 文档生成、步骤原子化、预判 edge case）。编排部分对比单 Agent 循环与多 Agent 的两种形态——Manager 模式（中央 Agent 把子 Agent 当工具调用）与去中心化 handoff，并给出拆分时机：优先把单个 Agent 做强，只在逻辑过于复杂或工具互相干扰时才拆。最后是七类 guardrails 的纵深防御思路。

## 为什么值得读

与 Anthropic 的文章形成完美互补：Anthropic 讲"模式分类"，OpenAI 讲"从 0 到 1 的决策流程"（要不要做、用什么模型、怎么拆、怎么防翻车）；官方出品意味着术语和最佳实践与自家 Agents SDK / Responses API 对齐，动手时可直接套用。

## 代码 / 仓库出处

- 指南中的代码示例基于 **OpenAI Agents SDK**（代码优先、非声明式的编排方式；官方文档与示例仓库见 OpenAI 开发者站点）。
- 无独立教程仓库，定位是设计指南而非手把手 coding 教程。
