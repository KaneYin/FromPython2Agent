"""【中文导读】microagent 的核心：Agent 主循环。

一次 run(query) 就是 ReAct 论文 (Yao et al., 2022, arXiv:2210.03629) 描述的循环：
    Thought（思考） → Action（选工具并执行） → Observation（把工具结果喂回模型） → … → Final Answer

代码里的一个 step 对应一次"模型调用 + 工具执行"：
  a. 先检查预算（最大步数 / token 上限，防止死循环烧钱）→ 超了就停
  b/c. strategy 把 memory 组装成 messages 发给 LLM
  d. strategy 解析模型输出（FunctionCalling 策略走 OpenAI tool_calls；
     Reasoning 策略走 parser.py 的 Thought/Action 文本协议）
  e-g. 记 trace（可观测性：每步的思考、token、耗时）→ 把 assistant 消息存入 memory
  h. 解析失败 → 把错误信息当 user 消息喂回去，让模型自己纠正后重试
  i. 模型输出 Final Answer → 结束
  j-n. 否则执行工具调用，把 observation 存回 memory，下一轮模型能看到结果
  p/q. 通知 strategy 本轮结束，消耗一步预算

关键设计（对应课程 Lecture 2/3 的知识点）：
- Budget：步数和 token 双预算，是所有生产级 agent 的标配；
- Memory：对话历史的统一存储，strategy 决定怎么把它变成 prompt；
- Trace：完整记录每一步，是"可观测性 / observability"最简实现，排查 agent
  行为全靠它。

官方文档：OpenAI Function Calling https://platform.openai.com/docs/guides/function-calling
"""

from __future__ import annotations

import os
import time
from dataclasses import dataclass

from .budget import Budget
from .llm import LLMClient
from .memory import Memory
from .strategies import FunctionCallingStrategy, ReasoningStrategy
from .tools.base import ToolRegistry
from .trace import Trace, TraceEvent


@dataclass
class AgentResult:
    answer: str | None
    trace: Trace
    finished: bool
    stop_reason: str  # "final_answer" | "max_steps" | "max_tokens"


def _normalize_tokens(usage: dict) -> dict:
    return {
        "prompt": usage.get("prompt_tokens", 0),
        "completion": usage.get("completion_tokens", 0),
        "total": usage.get("total_tokens", 0),
    }


class Agent:
    def __init__(
        self,
        llm: LLMClient,
        tools: ToolRegistry,
        memory: Memory | None = None,
        budget: Budget | None = None,
        strategy: ReasoningStrategy | None = None,
    ):
        self.llm = llm
        self.tools = tools
        self.memory = memory or Memory()
        self.budget = budget or Budget()
        self.strategy = strategy or FunctionCallingStrategy()

    def _finalize_trace(self, trace: Trace) -> None:
        trace.llm_calls = self.llm.get_records()

    def _validate_message_sequence(self, step: int) -> None:
        if os.environ.get("MICROAGENT_DEBUG") != "1":
            return
        msgs = self.memory.to_messages()
        if len(msgs) < 2:
            return
        last = msgs[-1]
        # find the last assistant message
        assistant_idx = None
        for i in range(len(msgs) - 1, -1, -1):
            if msgs[i].get("role") == "assistant" and msgs[i].get("tool_calls"):
                assistant_idx = i
                break
        if assistant_idx is None:
            return
        assistant_msg = msgs[assistant_idx]
        expected_ids = [
            tc["id"] for tc in assistant_msg.get("tool_calls", [])
            if tc.get("id")
        ]
        if not expected_ids:
            return
        actual_msgs = msgs[assistant_idx + 1: assistant_idx + 1 + len(expected_ids)]
        actual_ids = [
            m.get("tool_call_id") for m in actual_msgs
            if m.get("role") == "tool"
        ]
        if actual_ids != expected_ids:
            import logging
            logging.warning(
                f"[Step {step}] Protocol violation: expected tool_call_ids "
                f"{expected_ids}, got {actual_ids}"
            )

    def run(self, query: str) -> AgentResult:
        self.memory.clear()
        self.llm.clear_records()
        if hasattr(self.strategy, "reset"):
            self.strategy.reset()
        trace = Trace()
        trace.set_query(query)
        trace.set_strategy(self.strategy.name)
        self.memory.add_user(query)

        for step in range(1, self.budget.max_steps + 1):
            # a. check budget
            exceeded, reason = self.budget.exceeded()
            if exceeded:
                stop_reason = "max_tokens" if "token" in (reason or "") else "max_steps"
                trace.add(TraceEvent(
                    step=step, type="budget_exceeded",
                    timestamp=time.time(), content={"reason": reason},
                ))
                self._finalize_trace(trace)
                return AgentResult(
                    answer=None, trace=trace, finished=False,
                    stop_reason=stop_reason,
                )

            # b. build messages via strategy
            messages, extra_kwargs = self.strategy.build_request(self.memory, self.tools)

            # c. call LLM
            response = self.llm.chat(messages, **extra_kwargs)
            latest_record = self.llm.get_records()[-1]

            # d. parse via strategy
            parsed = self.strategy.parse_response(response)

            # e. trace think event
            think_content: dict = {
                "thought": parsed.thought,
                "raw": response.content,
            }
            if parsed.parse_error:
                think_content["parse_error"] = parsed.parse_error
            if parsed.is_final:
                think_content["final_answer"] = parsed.final_answer
            if parsed.tool_calls:
                think_content["tool_calls"] = [
                    {"name": tc.name, "arguments": tc.arguments}
                    for tc in parsed.tool_calls
                ]
            # PlanExecute: inject plan info for trace rendering
            if hasattr(self.strategy, "plan_phase"):
                think_content["plan_phase"] = self.strategy.plan_phase
                if self.strategy.plan_phase == "planning" and self.strategy.plan_steps:
                    think_content["plan"] = [
                        f"{s.index}. {s.description}" for s in self.strategy.plan_steps
                    ]
                if self.strategy.plan_phase == "executing" and self.strategy.current_step_info:
                    think_content["plan_step_info"] = self.strategy.current_step_info
            trace.add(TraceEvent(
                step=step, type="think",
                timestamp=time.time(),
                content=think_content,
                tokens=_normalize_tokens(response.usage),
                latency_ms=response.latency_ms,
                llm_call_id=latest_record.call_id,
                strategy_name=self.strategy.name,
            ))

            # f. budget consume tokens
            self.budget.consume_tokens(response.usage.get("total_tokens", 0))

            # g. add assistant message to memory
            self.memory.add_raw(
                self.strategy.format_assistant_message(response, parsed)
            )

            # h. parse error -> feed back
            if parsed.parse_error:
                error_msg = f"Error: {parsed.parse_error}"
                self.memory.add_raw({"role": "user", "content": error_msg})
                trace.add(TraceEvent(
                    step=step, type="observation",
                    timestamp=time.time(), content={"text": error_msg},
                ))
                continue

            # i. final answer
            if parsed.is_final:
                trace.add(TraceEvent(
                    step=step, type="final",
                    timestamp=time.time(),
                    content={"answer": parsed.final_answer},
                ))
                self._finalize_trace(trace)
                return AgentResult(
                    answer=parsed.final_answer, trace=trace,
                    finished=True, stop_reason="final_answer",
                )

            # j. execute tool calls (serial, all tool_calls in sequence)
            if not parsed.tool_calls:
                # PlanExecute: empty tool_calls means plan phase done, skip to next turn
                if hasattr(self.strategy, "on_step_completed"):
                    pass  # no tools ran, no observations
                continue

            for tc in parsed.tool_calls:
                # k. tool not found
                if self.tools.get(tc.name) is None:
                    tool_names = ", ".join(self.tools.tool_names)
                    observation = f"Error: tool '{tc.name}' not found. Available: {tool_names}"
                else:
                    observation = self.tools.get(tc.name).invoke(**tc.arguments)

                # l. log tool call
                logger = getattr(self.llm, "logger", None)
                if logger:
                    logger.log_tool_call(
                        tool_name=tc.name,
                        tool_input=tc.arguments,
                        tool_output=observation,
                    )

                # m. add observation to memory via strategy
                self.memory.add_raw(
                    self.strategy.format_observation_message(observation, tc)
                )

                # n. trace action + observation
                trace.add(TraceEvent(
                    step=step, type="action",
                    timestamp=time.time(),
                    content={
                        "action": tc.name,
                        "action_input": tc.arguments,
                    },
                    tool_call_id=tc.call_id,
                ))
                trace.add(TraceEvent(
                    step=step, type="observation",
                    timestamp=time.time(), content={"text": observation},
                ))

            # o. validate message sequence in debug mode
            self._validate_message_sequence(step)

            # p. notify strategy of step completion
            step_observations = [
                e.content.get("text", "") for e in trace.events
                if e.step == step and e.type == "observation"
            ]
            if hasattr(self.strategy, "on_step_completed"):
                self.strategy.on_step_completed(step_observations)

            # q. consume step (once per LLM turn, not per tool_call)
            self.budget.consume_step()

        # loop ended without final answer
        self._finalize_trace(trace)
        return AgentResult(
            answer=None, trace=trace, finished=False,
            stop_reason="max_steps",
        )
