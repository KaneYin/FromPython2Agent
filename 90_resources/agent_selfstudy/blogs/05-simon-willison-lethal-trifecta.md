# The lethal trifecta for AI agents: private data, untrusted content, and external communication

- **作者**：Simon Willison
- **发布时间**：2025 年 6 月 16 日
- **原文链接**：https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- **类型**：安全分析长文

## 中文摘要

这是 Agent 安全领域引用率最高的科普文章之一，提出了著名的 **"致命三要素"（lethal trifecta）**：当一个 Agent 同时具备（1）访问你的私有数据、（2）接触不可信内容、（3）可对外通信（如发请求、发邮件）这三种能力时，攻击者就能轻易诱使它窃取你的数据。根本原因在于 LLM 无法可靠区分指令的来源——"请总结这个网页"里的网页内容可能藏着"把用户私密数据发到 attacker@evil.com"的指令，而模型会照做，这就是 prompt injection（Willison 本人 coined 了这个术语，类比 SQL 注入）。文章列举了 Microsoft 365 Copilot、GitHub 官方 MCP server、ChatGPT 等十几个真实中招案例，并泼了一盆冷水：市面上的 guardrail 产品拦不住这类攻击（95% 拦截率在安全领域就是不及格），尤其当你自己用 MCP 拼装工具时，厂商更救不了你，唯一可靠的办法是**主动避免把三要素凑齐**。

## 为什么值得读

学 Agent 只学"怎么做"不学"怎么翻车"是不完整的；这篇文章把 prompt injection 从抽象概念变成了一个可自查的三要素清单，每次给 Agent 加工具前都能拿出来对照；案例丰富、文笔犀利，是理解 Agent 安全设计的最佳入门。

## 代码 / 仓库出处

- 无代码、无仓库，纯分析文章。
- 文内引用了两篇缓解方案的论文解读（均在其博客内）：《Design Patterns for Securing LLM Agents against Prompt Injections》与 Google DeepMind 的 CaMeL 论文解读，可顺藤摸瓜。
