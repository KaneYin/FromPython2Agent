# FromPython2Agent · 学习资料总索引

从 Python 到 Agent 的学习工作区，包含个人练习、独立 Demo、课程资料和开源参考实现。

仓库入口见 [README](README.md)，目录与环境约定见 [仓库指南](docs/REPOSITORY_GUIDE.md)，当前实现状态与已验证问题见 [代码 Review](docs/CODE_REVIEW.md)。下文保留原有的主题资源索引；课程信息描述的是归档时的资料，未在本次整理中重新核验外部网站。

## 个人练习与 Demo

主线顺序为 `00_python_basics → 01_machine_learning → 02_deep_learning → 03_llm → 04_rag → 05_agents`。机器学习与深度学习阶段目前只有说明文件，为后续实现预留位置；课程和参考资料统一放在 `90_resources/`。

| 目录 | 内容与状态 |
|---|---|
| [00_python_basics/](00_python_basics/README.md) | Python 基础笔记与未完全完成的字符串练习 |
| [01_machine_learning/](01_machine_learning/README.md) | 为后续机器学习实现预留，尚未添加实现 |
| [02_deep_learning/](02_deep_learning/README.md) | 为后续深度学习实现预留，尚未添加实现 |
| [03_llm/01_minimal_chat/](03_llm/01_minimal_chat/README.md) | 直接调用模型的示例，以及仍有导入和运行问题的抽象层草稿 |
| [03_llm/02_transformer_from_scratch/](03_llm/02_transformer_from_scratch/README.md) | Transformer 学习 Notebook，实现部分未完成 |
| [04_rag/01_basic_rag/](04_rag/01_basic_rag/README.md) | 基于 Ollama 的 RAG Demo，模拟服务响应的完整流程检查通过 |
| [05_agents/01_agent_loop/](05_agents/01_agent_loop/README.md) | 工具调用循环草稿，保留语法问题与工具占位实现 |

以上未完成内容均保留原样，未在仓库整理中补全。

## 资料包组成

| 目录 | 内容 |
|---|---|
| `90_resources/courses/cmu/11_768_ai_agents/` | CMU 11-768《AI Agents》（2026 秋季）课程课件：5 份讲座 slides PDF + 课程 README（含视频链接、GitHub 作业链接） |
| `90_resources/courses/cmu/11_763_llm_inference/` | CMU 11-763《Inference Algorithms for Language Modeling》（2025 秋季）课程资料：7 份讲座 slides PDF + 作业代码仓库（含 3 个 homework + 期末项目 starter code）+ 课程 README |
| `90_resources/agent_selfstudy/` | 自学资料包：9 篇博客笔记、8 篇论文 PDF、5 个开源实现、31 份 LLM 公开课课件 + 中文总 README（含学习路线） |
| [90_resources/courses/cmu/11_868_llm_systems/](90_resources/courses/cmu/11_868_llm_systems/README.md) | CMU 11-868《Large Language Model Systems》课程归档、作业 starter 与示例代码 |

注意：现有 `.gitignore` 排除了 PDF、部分数据/权重格式与生成产物。它们保留在本地，但上述资源清单不等于新克隆仓库中必然存在的文件清单。

---

## CMU 11-768《AI Agents》课程外链

- 课程官网（含课程表、slides、阅读材料）：https://cmu-agents.com
- 讲座录像（YouTube，Graham Neubig 个人频道 https://www.youtube.com/@neubig）：
  - L1 What are Agents and How Do They Work?：https://www.youtube.com/watch?v=UwfjzyLnvMg
  - L2 Tool Use for Language Model Agents：https://www.youtube.com/watch?v=jXChFB4JSyw
  - L3 Long Context Modeling for Agents：https://www.youtube.com/watch?v=AiwCCvFW1uE
  - L4 Memory and Skills for Agents：https://www.youtube.com/watch?v=6zigF2a-2Pw
- 课程 GitHub 组织：https://github.com/cmu-agents
  - 作业 1（手写 ReAct harness）：https://github.com/cmu-agents/assignment-1
  - 作业 2（agent 评测设计）：https://github.com/cmu-agents/assignment-2
  - chess-app（课程配套）：https://github.com/cmu-agents/chess-app

---

## 核心概念索引（概念 → 课件 / 论文 / 博客 / 代码 / 官方文档）

### ReAct（Thought → Action → Observation 循环）
- 论文：https://arxiv.org/abs/2210.03629（本地 `90_resources/agent_selfstudy/papers/Yao2022-ReAct.pdf`）
- 博客精读：`90_resources/agent_selfstudy/blogs/06-demystifying-react-explainer.md`（原文：https://dev.to/4484ho/demystifying-react-why-reasoning-and-acting-is-the-standard-for-llm-agents-1ii6）
- 代码实现：`90_resources/agent_selfstudy/code/microagent/microagent/parser.py`（文本协议解析，带中文注释）、`90_resources/agent_selfstudy/code/microagent/microagent/agent.py`（主循环）、`90_resources/agent_selfstudy/code/assignment-1/src/assignment/agent/base.py`（课程作业版）

### Tool Use / Function Calling（工具调用）
- 课程课件：`90_resources/courses/cmu/11_768_ai_agents/slides/lecture-02-tool-use.pdf`＋ 视频 https://www.youtube.com/watch?v=jXChFB4JSyw
- 论文 Toolformer：https://arxiv.org/abs/2302.04761（本地 `90_resources/agent_selfstudy/papers/Schick2023-Toolformer.pdf`）
- 论文 Gorilla（API 调用准确率）：https://arxiv.org/abs/2305.15334（本地 `90_resources/agent_selfstudy/papers/Patil2023-Gorilla.pdf`）
- 博客辨析：`90_resources/agent_selfstudy/blogs/07-toolformer-vs-agents-explainer.md`（原文：https://medium.com/@rashmi18patel/toolformer-vs-agents-a-deep-learning-perspective-e1f60af29694）
- 官方文档：OpenAI Function Calling https://platform.openai.com/docs/guides/function-calling

### Long Context（长上下文管理）
- 课程课件：`90_resources/courses/cmu/11_768_ai_agents/slides/lecture-03-long-context.pdf` ＋ 视频 https://www.youtube.com/watch?v=AiwCCvFW1uE
- 上下文压缩实战：`90_resources/agent_selfstudy/code/assignment-1/src/assignment/agent/base.py` 顶部中文注释（compaction 机制）

### Memory & Skills（记忆与技能）
- 课程课件：`90_resources/courses/cmu/11_768_ai_agents/slides/lecture-04-memory-and-skills.pdf` ＋ 视频 https://www.youtube.com/watch?v=6zigF2a-2Pw
- 论文 MemGPT：https://arxiv.org/abs/2310.08560（本地 `90_resources/agent_selfstudy/papers/Packer2023-MemGPT.pdf`）
- 论文 Reflexion（试错自改进）：https://arxiv.org/abs/2303.11366（本地 `90_resources/agent_selfstudy/papers/Shinn2023-Reflexion.pdf`）

### Coding Agents（代码智能体）
- 课程课件：`90_resources/courses/cmu/11_768_ai_agents/slides/lecture-06-coding-agents.pdf`
- 论文 SWE-agent：https://arxiv.org/abs/2405.15793（本地 `90_resources/agent_selfstudy/papers/Yang2024-SWE-agent.pdf`）
- 课程作业实战：https://github.com/cmu-agents/assignment-1（本地 `90_resources/agent_selfstudy/code/assignment-1/`）

### Computer Use Agents（计算机操作智能体）
- 课程课件：`90_resources/courses/cmu/11_768_ai_agents/slides/lecture-07-computer-use-agents.pdf`

### Deep Research Agents（深度调研智能体）
- 开源实现：`90_resources/agent_selfstudy/code/deep-research/`（TypeScript，<500 行，核心文件 `src/deep-research.ts` 带中文注释）

### Multi-Agent（多智能体协作）
- 开源 demo：`90_resources/agent_selfstudy/code/smolagents-codeagent-demo/main.py`（manager + web_agent 协作，带中文注释）
- 设计模式：`90_resources/agent_selfstudy/blogs/09-andrew-ng-agentic-design-patterns.md`（原文：https://www.deeplearning.ai/the-batch/issue-242/）

### Planning（规划）
- 论文 Plan-and-Solve：https://arxiv.org/abs/2305.04091（本地 `90_resources/agent_selfstudy/papers/Wang2023-Plan-and-Solve.pdf`）
- 论文 ReWOO（规划与执行解耦）：https://arxiv.org/abs/2305.18323（本地 `90_resources/agent_selfstudy/papers/Xu2023-ReWOO.pdf`）

### Agent 评测（Evaluation）
- 课程作业 2：https://github.com/cmu-agents/assignment-2（本地 `90_resources/agent_selfstudy/code/assignment-2/`，含中文 NOTES）

### Agent 安全
- 必读博客：`90_resources/agent_selfstudy/blogs/05-simon-willison-lethal-trifecta.md`（原文：https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/）
- Agent 定义：`90_resources/agent_selfstudy/blogs/04-simon-willison-agent-definition-loop.md`（原文：https://simonwillison.net/2025/Jun/5/wrecking-its-environment-in-a-loop/）

### Agent 工程总览（先读这些建立全局观）
- Lilian Weng《LLM Powered Autonomous Agents》：https://lilianweng.github.io/posts/2023-06-23-agent/（本地笔记 `90_resources/agent_selfstudy/blogs/01-lilian-weng-llm-powered-autonomous-agents.md`）
- Anthropic《Building Effective Agents》：https://www.anthropic.com/research/building-effective-agents（本地笔记 `90_resources/agent_selfstudy/blogs/02-anthropic-building-effective-agents.md`）
- OpenAI《A Practical Guide to Building Agents》：https://openai.com/business/guides-and-resources/a-practical-guide-to-building-ai-agents/（本地笔记 `90_resources/agent_selfstudy/blogs/03-openai-practical-guide-building-agents.md`）
- Chip Huyen《Agents》：https://huyenchip.com/2025/01/07/agents.html（本地笔记 `90_resources/agent_selfstudy/blogs/08-chip-huyen-agents-ai-engineering.md`）

---

## 框架与协议官方文档

- smolagents（HuggingFace 轻量 agent 库）：https://huggingface.co/docs/smolagents ｜ 仓库 https://github.com/huggingface/smolagents
- OpenAI Function Calling：https://platform.openai.com/docs/guides/function-calling
- MCP（Model Context Protocol，microagent 的 `mcp/` 模块用的就是它）：https://modelcontextprotocol.io
- 大型框架（只记链接，未下载）：LangChain https://github.com/langchain-ai/langchain ｜ OpenHands https://github.com/All-Hands-AI/OpenHands ｜ AutoGPT https://github.com/Significant-Gravitas/AutoGPT

---

## CMU 11-664/763《Inference Algorithms for Language Modeling》课程外链

LLM 推理时算法课（Neubig + Amanda Bertsch，2025 秋季）：采样、beam search、受控生成、reward model、推理扩展等。

- 课程官网（含课程表、作业说明）：https://phontron.com/class/lminference-fall2025/
- 作业页：https://www.phontron.com/class/lminference-fall2025/assignments/
- YouTube 完整播放列表（22 讲录像都在这）：https://www.youtube.com/playlist?list=PL8PYTP1V4I8DY15Ob83nmwBAVyNtUQadX
- 作业代码仓库：https://github.com/neubig/lminference-fall2025-code（本地 `90_resources/courses/cmu/11_763_llm_inference/code/`：HW1 解码方法、HW2 元解码/Best-of-n/MBR、HW3 自写高效推理系统、期末推理服务器项目）
- 本地课件（7 份，`90_resources/courses/cmu/11_763_llm_inference/slides/`）：
  - 采样方法 `lecture-0902-sampling-methods.pdf` ｜ Beam Search `lecture-0904-beam-search.pdf`
  - 受控生成 `lecture-0911-controlled-generation.pdf` ｜ Reward Model / Best-of-N `lecture-1002-reward-models-best-of-n.pdf`
  - MBR 解码 `lecture-1009-mbr-multi-sample.pdf` ｜ 推理扩展 vs 模型扩展 `lecture-1021-inference-scaling.pdf`
  - 线性注意力/稀疏模型 `lecture-1118-linear-attention-sparse.pdf`
- 注意：Neubig 主讲的 12 讲（CoT、Self-Refine、推理模型、工具调用、Agents、vLLM/SGLang 等）和 3 场嘉宾讲座无公开课件，只能看上面播放列表里的录像。

### 推理时算法核心概念索引

- 采样 / 解码（temperature、top-k、top-p、mirostat）：课件 `lecture-0902-sampling-methods.pdf` ＋ 作业 HW1（`code/homework1/`，含坏掉的 diverse beam search 等 starter code 可动手修）
- Beam Search 及其变体：课件 `lecture-0904-beam-search.pdf`
- Best-of-N / Reward Model / MBR 解码：课件 `lecture-1002-reward-models-best-of-n.pdf`、`lecture-1009-mbr-multi-sample.pdf` ＋ 作业 HW2（`code/homework2/`，含 basic_deepresearch 示例）
- 推理扩展（inference scaling）：课件 `lecture-1021-inference-scaling.pdf` —— "用更多推理算力换质量"，是推理模型（o1/R1 类）背后的核心思想
- 高效推理系统（vLLM / SGLang 原理）：作业 HW3（`code/homework3/`，要求禁用现成框架手写，学原理最直接）
- 推理服务器实战：期末项目 starter（`code/final-project/`）

---

## LLM 公开课外链（课件在本地，视频/代码见官网）

- CMU 11-711 高级 NLP（Spring 2026，23 份课件在 `90_resources/agent_selfstudy/courses/anlp-spring2026/`）：https://cmu-l3.github.io/anlp-spring2026/
- Stanford CS336 从零搭建语言模型（Spring 2025，8 份课件在 `90_resources/agent_selfstudy/courses/cs336-spring2025/`）：https://stanford-cs336.github.io/spring2025/
- Karpathy《Let's build GPT》视频播放列表：https://www.youtube.com/playlist?list=PLAqhIrjkxbuWI23v9cThsA9GvCAUhRvKZ ｜ nanoGPT 仓库：https://github.com/karpathy/nanoGPT

---

## 建议学习顺序

1. 工程总览博客（Lilian Weng → Anthropic → OpenAI）建立全局观
2. CMU 11-768 L1–L4 课件＋视频：agent 基本概念、工具调用、长上下文、记忆
3. 对照读 `microagent` 代码（带中文注释），理解 ReAct 循环是怎么转起来的
4. 读 ReAct / Toolformer / MemGPT 三篇论文
5. 动手：跑通 `assignment-1` 或 `smolagents-codeagent-demo`
6. 进阶：L6/L7 课件、SWE-agent 论文、deep-research 代码、公开课课件查漏补缺
