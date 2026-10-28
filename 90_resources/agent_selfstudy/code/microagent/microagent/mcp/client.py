"""MCPClient — manage an MCP server subprocess via stdio JSON-RPC."""
from __future__ import annotations

import json
import os
import subprocess
from dataclasses import dataclass, field


class MCPError(Exception):
    """Error from MCP server communication."""
    pass


@dataclass
class MCPServerConfig:
    """Configuration for launching an MCP server."""

    name: str  # identifier, e.g. "filesystem"
    command: list[str]  # launch command, e.g. ["npx", "@modelcontextprotocol/server-filesystem", "/tmp"]
    env: dict[str, str] | None = None  # extra environment variables


class MCPClient:
    """Manages a single MCP server subprocess with stdio JSON-RPC."""

    def __init__(self, config: MCPServerConfig) -> None:
        self._config = config
        self._process: subprocess.Popen | None = None
        self._request_id: int = 0
        self._initialized: bool = False

    # ── Lifecycle ──────────────────────────────────────────────────

    def start(self) -> None:
        """Start the subprocess and complete the initialize handshake."""
        env = {**os.environ, **(self._config.env or {})}
        self._process = subprocess.Popen(
            self._config.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,  # stderr captured separately to avoid polluting stdout
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
        )
        self._initialize()

    def stop(self) -> None:
        """Terminate the subprocess gracefully."""
        if self._process:
            try:
                self._send_notification("notifications/cancelled", {})
            except Exception:
                pass
            try:
                self._process.terminate()
                self._process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait(timeout=3)
            self._process = None

    def __enter__(self) -> MCPClient:
        self.start()
        return self

    def __exit__(self, *args) -> None:
        self.stop()

    # ── JSON-RPC ───────────────────────────────────────────────────

    def _next_id(self) -> int:
        self._request_id += 1
        return self._request_id

    def _send_request(self, method: str, params: dict) -> dict:
        """Send a JSON-RPC request and block until the matching response arrives."""
        if self._process is None or self._process.stdin is None or self._process.stdout is None:
            raise MCPError("MCP server is not running")

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

        # Read responses, skipping lines that don't match our request id
        # (the server may send notifications or responses to other requests)
        while True:
            raw = self._process.stdout.readline()
            if not raw:
                raise MCPError("MCP server closed stdout unexpectedly")
            raw = raw.strip()
            if not raw:
                continue
            try:
                resp = json.loads(raw)
            except json.JSONDecodeError:
                continue  # skip non-JSON lines
            if resp.get("id") == req_id:
                if "error" in resp:
                    raise MCPError(f"MCP error: {resp['error']}")
                return resp.get("result", {})

    def _send_notification(self, method: str, params: dict) -> None:
        """Send a JSON-RPC notification (no response expected)."""
        if self._process is None or self._process.stdin is None:
            raise MCPError("MCP server is not running")
        notif = {"jsonrpc": "2.0", "method": method, "params": params}
        self._process.stdin.write(json.dumps(notif) + "\n")
        self._process.stdin.flush()

    # ── MCP protocol methods ───────────────────────────────────────

    def _initialize(self) -> None:
        """Perform the MCP initialize handshake."""
        result = self._send_request("initialize", {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "microagent", "version": "0.4.0"},
        })
        # Send initialized notification (required by MCP protocol)
        self._send_notification("notifications/initialized", {})
        self._initialized = True

    def list_tools(self) -> list[dict]:
        """Return the raw MCP tool schema list from the server."""
        result = self._send_request("tools/list", {})
        return result.get("tools", [])

    def call_tool(self, name: str, arguments: dict) -> str:
        """Call a tool on the MCP server and return the text result."""
        result = self._send_request("tools/call", {
            "name": name,
            "arguments": arguments,
        })
        # MCP result.content is list[{type, text}]
        contents = result.get("content", [])
        parts = [c["text"] for c in contents if c.get("type") == "text"]
        return "\n".join(parts) if parts else "(no output)"
