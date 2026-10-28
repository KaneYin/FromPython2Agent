# Phase 1.5 Part 3: ReasoningStrategy 抽象 + Function Calling 支持

Phase 1 实现的是 text-based ReAct（工具描述写在 system prompt 里，靠正则解析模型输出）。这一轮我们引入 **ReasoningStrategy 抽象**，让 Agent 能支持两种范式：

1. **TextReActStrategy**：现有实现，整体保留
2. **FunctionCallingStrategy**：新增，使用 OpenAI tools API 原生 function calling

**这一轮的目标不是"替换"，而是"抽象 + 共存"。** 两种 strategy 并存是项目的核心差异化卖点，未来会用来做对比研究。

## 测试环境

主要测试 LLM：**vLLM 部署的 MiniMax 2.5 FP8**。配置示例：

```python
base_url = "http://your-vllm:8000/v1"
api_key = "EMPTY"
model = "MiniMaxAI/MiniMax-M2"  # 或具体部署名
```

注意 quirk（**你的代码必须考虑这些**）：
- vLLM 老版本可能静默忽略 tools 参数
- MiniMax 偶尔同时返回 content 和 tool_calls
- tool_call arguments 偶尔不是严格 JSON（尾随逗号、单引号）

---

## 实现要求

### 1. 新增 microagent/strategies/ 子模块

```
microagent/strategies/
├── __init__.py
├── base.py           # ReasoningStrategy 抽象基类
├── text_react.py     # 把 Phase 1 的实现搬过来
└── function_call.py  # 新增
```

### 2. strategies/base.py

```python
from abc import ABC, abstractmethod
from dataclasses import dataclass

@dataclass
class ParsedStep:
    """统一的解析结果，两种 strategy 都返回这个"""
    thought: str | None              # function calling 模式下可能为 None
    is_final: bool
    final_answer: str | None = None
    
    # 工具调用（list 而非单个，为未来并行准备；Phase 1.5 串行只取 [0]）
    tool_calls: list[ToolCall] | None = None
    
    parse_error: str | None = None


@dataclass
class ToolCall:
    call_id: str | None       # function calling 模式下由 LLM 给定；text 模式下 None
    name: str
    arguments: dict


class ReasoningStrategy(ABC):
    name: str  # "text_react" / "function_call"，用于 trace 标识
    
    @abstractmethod
    def build_request(
        self,
        memory: Memory,
        registry: ToolRegistry,
    ) -> tuple[list[dict], dict]:
        """构建 LLM 请求
        
        返回 (messages, extra_kwargs)
        extra_kwargs 可包含 tools / tool_choice / stop 等
        """
    
    @abstractmethod
    def parse_response(self, response: LLMResponse) -> ParsedStep: ...
    
    @abstractmethod
    def format_assistant_message(self, response: LLMResponse, parsed: ParsedStep) -> dict:
        """把 LLM 响应转成可存入 memory 的 assistant message
        
        text_react: {"role": "assistant", "content": "Thought:..."}
        function_call: {"role": "assistant", "content": null, "tool_calls": [...]}
        """
    
    @abstractmethod
    def format_observation_message(
        self,
        observation: str,
        tool_call: ToolCall,
    ) -> dict:
        """把工具执行结果转成可存入 memory 的 message
        
        text_react: {"role": "user", "content": "Observation: ..."}
        function_call: {"role": "tool", "tool_call_id": "...", "content": "..."}
        """
```

### 3. strategies/text_react.py

把 Phase 1 的实现搬过来，**逻辑完全不变**，只是塞进 strategy 接口里。
- `build_request`：拼接 system prompt + tools 描述 + history，返回 messages + `{"stop": ["Observation:"]}`
- `parse_response`：现有的正则 parser
- `format_assistant_message`：原样把 LLM 输出存为 assistant content
- `format_observation_message`：返回 `{"role": "user", "content": f"Observation: {observation}"}`

### 4. strategies/function_call.py（核心新增）

#### 4.1 build_request

- System prompt **不再包含工具描述**，只保留角色定义（"You are a helpful AI assistant. Use the provided tools when necessary."）
- `extra_kwargs` 里包含 `tools` 字段，从 ToolRegistry 转换：

```python
tools = [
    {
        "type": "function",
        "function": {
            "name": tool.name,
            "description": tool.description,
            "parameters": tool.parameters,
        }
    }
    for tool in registry.list_all()
]
return messages, {"tools": tools, "tool_choice": "auto"}
```

- **不要传 stop 参数**（function calling 模式下模型自己会在 tool_call 后停）

#### 4.2 parse_response（重点处理 quirk）

```python
def parse_response(self, response: LLMResponse) -> ParsedStep:
    raw = response.raw_response  # 完整的 LLM 返回 JSON
    msg = raw["choices"][0]["message"]
    
    tool_calls_raw = msg.get("tool_calls")
    content = msg.get("content")
    
    # Quirk 1: vLLM 老版本不支持，tools 被忽略
    # 如果 content 看起来像 ReAct 格式（含 "Action:"），明确报错
    if tool_calls_raw is None and content and "Action:" in content:
        return ParsedStep(
            thought=None,
            is_final=False,
            parse_error=(
                "Model returned ReAct-style text output instead of tool_calls. "
                "The backend may not support function calling. "
                "Consider switching to TextReActStrategy."
            ),
        )
    
    # 正常 final answer 路径
    if tool_calls_raw is None:
        return ParsedStep(
            thought=None,
            is_final=True,
            final_answer=content or "",
        )
    
    # 解析 tool_calls
    parsed_calls = []
    for tc in tool_calls_raw:
        args_str = tc["function"]["arguments"]
        try:
            args = json.loads(args_str)
        except json.JSONDecodeError:
            # Quirk 2: 国产模型偶发非严格 JSON
            try:
                import ast
                args = ast.literal_eval(args_str)
                if not isinstance(args, dict):
                    raise ValueError("args not a dict")
            except Exception as e:
                return ParsedStep(
                    thought=content,
                    is_final=False,
                    parse_error=f"Cannot parse tool arguments: {args_str!r}, error: {e}",
                )
        
        parsed_calls.append(ToolCall(
            call_id=tc.get("id"),
            name=tc["function"]["name"],
            arguments=args,
        ))
    
    # Quirk 3: MiniMax 偶尔同时返回 content 和 tool_calls
    # 我们把 content 当作 thought 保留（不报错）
    return ParsedStep(
        thought=content,  # 可能为 None
        is_final=False,
        tool_calls=parsed_calls,
    )
```

#### 4.3 format_assistant_message / format_observation_message

按 OpenAI 协议严格构造：

```python
def format_assistant_message(self, response, parsed):
    msg = {
        "role": "assistant",
        "content": parsed.thought,  # 可以是 null
    }
    if parsed.tool_calls:
        msg["tool_calls"] = [
            {
                "id": tc.call_id,
                "type": "function",
                "function": {
                    "name": tc.name,
                    "arguments": json.dumps(tc.arguments, ensure_ascii=False),
                }
            }
            for tc in parsed.tool_calls
        ]
    return msg

def format_observation_message(self, observation, tool_call):
    return {
        "role": "tool",
        "tool_call_id": tool_call.call_id,
        "content": observation,
    }
```

### 5. Agent 主循环改造

`agent.py` 修改：

- `Agent.__init__` 接受 `strategy: ReasoningStrategy` 参数，**默认使用 FunctionCallingStrategy**
- 主循环逻辑改为调用 strategy 方法：

```python
for step in range(max_steps):
    if budget.exceeded(): break
    
    messages, extra_kwargs = strategy.build_request(memory, registry)
    response = llm.chat(messages, **extra_kwargs)
    
    trace.record_think(step, response, strategy_name=strategy.name)
    budget.consume_tokens(...)
    
    parsed = strategy.parse_response(response)
    
    # assistant message 入 memory
    memory.add_raw(strategy.format_assistant_message(response, parsed))
    
    if parsed.parse_error:
        # 错误反馈：以 user role 注入错误信息（两种 strategy 都用这个方式）
        memory.add_raw({"role": "user", "content": f"Error: {parsed.parse_error}"})
        trace.record_observation(...)
        continue
    
    if parsed.is_final:
        trace.record_final(parsed.final_answer)
        return AgentResult(answer=parsed.final_answer, ...)
    
    # 串行执行所有 tool_calls（Phase 1.5 只取 [0]，但代码结构留出未来扩展空间）
    if len(parsed.tool_calls) > 1:
        log.warning(
            f"Got {len(parsed.tool_calls)} tool_calls but executing serially, "
            "only processing the first. Parallel execution coming in Phase 2."
        )
    
    tc = parsed.tool_calls[0]
    
    if tc.name not in registry:
        observation = f"Error: tool '{tc.name}' not found"
    else:
        observation = registry.get(tc.name).invoke(**tc.arguments)
    
    memory.add_raw(strategy.format_observation_message(observation, tc))
    trace.record_action(step, tc.name, tc.arguments, observation, tool_call_id=tc.call_id)
    budget.consume_step()
```

**关键变化**：
- Memory 提供 `add_raw(message: dict)` 方法，因为 function calling 模式下 message 结构更复杂
- 旧的 `add_user / add_assistant / add_observation` 方法保留（向后兼容），内部转调 `add_raw`
- Trace 的 think 事件加 `strategy_name` 字段

### 6. quickstart.py 改造

提供两个示例：

```python
# Example 1: Function calling (default)
agent_fc = Agent(llm=llm, tools=registry)
result_fc = agent_fc.run("123 * 456 等于多少？")
print(result_fc.trace.to_markdown())

# Example 2: Text ReAct (explicit)
from microagent.strategies import TextReActStrategy
agent_text = Agent(llm=llm, tools=registry, strategy=TextReActStrategy())
result_text = agent_text.run("123 * 456 等于多少？")
print(result_text.trace.to_markdown())
```

### 7. 对比测试脚本

新建 `examples/compare_strategies.py`：

```python
queries = [
    "你好",
    "123 * 456 等于多少？",
    "先算 12 * 8，再把结果加 100",
    "现在几点？",
    "帮我算 sqrt(-1)",
    "统计'hello world'有几个单词，再告诉我现在时间",
]

for q in queries:
    print(f"\n{'='*60}\nQuery: {q}\n{'='*60}")
    
    for strategy_cls in [FunctionCallingStrategy, TextReActStrategy]:
        agent = Agent(llm=llm, tools=registry, strategy=strategy_cls())
        result = agent.run(q)
        print(f"\n[{strategy_cls.__name__}]")
        print(f"  finished: {result.finished}")
        print(f"  steps: {len(result.trace.events_of_type('think'))}")
        print(f"  total_tokens: {result.trace.summary()['total_tokens']}")
        print(f"  answer: {result.answer[:100] if result.answer else 'N/A'}")
```

这个对比数据**就是 DESIGN_NOTES.md 的核心素材**，跑完把输出贴给我。

### 8. Trace 适配

`trace.py` 修改：
- think 事件加 `strategy_name` 字段
- action 事件加 `tool_call_id` 字段（function calling 才有）
- to_markdown 在每个 trace 头部显示用的 strategy：`**Strategy**: function_call`

---

## 完成标准

1. 两个 strategy 实现完整，跑同一个 query 都能得到合理结果
2. `compare_strategies.py` 跑通，输出对比数据
3. function calling 在 vLLM + MiniMax 上能正确触发 tool_calls
4. 老的 quickstart.py 仍能跑（向后兼容）
5. 所有单元测试通过

---

## 不要做的事

- ❌ 不要做并行 tool 执行（Phase 2 再做）
- ❌ 不要重构 Tool / ToolRegistry（接口不变）
- ❌ 不要碰前端 viewer 模块
- ❌ 不要加 retry / streaming
- ❌ 不要把 strategy 选择搞成"自动判断"，必须显式指定
