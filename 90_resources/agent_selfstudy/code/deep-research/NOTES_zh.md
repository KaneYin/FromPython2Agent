# deep-research 学习笔记（极简 Deep Research Agent，<500 行 TypeScript）

> 上游仓库：https://github.com/dzhng/deep-research（MIT，19.7k stars；作者目标：保持 <500 行，简单到能看懂、能魔改）

## 这个仓库实现了什么

**一句话**：一个 TypeScript 写的极简"深度研究"agent：输入问题，自动生成搜索 query → 并行搜+抓网页 → 提炼 learnings → 按 breadth/depth 递归深挖 → 输出带引用来源的 Markdown 报告。

**一段话**：这是 OpenAI Deep Research 的开源极简复刻，代码只有约 877 行（含测试），核心逻辑在 `src/deep-research.ts`（294 行）。流程是：先让 LLM 针对用户问题生成追问（`feedback.ts`）澄清需求；然后循环"生成 SERP queries → Firecrawl 并行搜索抓取 → LLM 提炼 learnings 和新的研究方向"；用 `breadth`（每轮几个 query）和 `depth`（递归几层）两个参数控制研究规模；`p-limit` 做并发控制；最后把所有 learnings + 访问过的 URL 拼成 Markdown 报告写进 `report.md`。它证明了"复杂 agent 行为"不需要框架：三个 LLM 调用模式（query 生成、结果提炼、报告合成）+ 递归 + 并发就是全部。

## 核心文件

| 文件 | 作用 |
|---|---|
| `src/deep-research.ts` | **核心**：`deepResearch()` 递归主流程；`generateSerpQueries()` 生成搜索词；`processSerpResult()` 提炼 learnings |
| `src/run.ts` | CLI 入口：交互式问用户 query/breadth/depth，驱动 research，写 `report.md` |
| `src/api.ts` | Firecrawl 搜索+抓取的封装 |
| `src/prompt.ts` | system prompt（"你是专家研究员…"，含日期注入） |
| `src/feedback.ts` | 研究前的澄清追问生成 |
| `src/ai/providers.ts` | 模型选择：默认 OpenAI o3-mini，有 `FIREWORKS_KEY` 则切 DeepSeek R1；支持自定义 OpenAI 兼容 endpoint |
| `src/ai/text-splitter.ts` | 网页长文本切分（+ 单元测试） |
| `package.json` | `npm start` 启动；依赖 `ai` SDK（Vercel AI SDK 的 `generateObject`）、`firecrawl-js`、`zod`、`p-limit` |

## 怎么运行

依赖：Node.js；需要 Firecrawl API key（搜索+抓取）+ OpenAI API key（默认 o3-mini）。

```bash
npm install
# .env.local 文件：
# FIRECRAWL_KEY="..."
# OPENAI_KEY="..."
# （可选）FIREWORKS_KEY="..." → 自动改用 DeepSeek R1
# （可选）OPENAI_ENDPOINT + CUSTOM_MODEL → 接本地/第三方 OpenAI 兼容模型
npm start
# 按提示输入：研究问题 → breadth（建议 3-10，默认 4）→ depth（建议 1-5，默认 2）→ 回答澄清追问
# 最终报告写入 report.md（含来源 URL）
```

Docker 方式见 README（`docker compose up -d` + `docker exec -it deep-research npm run docker`）。

## 关键设计点

1. **结构化输出驱动流程**：用 `generateObject` + zod schema 让 LLM 输出"query 列表""learnings 列表"这类结构化数据，而不是自由文本再正则解析——这是现代 agent 最稳的做法。
2. **递归即"深度"**：`depth > 0` 就拿新 learnings 生成更具体的 query 继续挖，天然形成"越挖越深"的研究行为；`breadth` 控制每层宽度。两个参数就是全部的"规划"。
3. **learnings 累积作为上下文**：每轮把新 learnings 拼进下一轮 query 生成的 prompt，agent 的"记忆"就是不断增长的 learnings 列表，简单但有效。
4. **并发控制**：`p-limit` 限制同时搜索数（默认 2，免费版 Firecrawl 建议 1），工程上防限流。
5. **模型可插拔**：`getModel()` 按环境变量切换 o3-mini / DeepSeek R1 / 任意 OpenAI 兼容 endpoint（含本地模型），换模型不用改业务逻辑。
