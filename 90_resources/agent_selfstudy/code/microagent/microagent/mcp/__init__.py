"""MCP Client (stdio transport) — connect external MCP servers as tools."""
from __future__ import annotations

from .client import MCPClient, MCPServerConfig, MCPError
from .adapter import mcp_tool_to_tool, register_mcp_server
from .registry import MCPToolRegistry

__all__ = [
    "MCPClient",
    "MCPServerConfig",
    "MCPError",
    "mcp_tool_to_tool",
    "register_mcp_server",
    "MCPToolRegistry",
]
