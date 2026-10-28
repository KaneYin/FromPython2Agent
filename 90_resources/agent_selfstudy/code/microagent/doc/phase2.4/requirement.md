# Phase 2.4: MCP Client（stdio transport）

新增 MCP client 支持，让 Agent 能把外部 MCP server 暴露的工具无缝接入现有 ToolRegistry。Agent 主循环不做任何改动。

## 文件结构

```
microagent/
└── mcp/
    ├── __init__.py
    ├── client.py      # MCPClient：进程管理 + JSON-RPC 通信
    ├── adapter.py     # 把 MCP 工具转成 Tool 对象
    └── registry.py    # MCPToolRegistry：管理多个 MCP server
```

---

## 1. client.py：MCPClient

### 职责
- 启动/停止 MCP server 子进程
- 发送 JSON-RPC 请求，读取响应
- 实现 initialize / tools/list / tools/call 三个方法

### 实现

```python
@dataclass
class MCPServerConfig:
    name: str                    # 标识符，如 "filesystem"
    command: list[str]           # 启动命令，如 ["npx", "@modelcontextprotocol/server-filesystem", "/tmp"]
    env: dict[str, str] | None = None  # 额外环境变量

class MCPClient:
    def __init__(self, config: MCPServerConfig):
        self._config = config
        self._process: subprocess.Popen | None = None
        self._request_id: int = 0
        self._initialized: bool = False
    
    def start(self) -> None:
        """启动子进程，完成 initialize 握手"""
        self._process = subprocess.Popen(
            self._config.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # stderr 单独捕获，不污染 stdout
            text=True,
            env={**os.environ, **(self._config.env or {})},
        )
        self._initialize()
    
    def stop(self) -> None:
        """发 shutdown 通知，终止子进程"""
        if self._process:
            try:
                self._send_notification("notifications/cancelled", {})
            except Exception:
                pass
            self._process.terminate()
            self._process.wait(timeout=5)
            self._process = None
    
    def __enter__(self): self.start(); return self
    def __exit__(self, *args): self.stop()
    
    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id
    
    def _send_request(self, method: str, params: dict) -> dict:
        """发送 JSON-RPC request，阻塞等待对应 id 的 response"""
        req_id = self._next_id()
        request = {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params,
        }
        line = json.dumps(request, ensure_ascii=False) + "\n"
        self._process.stdin.write(line)
        self._process.stdin.flush()
        
        # 读响应，跳过不匹配 id 的行（server 可能发 notification）
        while True:
            raw = self._process.stdout.readline()
            if not raw:
                raise MCPError("MCP server closed stdout unexpectedly")
            try:
                resp = json.loads(raw)
            except json.JSONDecodeError:
                continue  # 跳过非 JSON 行
            if resp.get("id") == req_id:
                if "error" in resp:
                    raise MCPError(f"MCP error: {resp['error']}")
                return resp.get("result", {})
    
    def _send_notification(self, method: str, params: dict) -> None:
        """发送 JSON-RPC notification（无需响应）"""
        notif = {"jsonrpc": "2.0", "method": method, "params": params}
        self._process.stdin.write(json.dumps(notif) + "\n")
        self._process.stdin.flush()
    
    def _initialize(self) -> None:
        result = self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "microagent", "version": "0.1.0"},
        })
        # 发 initialized notification（MCP 协议要求）
        self._send_notification("notifications/initialized", {})
        self._initialized = True
    
    def list_tools(self) -> list[dict]:
        """返回原始 MCP tool schema 列表"""
        result = self._send_request("tools/list", {})
        return result.get("tools", [])
    
    def call_tool(self, name: str, arguments: dict) -> str:
        """调用工具，返回字符串结果"""
        result = self._send_request("tools/call", {
            "name": name,
            "arguments": arguments,
        })
        # MCP result.content 是 list[{type, text}]
        contents = result.get("content", [])
        parts = [c["text"] for c in contents if c.get("type") == "text"]
        return "\n".join(parts) if parts else "(no output)"


class MCPError(Exception):
    pass
```

**关键点**：
- stderr 必须单独捕获，否则 server 的日志会污染 stdout 的 JSON-RPC 流
- `_send_request` 要跳过不匹配 id 的行（server 可能主动发 notification）
- `__enter__/__exit__` 支持 with 语句，保证进程被清理

---

## 2. adapter.py：MCP 工具 → Tool 对象

```python
def mcp_tool_to_tool(client: MCPClient, mcp_schema: dict) -> Tool:
    """把 MCP tools/list 返回的单个工具 schema 转成 Tool 对象"""
    
    def invoke(**kwargs) -> str:
        try:
            return client.call_tool(mcp_schema["name"], kwargs)
        except MCPError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error: {type(e).__name__}: {e}"
    
    return Tool(
        name=mcp_schema["name"],
        description=mcp_schema.get("description", ""),
        parameters=mcp_schema.get("inputSchema", {"type": "object", "properties": {}}),
        func=invoke,
    )


def register_mcp_server(
    client: MCPClient,
    registry: ToolRegistry,
    prefix: str | None = None,
) -> list[str]:
    """发现并注册一个 MCP server 的所有工具，返回注册的工具名列表
    
    prefix: 如果设置，工具名变成 "{prefix}_{name}"，避免多 server 冲突
    """
    tools = client.list_tools()
    registered = []
    for mcp_tool in tools:
        tool = mcp_tool_to_tool(client, mcp_tool)
        if prefix:
            tool.name = f"{prefix}_{tool.name}"
        registry.register(tool)
        registered.append(tool.name)
    return registered
```

---

## 3. registry.py：MCPToolRegistry

管理多个 MCP server 的生命周期：

```python
class MCPToolRegistry:
    """管理多个 MCPClient 的生命周期，统一注册到 ToolRegistry"""
    
    def __init__(self, tool_registry: ToolRegistry):
        self._tool_registry = tool_registry
        self._clients: dict[str, MCPClient] = {}
    
    def add_server(
        self,
        config: MCPServerConfig,
        prefix: str | None = None,
        auto_prefix: bool = True,
    ) -> list[str]:
        """启动 MCP server，注册其工具，返回注册的工具名列表
        
        auto_prefix=True 时，如果不指定 prefix，用 config.name 作为前缀
        """
        effective_prefix = prefix if prefix is not None else (config.name if auto_prefix else None)
        client = MCPClient(config)
        client.start()
        self._clients[config.name] = client
        return register_mcp_server(client, self._tool_registry, prefix=effective_prefix)
    
    def remove_server(self, name: str) -> None:
        if name in self._clients:
            self._clients[name].stop()
            del self._clients[name]
    
    def stop_all(self) -> None:
        for client in self._clients.values():
            client.stop()
        self._clients.clear()
    
    def __enter__(self): return self
    def __exit__(self, *args): self.stop_all()
```

---

## 4. 验证脚本

新建 `examples/phase2.4/test_mcp.py`。

**测试用 MCP server**：用官方的 `@modelcontextprotocol/server-filesystem`（需要 npx）。

如果环境没有 node/npx，用一个**内置的 mock MCP server**代替：

```python
# examples/phase2.4/mock_mcp_server.py
# 一个极简的 MCP server，用 Python 实现，暴露两个工具：
# - echo: 原样返回输入
# - add: 两数相加

import sys, json

def handle(request):
    method = request.get("method")
    req_id = request.get("id")
    
    if method == "initialize":
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "mock-server", "version": "0.1.0"},
        }}
    
    elif method == "notifications/initialized":
        return None  # notification，不回复
    
    elif method == "tools/list":
        return {"jsonrpc": "2.0", "id": req_id, "result": {"tools": [
            {
                "name": "echo",
                "description": "Echo back the input text",
                "inputSchema": {
                    "type": "object",
                    "properties": {"text": {"type": "string"}},
                    "required": ["text"],
                }
            },
            {
                "name": "add",
                "description": "Add two numbers",
                "inputSchema": {
                    "type": "object",
                    "properties": {
                        "a": {"type": "number"},
                        "b": {"type": "number"},
                    },
                    "required": ["a", "b"],
                }
            },
        ]}}
    
    elif method == "tools/call":
        params = request.get("params", {})
        name = params.get("name")
        args = params.get("arguments", {})
        
        if name == "echo":
            text = args.get("text", "")
            result_text = f"Echo: {text}"
        elif name == "add":
            result_text = str(args.get("a", 0) + args.get("b", 0))
        else:
            result_text = f"Unknown tool: {name}"
        
        return {"jsonrpc": "2.0", "id": req_id, "result": {
            "content": [{"type": "text", "text": result_text}]
        }}

for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        request = json.loads(line)
        response = handle(request)
        if response is not None:
            print(json.dumps(response), flush=True)
    except Exception as e:
        print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"message": str(e)}}), flush=True)
```

测试脚本：

```python
# examples/phase2.4/test_mcp.py

from microagent.mcp import MCPServerConfig, MCPToolRegistry
from microagent.tools import ToolRegistry

registry = ToolRegistry()

config = MCPServerConfig(
    name="mock",
    command=["python", "examples/phase2.4/mock_mcp_server.py"],
)

with MCPToolRegistry(registry) as mcp_registry:
    registered = mcp_registry.add_server(config)
    print(f"Registered tools: {registered}")
    
    # 验证工具注册成功
    assert "mock_echo" in registered
    assert "mock_add" in registered
    
    # 用 Agent 跑两个 query
    agent = Agent(llm=llm, tools=registry)
    
    r1 = agent.run("用 echo 工具把 'hello MCP' 回传给我")
    print(f"echo: {r1.answer}")
    assert "hello MCP" in r1.answer
    
    r2 = agent.run("用 add 工具算 123 加 456")
    print(f"add: {r2.answer}")
    assert "579" in r2.answer
    
    print("All assertions passed.")
```

---

## 不要做的事

- ❌ 不要实现 SSE / HTTP transport（Phase 3 的事）
- ❌ 不要做工具名冲突的自动解决（prefix 机制够用）
- ❌ 不要修改 Agent 主循环
- ❌ 不要引入任何 MCP SDK（`mcp` 包之类），纯手撸

## 完成标准

1. mock_mcp_server.py 能独立运行（手动测 stdin/stdout）
2. test_mcp.py 跑通，两个 assertion 通过
3. MCPToolRegistry 的 with 语句能正确清理子进程
4. 原有测试全绿
