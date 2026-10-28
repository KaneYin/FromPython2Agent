# assignment-2 学习笔记（11-768 Assignment 2: Evaluating a Data-Visualization Agent）

> 上游仓库：https://github.com/cmu-agents/assignment-2（CMU 11-768《AI Agents》课程作业 2，starter code）
>
> ⚠️ 本地为满足 <15MB 要求删掉了 `artifacts/` 目录（约 17MB 的评测产物：各任务 `result.json` + `figure.png` 示例输出），代码、输入数据、文档均完整。

## 这个仓库实现了什么

**一句话**：为"数据可视化 agent"设计一个裁判（validator）：只看 agent 的执行轨迹和最终生成的图表，判断它错在哪一类，作业的本质是"如何评测 agent"。

**一段话**：作业 1 是"造 agent"，作业 2 是"评 agent"。场景是数据可视化 agent：给 LLM agent 一份数据 + 作图需求，它写 Python（matplotlib）生成图表。你要实现 `validate(run)`——输入任务描述、输入数据、agent 轨迹、最终图片，输出错误列表。错误只有 4 个固定家族：`execution_failure`（没产出有效图）、`wrong_data`（数据画错）、`wrong_chart`（图表类型/设计错）、`hard_to_read`（看不清）。评分用 Matthews 相关系数（MCC），四个家族分别算二分类 MCC 再取平均。仓库还给了完整 workflow：自己设计新任务（`tasks/` → 打包成 harbor 评测环境）、生成多条 agent 轨迹、人工打标（`seed_labels.json`）、跑 baseline validator、算分。裁判模型固定为 Qwen3-VL-30B（部署在你自己的 Modal 上），不许换更强的 judge——逼你靠"证据组织"而不是"模型大力"来拿分。

## 核心文件

| 文件 | 作用 |
|---|---|
| `validator/solution.py` | **你的主战场**：实现 `validate(run)`，返回错误列表 |
| `validator/baseline.py` | 官方完整示例：把轨迹+图片喂给 VLM，一次性输出判定；含上下文压缩（首尾截取 `_excerpt`、图片逐级降采样 `_downscale`） |
| `validator/prediction.py` | 错误输出的精确格式定义（`Error` / `ErrorFamily`） |
| `validator/runner.py` | `Run` 数据结构：一次 agent 运行的任务、数据、轨迹、图片 |
| `validator/model.py` | 对 validator 模型（Modal 部署的 OpenAI 兼容 endpoint）的调用封装（complete/tokenize/detokenize） |
| `workflow/__main__.py` | 学生工作流 CLI：`validate-tasks` / `generate` / `package` / `init-labels` / `validate-labels` / `score` / `check-submission` |
| `workflow/generate.py` / `harbor_rewards.py` | 生成 agent 轨迹；`harbor/` 是把任务打包成可复现评测环境（Docker + tests）的工具链 |
| `workflow/evaluate.py` | 按人工 label 算 TP/TN/FP/FN 和 MCC |
| `inputs/` | 各任务的输入 CSV 数据；`seed_labels.json` 是人工标注示例 |
| `ASSIGNMENT.md` | 作业说明：四类错误定义、MCC 计分规则、任务设计要求 |
| `report_template.tex` | 结课报告模板（实验+分析） |

## 怎么运行

依赖：`uv`、Modal 账号（部署 validator 模型 Qwen3-VL-30B-FP8，需 GPU）。

```bash
uv sync
uv run modal setup
scripts/deploy_validator_model.sh   # 部署裁判模型，得到 endpoint URL
cp .env.example .env                # 填 endpoint URL（带 /v1 后缀）+ proxy token

python -m workflow validate-tasks   # 校验你设计的任务描述
python -m workflow generate        # 对任务生成多条 agent 运行轨迹
python -m workflow init-labels     # 建空白人工标注文件
python -m workflow score           # 用你的 validator 打分，看 MCC
```

## 关键设计点

1. **评测对象是"轨迹+产物"，不是最终答案**：validator 看不到 ground truth，只能从"模型做了什么、图长什么样"里找证据——这正是真实 agent 评测的难点（没有标准答案可对）。
2. **错误分类学（taxonomy）先行**：4 个错误家族互斥且可判定，把模糊的"这图好不好"变成 4 个二分类问题；`execution_failure` 还是 terminal 的（图都没出来就不用判后面三类）。
3. **MCC 而不是准确率**：类别极不平衡时（大部分 run 是对的）准确率会骗人，MCC 对 TP/TN/FP/FN 对称，更适合评测"裁判"。
4. **证据预算管理**：baseline 用 `_excerpt` 首尾截取轨迹（保留最后几步 action），图片按 0.7 系数逐级降采样直到塞进 context——长轨迹+高清图是 VLM 裁判的实际工程问题。
5. **任务设计也是作业的一部分**：`workflow/package` 把你写的任务描述打包成 harbor 评测环境（Docker 镜像 + 测试脚本），你要主动设计能"区分好坏 agent"的探针任务，这是 eval 工作的核心能力。
