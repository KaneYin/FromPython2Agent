## F06: 并行 tool calling 行为不稳定

**Category**: 模型层
**Affected Strategy**: FC only
**Severity**: Low
**Status**: Known limitation

### 现象
Q6 在 Phase 2.1（已支持并行执行）下跑 3 次：
- 1 次：模型串行调用（2 step / 1 action per step）
- 2 次：模型并行调用（2 step / 第 1 步 2 actions）

同条件 temperature=0，行为仍不一致。

### 真实根因
parallel tool calling 是模型的可选行为，MiniMax 2.5 未明确保证。框架已正确支持并行执行，限制来自模型层。

### 工程教训
框架能力 ≥ 模型能力时，可观测的余量本身就是设计正确性的证明——Run 2/3 证明并行路径工作，Run 1 暴露了模型行为差异。