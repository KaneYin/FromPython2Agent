# LLM Powered Autonomous Agents

- **作者**：Lilian Weng（OpenAI）
- **发布时间**：2023 年 6 月 23 日
- **原文链接**：https://lilianweng.github.io/posts/2023-06-23-agent/
- **类型**：技术综述博客

## 中文摘要

这是 Agent 领域被引用最多的一篇综述长文，几乎定义了后来所有讨论 Agent 的话语体系。核心框架是：以 LLM 为"大脑"的自主 Agent 系统由三大组件构成——**规划（Planning）**、**记忆（Memory）**、**工具使用（Tool Use）**。规划部分系统梳理了任务分解（CoT、Tree of Thoughts、LLM+P 外包给经典规划器）与自我反思（ReAct 的 Thought/Action/Observation 循环、Reflexion 的试错反思、Chain of Hindsight、Algorithm Distillation）两条技术线；记忆部分将人类记忆类比映射到 Agent 上（感觉记忆→embedding、短期记忆→上下文窗口、长期记忆→外部向量库），并讲解了 MIPS 检索与 LSH、ANNOY、HNSW 等近似最近邻算法；工具部分则覆盖了 HuggingGPT、API-Bank 等早期工作。文章写于 AutoGPT、GPT-Engineer、BabyAGI 爆火之时，既是对热潮的冷静梳理，也给出了清晰的组件化 mental model，至今仍是入门 Agent 的第一站。

## 为什么值得读

"Planning + Memory + Tools" 这个三分法已成为行业标准术语，读完它再看 Anthropic、OpenAI 的官方指南会顺畅得多；每个技术点都附带原始论文链接，是一份极佳的文献地图；篇幅虽长但结构清晰，适合作为自学路线的总纲。

## 代码 / 仓库出处

- 文中提到的概念验证项目均链接至其 GitHub 仓库：**AutoGPT**、**GPT-Engineer**、**BabyAGI**（原文正文内链）。
- 含 ReAct 的 `Thought / Action / Observation` 提示模板示例（文本示例，非代码库）。
- 未提供可运行的完整代码，定位是综述而非教程。
