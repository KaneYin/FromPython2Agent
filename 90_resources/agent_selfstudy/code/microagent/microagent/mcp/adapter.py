"""MCP tool → Tool adapter — bridge MCP server tools into the ToolRegistry."""
from __future__ import annotations

from ..tools.base import Tool, ToolRegistry
from .client import MCPClient, MCPError


def mcp_tool_to_tool(client: MCPClient, mcp_schema: dict) -> Tool:
    """Convert a single MCP tool schema (from tools/list) into a Tool object.

    The returned Tool's func closure captures the client reference so that
    invoking the tool transparently calls tools/call on the MCP server.
    """
    tool_name = mcp_schema["name"]

    def invoke(**kwargs) -> str:
        try:
            return client.call_tool(tool_name, kwargs)
        except MCPError as e:
            return f"Error: {e}"
        except Exception as e:
            return f"Error: {type(e).__name__}: {e}"

    return Tool(
        name=tool_name,
        description=mcp_schema.get("description", ""),
        parameters=mcp_schema.get("inputSchema", {"type": "object", "properties": {}}),
        func=invoke,
    )


def register_mcp_server(
    client: MCPClient,
    registry: ToolRegistry,
    prefix: str | None = None,
) -> list[str]:
    """Discover and register all tools from an MCP server.

    Args:
        client: A connected MCPClient.
        registry: The ToolRegistry to register tools into.
        prefix: If set, tool names become "{prefix}_{name}" to avoid collisions
                across multiple MCP servers.

    Returns:
        List of registered tool names.
    """
    tools = client.list_tools()
    registered: list[str] = []
    for mcp_tool in tools:
        tool = mcp_tool_to_tool(client, mcp_tool)
        if prefix:
            tool.name = f"{prefix}_{tool.name}"
        registry.register(tool)
        registered.append(tool.name)
    return registered
