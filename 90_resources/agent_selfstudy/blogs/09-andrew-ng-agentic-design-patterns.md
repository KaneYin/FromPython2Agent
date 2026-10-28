# Agentic Design Patterns（The Batch 第 242 期：Reflection 篇）

- **作者**：Andrew Ng（DeepLearning.AI《The Batch》通讯）
- **发布时间**：2024 年 3 月（第 242 期）
- **原文链接**：https://www.deeplearning.ai/the-batch/issue-242/
- **类型**：行业通讯 / 设计模式导论

## 中文摘要

Andrew Ng 在 2024 年初提出了一个极具预见性的判断：**AI agent workflows 将在当年带来比下一代基础模型更大的 AI 进展**，并归纳出四种 agentic 设计模式——Reflection（反思）、Tool use（工具使用）、Planning（规划）、Multi-agent collaboration（多智能体协作）。本期聚焦第一种模式 **Reflection**：核心思想是把"人给 LLM 提批评意见再让它改"这个日常动作自动化——先让模型生成初版输出，再 prompt 它自我批判（检查代码的正确性、风格、效率），然后带着批评意见重写，循环往复；还可以引入外部评估工具（如跑单元测试、用网页搜索核验事实）让反思有据可依；更进一步可以用双 Agent 实现（一个生成、一个专职挑刺），两者讨论出更高质量的结果。Ng 特别指出，反思是实现成本最低、但在他的应用中带来"惊人性能提升"的模式，并推荐了 Self-Refine、Reflexion、CRITIC 三篇论文作为深入阅读。他还顺带提出用 "agentic" 作形容词来终结"什么才算真 agent"的无谓争论——系统可以有不同程度的 agentic。

## 为什么值得读

这是把"agentic workflow"概念推向主流的源头文章之一，四模式分类（反思/工具/规划/多智能体）至今仍被广泛引用；Reflection 模式是性价比最高的入门实践，读完可直接动手做"生成-批判-重写"循环；Ng 的写作面向所有 AI 从业者而非论文读者，语言平实，适合作为自学路线的"信心建立"读物。

## 代码 / 仓库出处

- 无配套代码仓库，通讯文章定位。
- 推荐的三篇论文（原文内链至 arXiv）：Self-Refine（Madaan et al. 2023）、Reflexion（Shinn et al. 2023）、CRITIC（Gou et al. 2024）。
- DeepLearning.AI 同期配套短课程见 learn.deeplearning.ai（如 "AI Agentic Design Patterns with AutoGen"）。
