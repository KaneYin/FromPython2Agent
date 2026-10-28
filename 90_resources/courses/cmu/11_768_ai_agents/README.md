# CMU 11-768《AI Agents》Fall 2026 公开资料整理

> 整理时间：2026-09-25。课程正在进行中（Fall 2026 学期），资料会随课程推进陆续发布。

## 课程简介

- **课程**：11-768 · AI Agents，Carnegie Mellon University，Fall 2026
- **授课**：Daniel Fried、Graham Neubig
- **课程官网**：https://www.cmu-agents.com （也解析 https://cmu-agents.com）
- **上课时间**：每周二/四 3:30–4:50 PM，Porter Hall 100
- **课程内容**：基于 LLM 的 AI Agent 系统——感知、推理、规划、多步行动；涵盖搭建 Agent 的基础知识，以及长时程推理（long-horizon reasoning）、训练、安全性、人机交互等前沿研究问题。强调动手实现与训练方法。
- **重要时间节点**：Fall Break 10/12–10/16，Thanksgiving Break 11/25–11/27，期末展示（poster）12/1–12/3

## 讲座一览

| # | 标题 | 幻灯片（本地） | 视频 | 阅读材料 |
|---|------|---------------|------|----------|
| 1 | What are Agents and How Do They Work?（Fried & Neubig） | 未找到公开 slides | https://www.youtube.com/watch?v=UwfjzyLnvMg | Toolformer、ReAct |
| 2 | Tool Use for Language Model Agents（Neubig） | slides/lecture-02-tool-use.pdf（3.8 MB） | https://www.youtube.com/watch?v=jXChFB4JSyw | function calling、chat templates、XGrammar 约束解码、Berkeley Function-Calling Leaderboard |
| 3 | Long Context Modeling for Agents（Neubig） | slides/lecture-03-long-context.pdf（1.9 MB） | https://www.youtube.com/watch?v=AiwCCvFW1uE | 上下文管理、needle-in-a-haystack 评测的局限性 |
| 4 | Memory and Skills for Agents（Fried） | slides/lecture-04-memory-and-skills.pdf（5.8 MB） | https://www.youtube.com/watch?v=6zigF2a-2Pw | MemGPT、Agent Workflow Memory、Agent Skill Induction、ReasoningBank |
| 5 | （标题未知，尚未确认） | 未找到 | 未找到 | 未知 |
| 6 | Agents for Coding and Software Development | slides/lecture-06-coding-agents.pdf（4.3 MB） | 未找到 | 未知 |
| 7 | Computer Use Agents | slides/lecture-07-computer-use-agents.pdf（7.0 MB） | 未找到 | 未知 |

> 注：阅读材料主要来自课程相关的公开报道（LinkedIn 帖子），官网 schedule 页面暂时无法抓取；建议以官网最终公布为准。

### 后续课程（syllabus 预告，尚未发布）

据课程大纲预告，后半学期还包括以下主题，slides/视频均未发布：

- RL 训练 Agent（共 4 讲）
- Sandboxing 与凭证管理（credential management）
- Observability 与监控
- Deep research agents
- Multi-agent 交互
- Guest lectures：Sasha Rush、Karthik Narasimhan

## 缺失项说明

1. **Lecture 1 的幻灯片**：在搜索引擎索引和官网已知 URL 模式中均未找到，未收录（不编造 URL）。
2. **Lecture 5**：标题与材料均未在公开渠道确认，未收录。
3. **Lecture 6/7 的视频**：YouTube 上目前只找到前 4 讲的视频，第 5 讲及之后的视频尚未发布。
4. **Lecture 8+**：syllabus 预告的 RL、sandboxing、observability、deep research、multi-agent 等主题尚未开讲，无公开材料。
5. **YouTube 播放列表**：未找到该课程的官方播放列表；已发布的 4 个视频均在 Graham Neubig 的个人频道（https://www.youtube.com/@neubig）。
6. **Piazza / Canvas**：需要登录，未收录。

## GitHub（作业与代码）

- 组织主页：https://github.com/cmu-agents
- **assignment-1**（11-768 Assignment 1: Build an Agent Harness）：https://github.com/cmu-agents/assignment-1
- **assignment-2**：https://github.com/cmu-agents/assignment-2（已存在，具体内容未确认）
- **chess-app**：https://github.com/cmu-agents/chess-app

（仓库较大，仅记录链接，未完整下载。）

## 本地文件

- `slides/`：5 个已验证的 PDF 幻灯片，共约 22.8 MB
- `README.md`：本文件

下载验证：每个 PDF 均通过 `file` 命令确认为有效 PDF 文档。
