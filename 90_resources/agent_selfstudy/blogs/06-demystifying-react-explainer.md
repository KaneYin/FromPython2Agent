# Demystifying ReAct: Why Reasoning and Acting is the Standard for LLM Agents

- **作者**：4484ho（DEV Community 独立作者，LangChain 学习笔记系列）
- **发布时间**：2026 年初
- **原文链接**：https://dev.to/4484ho/demystifying-react-why-reasoning-and-acting-is-the-standard-for-llm-agents-1ii6
- **类型**：论文精读 / 原理解读（ReAct: Synergizing Reasoning and Acting in Language Models, Yao et al.）

## 中文摘要

这是一篇罕见的"工程师视角" ReAct 论文精读，作者在学习 LangChain 时发现 ReAct 已被框架封装成黑盒，于是回头把原论文逐节拆开。文章先指出 ReAct 要解决的核心矛盾：纯推理（CoT）会因缺乏外部知识而产生事实错误、纯行动（action-only）则会因缺少抽象目标而漫游，把二者融合成 Thought→Action→Observation 的循环，就同时获得了可纠错的推理与有方向的行动。接着用形式化语言重述了论文机制：环境被建模为类 MDP 的 (state, action, observation)，上下文 c(t) 是历史轨迹的拼接，模型在每一步采样生成 thought 或 action。实验部分覆盖知识密集型任务（HotpotQA、FEVER，用 Wikipedia API 做 Search/Lookup/Finish）与决策任务（ALFWorld、WebShop），结论是 ReAct 兼具 CoT 的推理能力与行动效率，还能自我纠正幻觉。最有价值的是后半部分原创整理：把 Observation 的落地实现拆成"数据接收序列化→拼接到上下文→token 预算控制→触发下一轮推理"四步，并总结出 ReAct 循环的三个工程特性——同步性、token 成本随步数累积、以及 observation 与预期不符时触发的递归式动态重规划。

## 为什么值得读

多数 ReAct 解读停留在"Thought/Action/Observation 三段式"的口号层，这篇深入到"observation 到底在代码里是什么"——一次外部工具返回是如何被序列化、拼进上下文、触发下一次调用的；CoT（闭系统）vs ReAct（开系统）的对比框架非常清晰；公式与工程细节兼备，适合在读完 Lilian Weng 综述后作为 ReAct 专题深挖。

## 代码 / 仓库出处

- 无配套代码仓库，定位是论文解读。
- 原论文：ReAct: Synergizing Reasoning and Acting in Language Models（Shunyu Yao et al.，arXiv，原文内链）。
- 相关实验环境提及：HotpotQA、FEVER、ALFWorld、WebShop（均为公开 benchmark）。
