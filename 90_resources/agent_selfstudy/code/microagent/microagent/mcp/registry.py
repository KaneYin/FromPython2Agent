"""MCPToolRegistry — manage lifecycles of multiple MCP servers."""
from __future__ import annotations

from ..tools.base import ToolRegistry
from .adapter import register_mcp_server
from .client import MCPClient, MCPServerConfig


class MCPToolRegistry:
    """Manages multiple MCPClient lifecycles and registers their tools into a ToolRegistry.

    Usage::

        tool_registry = ToolRegistry()
        with MCPToolRegistry(tool_registry) as mcp:
            mcp.add_server(MCPServerConfig(name="fs", command=[...]))
            # tools are now available in tool_registry
        # all MCP server processes are cleaned up on exit
    """

    def __init__(self, tool_registry: ToolRegistry) -> None:
        self._tool_registry = tool_registry
        self._clients: dict[str, MCPClient] = {}

    def add_server(
        self,
        config: MCPServerConfig,
        prefix: str | None = None,
        auto_prefix: bool = True,
    ) -> list[str]:
        """Start an MCP server, register its tools, and return the registered tool names.

        Args:
            config: Server configuration.
            prefix: Explicit prefix for tool names. If None and auto_prefix is True,
                    the config.name is used as prefix.
            auto_prefix: When True and no explicit prefix, use config.name as prefix.
        """
        effective_prefix = (
            prefix if prefix is not None
            else (config.name if auto_prefix else None)
        )
        client = MCPClient(config)
        client.start()
        self._clients[config.name] = client
        return register_mcp_server(client, self._tool_registry, prefix=effective_prefix)

    def remove_server(self, name: str) -> None:
        """Stop and remove a specific MCP server by name."""
        if name in self._clients:
            self._clients[name].stop()
            del self._clients[name]

    def stop_all(self) -> None:
        """Stop all managed MCP servers."""
        for client in self._clients.values():
            client.stop()
        self._clients.clear()

    def __enter__(self) -> MCPToolRegistry:
        return self

    def __exit__(self, *args) -> None:
        self.stop_all()
