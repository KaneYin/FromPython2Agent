# assignment-1 学习笔记（11-768 Assignment 1: Build an Agent Harness）

> 上游仓库：https://github.com/cmu-agents/assignment-1（CMU 11-768《AI Agents》课程作业 1，starter code）

## 这个仓库实现了什么

**一句话**：从零搭建一个领域无关的 ReAct agent harness（含工具执行、Skill 加载、上下文压缩），并用它完成修 bug（SWE-Bench 风格）和下国际象棋两个任务。

**一段话**：这个仓库不是"调库做 agent"，而是"手写 agent 框架本身"。你需要实现的核心是一个通用 ReAct 循环：拼 prompt → 调 LLM（带 tools）→ 执行 tool call → 把 observation 拼回 prompt → 重复。作业分三部分：Part 1 实现 `Agent.run()` 等主循环，做成 `CodeAgent` 在终端修 chess app 的 bug 并产出 git patch，再用同样的 harness 去解 SWE-Bench 的 django 实例；Part 2 实现上下文压缩（context compaction），让模型自己总结旧轨迹以节省 token；Part 3 实现 `ChessAgent`，定义 `play_move` 等工具让 LLM 在修好的棋盘上和规则 bot 下棋，还探索了"用 Python 代码做程序化走子搜索"（simulate + run_python）。配套有完整评测脚本（把 patch 打到测试镜像里跑 pytest 判分）。

## 核心文件

| 文件 | 作用 |
|---|---|
| `src/assignment/agent/base.py` | 核心！领域无关的 ReAct 基类 `Agent`。`build_prompt()`（待实现）、`run()` 主循环（待实现）、`query_language_model()`（已给）、`compact_context()`（Part 2 待实现）都在这里 |
| `src/assignment/agent/code_agent.py` | `CodeAgent(Agent)`：修软件 issue 的子类，提供 `execute`（终端执行）和 `send_message` 工具，产出 fix patch |
| `src/assignment/agent/chess_agent.py` | `ChessAgent(Agent)`：下棋的子类 |
| `src/assignment/agent/chess_tools.py` | 下棋工具的 tool schema 定义（`play_move` 等） |
| `src/assignment/agent/tools.py` | 通用工具定义（`EXECUTE_TOOL`、`SEND_MESSAGE_TOOL`、`INVOKE_SKILL_TOOL`） |
| `src/assignment/prompts.py` | Prompt 模板（Jinja2）：象棋 system prompt、程序化走子搜索的 prompt |
| `src/assignment/env.py` / `chess_sandbox.py` / `sandbox_python.py` | 环境抽象：Modal 云沙箱里执行 agent 生成的代码 |
| `src/assignment/eval/harness.py` | 评测脚本：把 patch 应用到测试镜像，解析 `pytest -rA` 输出，按 fail_to_pass / pass_to_pass 判分 |
| `src/assignment/cli.py` | 三个命令行入口：`assignment-code-agent` / `assignment-swebench-agent` / `assignment-play-chess` |
| `scripts/evaluate.py` / `evaluate_swebench.py` | 评测入口脚本 |
| `ASSIGNMENT.md` | 作业说明全文（环境、计费、规则、三个 Part 的任务） |
| `tasks/` | 任务定义：`chess-terminal-move`（修棋 bug）、`swebench/django__django-15368`、skills（`SKILL.md` 格式） |
| `Makefile` | 常用命令封装（setup / test / run-code-agent / run-chess-agent / 观察消融实验等） |

## 怎么运行

依赖：`uv`、Modal 账号（云端沙箱）、OpenAI 兼容的 LLM API（课程默认 `deepseek/deepseek-v4-flash-0731`）。

```bash
make setup            # uv sync + 初始化 chess_app 子模块
uv run modal setup    # 登录 Modal（代码在云端沙箱执行）
cp .env.example .env  # 填 OPENAI_BASE_URL / OPENAI_API_KEY / OPENAI_MODEL
make doctor           # 不花钱的预检：子模块、Modal 鉴权、模型 endpoint
make test             # 离线单测（starter 故意 fail，标出 TODO 里程碑）

# 跑起来（花钱：Modal + LLM）
make run-code-agent   # CodeAgent 修 chess bug → artifacts/fix.patch
make check-part1      # 把 patch 打到测试镜像里跑公开测试判分
make run-chess-agent  # ChessAgent 在修好的棋盘上和 bot 下棋
```

## 关键设计点

1. **领域无关的 ReAct 循环**：`Agent` 基类只管"拼 prompt → 调模型 → 执行 tool call → 拼 observation"这个循环；`CodeAgent` / `ChessAgent` 子类只提供自己的 system prompt 和工具执行器。想清楚"通用循环"和"领域逻辑"的分界是这份作业最大的学习点。
2. **原生 tool calling，不是文本解析**：用 OpenAI Chat Completions 的 `tools` 参数，`process_response` 取 `choices[0].message`，工具结果以 `role: "tool"` 消息拼回，避免了 ReAct 论文里 Thought/Action 文本正则解析的脆弱性。
3. **Skill 机制**：`tasks/code-skills` 下每个子目录一个 `SKILL.md`（YAML frontmatter + markdown），`load_skills` 校验重名/格式后注入 prompt，并暴露统一的 `invoke_skill` 工具——相当于给 agent 的"可复用 playbook"。
4. **Context compaction（Part 2）**：超过 token 阈值时，让模型自己把旧轨迹压缩成"目标、已做工作、失败尝试、下一步"的工作记忆，保留最新 assistant action 原样。`maybe_compact_context()` 在每次调模型前检查。
5. **Observation 截断与失败可恢复**：工具输出超 10000 字符时头尾保留 + 省略标记；`execute_tool_calls` 里未知工具/坏 JSON 变成 observation 返回给模型而不是抛异常，让 agent 能自我纠错。
6. **轨迹即证据**：`run()` 的 finally 块保证每次运行都落盘 `prompts/responses/compactions` 三段 JSON，评测和 debug 都靠它。
