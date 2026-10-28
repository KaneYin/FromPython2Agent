# An agent is an LLM wrecking its environment in a loop

- **作者**：Simon Willison
- **发布时间**：2025 年 6 月 5 日
- **原文链接**：https://simonwillison.net/2025/Jun/5/wrecking-its-environment-in-a-loop/
- **类型**：观点短文（Agent 定义收藏系列之一）

## 中文摘要

Docker 创始人 Solomon Hykes 在 AI Engineer World's Fair 上抛出了一个被 Simon Willison 称为"见过最好的 Agent 定义"：**An AI agent is an LLM wrecking its environment in a loop（AI Agent 就是在一个循环里不断"折腾"其环境的 LLM）**。Willison 指出这句话妙在融合了两种定义传统：一是当下流行的"工具循环"定义（Anthropic 式：LLM 基于环境反馈反复调用工具），二是可追溯到上世纪 90 年代的经典学术定义（agent 是感知环境并作用于环境的东西）。文章很短，本质是一则带点评的收藏，但它把 Agent 的本质压缩成一句话心智模型：LLM 调用 → 环境（Action）→ 反馈（Feedback）→ 下一次 LLM 调用，直到停止条件。Willison 长期在博客收集各种 Agent 定义，这篇是其中传播最广的一则。

## 为什么值得读

一分钟读完，却能帮你建立对 Agent 最本质的直觉——"循环 + 环境反馈"才是 Agent 与普通 LLM 调用的分水岭；之后读 ReAct、读 Anthropic 的 autonomous agent 章节时，都会自动映射到这个循环图上；也适合在向别人解释"什么是 Agent"时直接引用。

## 代码 / 仓库出处

- 纯观点文章，无代码、无仓库。
- 文内链接：Anthropic《Building Effective Agents》与经典 agent 学术定义，供延伸阅读。
