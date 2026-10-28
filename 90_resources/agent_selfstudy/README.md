# LLM / Agent 自学资料包

给中文自学者准备的一套公开学习资料：博客教程、论文、教学代码、公开课课件。
全部资料均为公开可获取版本（arXiv 论文、课程官网课件、公开 GitHub 仓库），不含盗版全文复制；
博客笔记只存原文链接 + 自写中文摘要，符合版权要求。

> 总体积约 360MB（主要是课程课件）。建议按下面的推荐顺序学习。

---

## 📁 目录结构

| 目录 | 内容 | 数量 |
|---|---|---|
| `blogs/` | 高质量 Agent 博客/教程笔记（链接 + 中文摘要） | 9 篇 |
| `papers/` | arXiv 论文 PDF | 8 篇 |
| `code/` | 小而精的开源 agent 实现（已配中文 NOTES） | 5 个仓库 |
| `courses/` | LLM 公开课课件 PDF | 31 份 |

---

## 📰 blogs/ — 博客与教程笔记

每篇笔记包含：标题、作者、发布时间、原文链接、200–400 字中文摘要、「为什么值得读」、
关键代码/仓库出处。不复制原文全文。

**建议阅读顺序**（blogs/README.md 里也有索引表）：

1. `01-lilian-weng-llm-powered-autonomous-agents.md` — Lilian Weng《LLM Powered Autonomous Agents》：Agent 领域的经典综述，规划/记忆/工具三分框架，入门第一站。
2. `09-andrew-ng-agentic-design-patterns.md` — Andrew Ng《Agentic Design Patterns》：Reflection、Tool Use、Planning、Multi-agent 四大设计模式。
3. `02-anthropic-building-effective-agents.md` — Anthropic《Building Effective Agents》：workflow vs agent 的分野，"能用确定性流程就别上 agent"。
4. `03-openai-practical-guide-building-agents.md` — OpenAI《A Practical Guide to Building Agents》：生产级 agent 实战指南。
5. `08-chip-huyen-agents-ai-engineering.md` — Chip Huyen《Agents》（AI Engineering 一章）：工程视角的 agent 设计权衡。
6. `06-demystifying-react-explainer.md` — ReAct 论文工程师视角精读（Thought/Action/Observation 循环）。
7. `07-toolformer-vs-agents-explainer.md` — Toolformer 原理 + 与 agent 路线的辨析。
8. `04-simon-willison-agent-definition-loop.md` — Simon Willison："agent 就是让 LLM 在循环里折腾环境"。
9. `05-simon-willison-lethal-trifecta.md` — Simon Willison：Agent 安全必读，"致命三要素"（prompt injection 防护）。

---

## 📄 papers/ — 论文（arXiv 公开版）

| 文件 | 一句话中文介绍 |
|---|---|
| `Yao2022-ReAct.pdf` | 让 LLM 交替进行"推理（Thought）— 行动（Action）— 观察（Observation）"，开创了 agent 的标准循环范式。 |
| `Schick2023-Toolformer.pdf` | 教 LLM 自己决定何时、如何调用 API 工具（计算器、日历、搜索引擎等），自监督地学会工具使用。 |
| `Packer2023-MemGPT.pdf` | 把操作系统内存分页思想搬进 LLM，用"主存/外存"分层记忆实现无限上下文 agent。 |
| `Shinn2023-Reflexion.pdf` | Agent 做错后用语言写"反思"存入记忆，下次做得更好——试错自改进的代表作。 |
| `Patil2023-Gorilla.pdf` | 专门微调 LLM 来准确调用海量 API（函数名/参数不出错），工具调用准确率的标杆工作。 |
| `Yang2024-SWE-agent.pdf` | 让 agent 在真实终端里修 GitHub issue 的开创性系统，SWE-bench 任务的 agent 范式奠基。 |
| `Xu2023-ReWOO.pdf` | 把"推理规划"和"观察工具结果"解耦：先一次性规划好全部工具调用，再批量执行，省 token 又快。 |
| `Wang2023-Plan-and-Solve.pdf` | 让 LLM 先把任务拆成子计划再逐个执行，比 CoT 更稳的提示策略（PS+ 变体）。 |

> 注：ReWOO 正确的 arXiv ID 是 2305.18323（最初记录的 2305.18351 是另一篇无关数学论文，已纠正）。

---

## 💻 code/ — 公开实现（小而精）

每个仓库根目录都有 `NOTES_zh.md`：实现了什么、核心文件、怎么运行、关键设计点。
（注：本机 git 协议被代理阻塞，仓库用 GitHub 官方 zip 包下载，内容等同于浅 clone，缺 `.git` 目录；
在自己电脑上建议用 `git clone` 重新拉一份。）

| 目录 | 一句话 | 亮点 |
|---|---|---|
| `code/assignment-1/` | CMU 11-768 课程作业 1：手写 ReAct agent harness 修 bug + 下棋 | 最贴合课程的动手作业，含评测 |
| `code/assignment-2/` | CMU 11-768 课程作业 2：数据可视化 agent 的评测/裁判设计 | 学会给 agent 做 eval |
| `code/microagent/` | 零框架极简 ReAct（文本 ReAct / Function Calling 双策略可切换） | 代码极少，自带中文 README |
| `code/smolagents-codeagent-demo/` | 基于 smolagents CodeAgent 的联网调研 demo（217 行单文件） | 看 CodeAgent 怎么让 LLM 写代码当 action |
| `code/deep-research/` | 19.7k stars 的极简 Deep Research agent（TypeScript，<500 行） | 多步调研 agent 的最小完整形态 |

大型框架只记链接（不下载）：[smolagents](https://github.com/huggingface/smolagents)（HuggingFace 轻量 agent 库）、
[LangChain](https://github.com/langchain-ai/langchain)、[OpenHands](https://github.com/All-Hands-AI/OpenHands)、
[AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)。

---

## 🎓 courses/ — 公开课课件（只下 slides）

### CMU 11-711 高级 NLP（Spring 2026）— 23 份
官网：https://cmu-l3.github.io/anlp-spring2026/ ｜ 目录：`courses/anlp-spring2026/`

覆盖：表示学习、自回归 LM、RNN、Attention/Transformer、预训练、Scaling Law、微调、解码算法、
RAG、多模态、评测、RL（两讲）、LM Agent、量化、分布式训练、MoE、长上下文、推理时扩展。
全部 23 讲 slides 均从官网找到并下载。

### Stanford CS336 从零构建语言模型（Spring 2025）— 8 份
官网：https://stanford-cs336.github.io/spring2025/ ｜ 目录：`courses/cs336-spring2025/`

`lecture03-architecture.pdf`（模型架构）、`lecture04-moes.pdf`（MoE）、`lecture05-gpus.pdf`（GPU）、
`lecture07-parallelism.pdf`（并行）、`lecture09-scaling-laws.pdf`、`lecture11-scaling-details.pdf`（Scaling Law）、
`lecture15-rlhf-alignment.pdf`（SFT/RLHF 对齐）、`lecture16-rlvr.pdf`（RL 对齐）。
其余讲次官网只给了 `.py` 代码走读、无 PDF，嘉宾讲座无材料，均已跳过。

### Karpathy《Let's build GPT》（只记链接）
- YouTube 播放列表 "Neural Networks: Zero to Hero"：https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ
  （其中 "Let's build GPT: from scratch, in code" 单集：https://www.youtube.com/watch?v=kCc8FmEb1nY）
- nanoGPT 仓库：https://github.com/karpathy/nanoGPT

---

## 🗺 推荐学习路线

1. **建立 mental model**：先读 blogs 01（Lilian Weng 综述）→ 09（Ng 设计模式）→ 02（Anthropic）。
2. **补 LLM 底子**：看 CS336 课件（架构/训练/对齐）+ CMU 11-711 相关讲次；跟 Karpathy 视频手写 nanoGPT。
3. **读核心论文**：ReAct → Toolformer → Reflexion → MemGPT → SWE-agent（papers/ 按此顺序）。
4. **动手写 agent**：从 `code/microagent/` 的极简 ReAct 开始 → 做 `code/assignment-1/` 作业 →
   跑 `code/deep-research/` 看多步调研 agent。
5. **进阶**：读 blogs 03（OpenAI 实战指南）+ 08（Chip Huyen 工程视角）+ 05（安全），
   再看 Gorilla / ReWOO / Plan-and-Solve 论文，尝试给自己的 agent 加 eval（参考 assignment-2）。

---

## ⚠️ 缺失 / 未覆盖项

- Lecture 1（CMU 11-768）的课件、课程第 5 讲信息、第 8 讲之后的内容（RL 训练、sandboxing 等）当时尚未公开。
- 博客未收录 jalammar 的 ReAct 专篇（未找到对应文章），改用两篇独立博客解读替代。
- `datawhalechina/hello-agents` 中文教程仓库因体积 168MB 超限未收录；可在自己电脑上 clone。
- `code/` 的仓库缺 `.git` 目录（网络原因用 zip 包下载），建议自行 `git clone` 更新。
