# CMU 11-664/763《Inference Algorithms for Language Modeling》（2025 秋季）

纯 LLM 推理课：研究"已经训练好的大模型，如何在推理时用算法提升生成质量、降低延迟、增强可控性"。
授课：Graham Neubig、Amanda Bertsch（CMU）。课程官网：https://phontron.com/class/lminference-fall2025/

> 这是 Graham Neubig（也是 CMU 11-768《AI Agents》的老师）开的课，两门课有呼应：
> 11-768 讲"怎么搭 agent"，这门课讲"agent 底下那层推理算法是怎么工作的"（采样、搜索、推理模型、工具调用、推理加速）。

## 讲座一览

课程表来源：https://phontron.com/class/lminference-fall2025/schedule/（已验证）。
YouTube 播放列表（整门课录像）：https://www.youtube.com/playlist?list=PL8PYTP1V4I8DY15Ob83nmwBAVyNtUQadX

| 日期 | 讲座 | 授课 | 本地 slides | 视频 |
|---|---|---|---|---|
| 08-26 | Introduction to Language Models and Inference | Graham | —（见 `code/01-lm-intro/`） | 播放列表 |
| 08-28 | Probability Review and Shared Task Introduction | Graham | —（见 `code/02-generation-basics/`） | 播放列表 |
| 09-02 | Common Sampling Methods for Modern NLP | Amanda | `slides/lecture-0902-sampling-methods.pdf`（30页） | 播放列表 |
| 09-04 | Beam Search and Variants | Amanda | `slides/lecture-0904-beam-search.pdf`（51页） | 播放列表 |
| 09-09 | Intro to A* and Best First Search | Graham | ❌ 无公开课件 | 播放列表 |
| 09-11 | Other Controlled Generation Methods | Amanda | `slides/lecture-0911-controlled-generation.pdf`（43页） | 播放列表 |
| 09-16 | Chain of Thought and Intermediate Steps | Graham | ❌ 无公开课件 | 播放列表 |
| 09-18 | Self-Refine and Self-Correction Methods | Graham | ❌ 无公开课件 | 播放列表 |
| 09-23 | Reasoning Models（STaR、DeepSeek-R1） | Graham | ❌ 无公开课件 | 播放列表 |
| 09-25 | Incorporating Tools（PAL、Toolformer、Gorilla、MCP） | Graham | ❌ 无公开课件 | 播放列表 |
| 09-30 | Agents and Multi-Agent Communication | Graham | ❌ 无公开课件 | 播放列表 |
| 10-02 | Reward Models and Best-of-N | Amanda | `slides/lecture-1002-reward-models-best-of-n.pdf`（36页） | 播放列表 |
| 10-07 | Systems not Models（嘉宾：Omar Khattab，DSPy） | 嘉宾 | ❌ 无公开课件 | 播放列表 |
| 10-09 | Minimum Bayes Risk and Multi-Sample Strategies | Amanda | `slides/lecture-1009-mbr-multi-sample.pdf`（43页） | 播放列表 |
| 10-21 | Inference Scaling vs Model Size | Amanda | `slides/lecture-1021-inference-scaling.pdf`（45页） | 播放列表 |
| 10-28 | Diffusion Models | Graham | ❌ 无公开课件 | 播放列表 |
| 10-30 | Defining Efficiency | Graham | ❌ 无公开课件 | 播放列表 |
| 11-06 | Inference and Hardware | Clara | ❌ 无公开课件 | 播放列表 |
| 11-13 | Draft Models and Speculative Decoding（嘉宾：Beidi Chen） | 嘉宾 | ❌ 无公开课件 | 播放列表 |
| 11-18 | Linearizing Attention and Sparse Models | Amanda | `slides/lecture-1118-linear-attention-sparse.pdf`（43页） | 播放列表 |
| 11-20 | Building MLC-LLM（嘉宾：Tianqi Chen） | 嘉宾 | ❌ 无公开课件 | 播放列表 |
| 11-25 | Library Implementation and Optimizations（vLLM/SGLang 原理） | Graham | ❌ 无公开课件 | 播放列表 |

说明：官网课程表上只有 Amanda 的 7 讲挂了 Slides 链接（Google Slides，已全部导出为 PDF 验证）；
Graham 的讲座和嘉宾讲座没有公开课件。课程表上也没有列出逐讲的阅读材料。

## 作业（说明页：https://www.phontron.com/class/lminference-fall2025/assignments/）

三个共享任务贯穿所有作业：Task 1 数学推理、Task 2 选择题问答、Task 3 开放生成。

| 作业 | 内容 | 占比 |
|---|---|---|
| HW1：Decoding Methods and Probability Review | 概率复习；实现 temperature / top-p / top-k / mirostat 采样；调试 diverse beam search；在共享任务上对比 | 20% |
| HW2：Meta-decoding Methods | Best-of-n、带 reward model 的 Minimum Bayes Risk 解码；self-refine 迭代生成；让 LM 执行 Python 代码（工具增强生成） | 20% |
| HW3：Efficiency | 自己写推理系统：batching、KV cache、speculative decoding、硬件优化；**不许用 vLLM / SGLang 等现成推理服务器**；按吞吐/延迟/精度打分 | 20% |
| Shared Task 期末 | 自己设计 API 推理服务器（固定延迟预算下在共享任务上评测）＋ 4-8 页 COLM 格式技术报告 ＋ 海报展示 | 25% |
| 课堂小测/参与 | 每节课一次，取最低分 drop 掉 3 次 | 15% |

## 代码仓库

- 仓库：https://github.com/neubig/lminference-fall2025-code（已下载到 `code/`，GitHub zip 包，缺 `.git` 目录；在自己电脑上建议 `git clone`）
- 内容：`01-lm-intro/`（FLOP 分析、Qwen 生成实验）、`02-generation-basics/`（采样方法 notebook）、`homework1/`（含作业 PDF `writeup/11_763_HW_1.pdf` 和 starter code：坏掉的 diverse beam search、mirostat）、`homework2/`（含作业 PDF、basic_deepresearch 示例）、`homework3/`、`final-project/example_code/`（推理服务器 starter）
- 已删除：`code/homework2/addendum-release/all_results_processed.json`（43MB 纯结果数据，对学习无用，已删减体积）

## 缺失项说明

1. Graham 讲授的讲座（A* 搜索、CoT、Self-Refine、推理模型、工具、Agents、Diffusion、效率等）和 3 场嘉宾讲座**没有公开课件**，只有 YouTube 录像。
2. 课程表上没有逐讲阅读材料列表。
3. 作业需要的数据集/模型在仓库 writeup 里说明获取方式，部分可能需要 CMU 内部权限。
