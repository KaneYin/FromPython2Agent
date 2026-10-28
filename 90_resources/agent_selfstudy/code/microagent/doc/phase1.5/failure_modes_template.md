# 任务：产出 docs/FAILURE_MODES.md

基于 Phase 1.5 已有的实验数据和已知问题，产出一份正式的 Failure Modes 研究文档。**这不是 bug list，而是 Agent 工程边界的研究档案。**

## 写作纪律

1. **每条 failure 必须可复现**：列出 query、strategy、模型、跑了几次、结果分布
2. **每条 failure 必须区分"第一直觉"和"真实根因"**：这是文档的灵魂，体现调试深度
3. **每条 failure 必须分类**：环境层 / 工具层 / Prompt 层 / 模型层 / 框架层
4. **写作风格**：技术、克制、精确。不要营销腔，不要"😀"，不要"我们相信"。每个结论要有数据/trace 支撑
5. **每条 failure 不少于 200 字，不多于 600 字**。太短没价值，太长读者放弃

## 必须包含的章节

### 1. 文档说明（开头）
说明这份文档是什么、不是什么。明确：
- 这是 Agent 边界的研究记录，不是 bug tracker
- 失败的五个分类层及其定义
- 测试环境基线（vLLM + MiniMax 2.5 FP8，具体版本号问我）

### 2. Failure 分类总览表
所有 failure 一张表，列：ID / 标题 / Category / Affected Strategy / Severity / Status

### 3. 详细 Failure 档案
**每条 failure 用下面这个模板**：

```markdown
## F0X: <一句话标题>

**Category**: <环境层/工具层/Prompt 层/模型层/框架层>
**Affected Strategy**: <FC only / Text only / Both>
**Discovered**: <YYYY-MM-DD, 哪个实验中发现>
**Severity**: <High / Medium / Low>
**Status**: <✅ Fixed / ⚠️ Known limitation / 🔬 Under investigation>

### 现象
Query 是什么、跑了多少次、结果分布、典型错误形态。

### 第一直觉（错误判断）
最初怀疑的方向。**必须坦诚写错误的假设**，这是文档价值所在。

### 真实根因
查到的真实原因。引用 trace 片段、代码片段、log 片段作证。

### 修复 / 当前处理
如果修了，怎么修的；如果没修，为什么是已知局限。

### 工程教训
1-3 条可迁移的认知。

### 相关 Trace
列出对应的 trace 文件路径。
```

## 必须入档的 5 个 failure（已有数据）

### F01: tzdata 缺失导致 datetime_now 工具在 Windows 上全部失败
- Category: 环境层
- 现象：Q4 "现在几点" FC 1/3、Text 0/3
- 第一直觉：function calling 对零参数工具支持差 / 模型变笨了
- 真实根因：Windows 缺 tzdata 包，ZoneInfo 全部抛错；模型在反复重试是正确的错误响应
- 修复：pyproject.toml 加 `tzdata; sys_platform == 'win32'`
- 工程教训：trace 必须包含工具真实返回；"模型重试 ≠ 模型不会"

### F02: FC 模式下 Q4 仍有不稳定性（如果 tzdata 修复后仍存在）
- 让用户先验证：修了 tzdata 后 Q4 是不是 3/3 通过了？
  - 如果是 → F02 不存在，跳过
  - 如果还有失败 → 入档为 "Model layer: function calling 在零参数 / 全可选参数工具上的行为"

### F03: Q7 "今天日期加 365 天" 复合推理失败
- Category: 模型层 + 工具层
- 现象：FC 2/3、Text 0/3
- 第一直觉：text ReAct 的显式 CoT 在复合推理上应该胜出
- 真实根因：工具集不完备（缺日期算术工具），模型在不完备工具集下推理链拉长；text ReAct 的格式约束反而加重了认知负担
- 修复：未修，作为 known limitation；Phase 2 计划补 date arithmetic 工具
- 工程教训：Agent 能力上限 = 推理能力 × 工具集完备度

### F04: Text 模式 Q6 step 数不稳定（2-5 步）
- Category: Prompt 层
- 现象：Q6 "统计 hello world 单词数+时间" Text 模式 step 在 2-5 之间漂移
- 第一直觉：模型在多工具组合下"想多了"
- 真实根因：text ReAct 的 prompt 模板没有显式禁止"同一步执行多工具"，模型在 Thought 阶段会尝试规划，有时收敛快有时收敛慢
- 修复：当前未修，已知 prompt 设计权衡（强约束 prompt 可能损害复杂任务表现）
- 工程教训：prompt 工程的"约束强度"是连续光谱，没有一刀切答案

### F05: FC 模式 Q6 返回 2 个 tool_calls，框架仅执行 1 个
- Category: 框架层
- 现象：MiniMax 返回 2 个 tool_calls 同时调用 text_stats + datetime_now，框架打 warning 仅串行执行第一个
- 第一直觉：这是模型协议错误
- 真实根因：parallel tool calling 是协议合法行为，是 Phase 1.5 框架主动的设计选择（串行实现优先）
- 修复：Phase 2 计划支持串行执行所有 tool_calls；Phase 3 计划支持并行
- 工程教训：框架能力滞后于模型能力是常态；可观测的限制比隐藏的限制好

## tools_schema_cost finding（独立小节，不入 failure 表）

在文档末尾加一节："Appendix A: tools schema 的隐性 token 成本"
- 实验数据：无 tools 53 tokens vs 带 3 tools 333 tokens, delta=282 tokens
- 修正原先的错误结论：tools schema **每次** LLM 调用都重新提交并计费，不是"只出现一次"
- 推论：FC 节省总 token 的主因是 completion 更紧凑 + 步数更少，**不是** schema 摊销
- 工程含义：超长对话 / 多轮任务下，FC 的 schema 重复成本可能反超节省，需要按场景评估

## 输出位置

`docs/FAILURE_MODES.md`

## 不要做的事

- ❌ 不要写"未来工作"章节，那是 Roadmap 的事
- ❌ 不要写"致谢" / "贡献者" 之类
- ❌ 不要为每个 failure 写代码 fix，那是 commit 的事
- ❌ 不要堆 emoji
- ❌ 不要在 F01-F05 之外凭空捏造 failure。如果想加新的，先告诉我数据来源

完成后停下，让我 review。