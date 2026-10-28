# Phase 2.3: 多工具扩展

新增三个生产级工具：Bash 执行、Web 搜索、文件读写。每个工具都要有完善的安全限制和错误处理。

## 工具 1: Bash 执行器

文件：`microagent/tools/bash.py`

### 安全限制（硬性要求，不可省略）

```python
BLOCKED_COMMANDS = [
    "rm", "rmdir", "del", "format", "mkfs",      # 删除/格式化
    "sudo", "su", "chmod", "chown",               # 权限提升
    "curl", "wget", "nc", "netcat",               # 网络（Phase 2.3 不开放）
    "python", "python3", "pip",                   # 防止递归调用自身
    ">", ">>",                                     # 重定向写文件（File IO 工具负责）
]

ALLOWED_ENV = {
    "PATH": "/usr/bin:/bin",  # Linux；Windows 另处理
    "HOME": "/tmp/microagent_sandbox",
}

MAX_OUTPUT_CHARS = 2000   # 超出截断，加提示 "[output truncated]"
TIMEOUT_SECONDS = 10
```

### 实现要点

```python
@dataclass
class BashTool(Tool):
    name = "bash"
    description = """Execute a bash command and return its output. 
Use for: listing files, checking system info, running scripts, text processing with grep/awk/sed.
Do NOT use for: file writes (use file_write), web requests (use web_search), anything requiring sudo."""
    parameters = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "The bash command to execute"
            }
        },
        "required": ["command"]
    }
    
    def _is_safe(self, command: str) -> tuple[bool, str]:
        """返回 (is_safe, reason)"""
        for blocked in BLOCKED_COMMANDS:
            # 用 shlex.split 解析后检查，不要字符串 contains（防绕过）
            ...
        return True, ""
    
    def invoke(self, command: str) -> str:
        is_safe, reason = self._is_safe(command)
        if not is_safe:
            return f"Error: Command blocked for safety: {reason}"
        
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
                env=ALLOWED_ENV,
            )
            output = result.stdout + result.stderr
            if len(output) > MAX_OUTPUT_CHARS:
                output = output[:MAX_OUTPUT_CHARS] + "\n[output truncated]"
            return output or "(no output)"
        except subprocess.TimeoutExpired:
            return f"Error: Command timed out after {TIMEOUT_SECONDS}s"
        except Exception as e:
            return f"Error: {type(e).__name__}: {e}"
```

**Windows 兼容**：`shell=True` 在 Windows 上用 cmd.exe，`ALLOWED_ENV` 在 Windows 上设为 `None`（继承当前环境，不做限制——Windows 沙箱留到 Phase 3）。用 `sys.platform` 判断。

---

## 工具 2: Web 搜索（Tavily）

文件：`microagent/tools/web_search.py`

### 实现要点

- 用 `httpx` 直接调 Tavily API（不要引入 `tavily-python` SDK）
- API endpoint: `https://api.tavily.com/search`
- API key 从环境变量 `TAVILY_API_KEY` 读取

```python
parameters = {
    "type": "object",
    "properties": {
        "query": {
            "type": "string",
            "description": "The search query"
        },
        "max_results": {
            "type": "integer",
            "description": "Maximum number of results to return (1-5, default 3)",
            "default": 3
        }
    },
    "required": ["query"]
}
```

返回格式（给 LLM 看的，要简洁）：

```
[1] Title: <title>
    URL: <url>
    Summary: <content 前 200 字>

[2] ...
```

错误处理：
- API key 未设置 → `"Error: TAVILY_API_KEY not set"`
- 网络超时（设 10s）→ `"Error: Search timed out"`
- 非 200 响应 → `"Error: Search API returned {status_code}"`

---

## 工具 3: 文件读写

文件：`microagent/tools/file_io.py`

**两个独立工具**：`file_read` 和 `file_write`（不要合并成一个）。

### 安全限制

```python
SANDBOX_DIR = Path.home() / ".microagent" / "sandbox"
MAX_FILE_SIZE = 50 * 1024  # 50KB，超出拒绝读取
MAX_WRITE_SIZE = 10 * 1024  # 10KB，超出拒绝写入
```

所有路径操作必须做 sandbox 检查：

```python
def _safe_path(self, path: str) -> tuple[Path, str | None]:
    """返回 (resolved_path, error_msg)"""
    target = (SANDBOX_DIR / path).resolve()
    if not str(target).startswith(str(SANDBOX_DIR.resolve())):
        return None, "Error: Path traversal not allowed"
    return target, None
```

### file_read

```python
parameters = {
    "type": "object", 
    "properties": {
        "path": {"type": "string", "description": "File path relative to sandbox directory"},
        "encoding": {"type": "string", "description": "File encoding, default utf-8"}
    },
    "required": ["path"]
}
```

返回文件内容（超过 MAX_FILE_SIZE 返回错误，不要截断——截断会给 LLM 不完整信息）。

### file_write

```python
parameters = {
    "type": "object",
    "properties": {
        "path": {"type": "string", "description": "File path relative to sandbox directory"},
        "content": {"type": "string", "description": "Content to write"},
        "mode": {"type": "string", "description": "'overwrite' or 'append', default 'overwrite'"}
    },
    "required": ["path", "content"]
}
```

写入前自动创建 SANDBOX_DIR（如果不存在）。返回：`"Written N bytes to {path}"`。

---

## 注册到 quickstart

`examples/quickstart.py` 注册全部 5 个工具（calculator / text_stats / datetime_now / bash / web_search / file_read / file_write）。

**注意**：web_search 只在 `TAVILY_API_KEY` 环境变量存在时注册，否则跳过并打印提示。

---

## 验证脚本

新建 `examples/phase2.3/test_tools.py`，跑以下 case，每个用 FC strategy：

```python
test_cases = [
    # Bash
    ("bash_basic", "用 bash 列出当前目录有哪些文件"),
    ("bash_blocked", "用 bash 运行 rm -rf /"),  # 应该被拦截
    
    # Web Search  
    ("web_search", "搜索一下 2025 年图灵奖得主是谁"),
    
    # File IO
    ("file_write", "创建一个文件 hello.txt，内容是 'Hello MicroAgent'"),
    ("file_read", "读取 hello.txt 的内容"),
    ("file_traversal", "读取 ../../etc/passwd"),  # 应该被拦截
    
    # 多工具组合
    ("multi_tool", "搜索 Python 最新版本，然后把结果写入 python_version.txt"),
]
```

每个 case 输出：`query | finished | steps | answer 前 100 字 | 安全拦截是否生效`

---

## 不要做的事

- ❌ 不要引入 `tavily-python` SDK，用 httpx 直接调
- ❌ Bash 工具不要做 Docker 沙箱（Phase 3 的事）
- ❌ file_read / file_write 不要允许 sandbox 目录外的路径
- ❌ 不要把三个工具合并成一个"万能工具"
- ❌ 不要修改现有 strategy 实现

## 完成标准

1. 7 个 test case 全部跑通，安全拦截 case 返回 Error 而不是执行
2. web_search 能返回真实搜索结果
3. file_read 能读到 file_write 写的文件
4. 原有测试全绿

完成后把 test_tools.py 的输出贴给我。