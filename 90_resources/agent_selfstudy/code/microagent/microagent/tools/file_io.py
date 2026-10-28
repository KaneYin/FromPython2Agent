"""File read/write tools with sandbox directory restriction."""
from __future__ import annotations

from pathlib import Path

from .base import Tool

SANDBOX_DIR = Path.home() / ".microagent" / "sandbox"
MAX_FILE_SIZE = 50 * 1024    # 50 KB — refuse reads beyond this
MAX_WRITE_SIZE = 10 * 1024   # 10 KB — refuse writes beyond this


def _safe_path(path: str) -> tuple[Path | None, str | None]:
    """Resolve *path* relative to SANDBOX_DIR and check for traversal.

    Returns (resolved_path, error_msg).  On success error_msg is None.
    """
    target = (SANDBOX_DIR / path).resolve()
    sandbox_prefix = str(SANDBOX_DIR.resolve())
    if not str(target).startswith(sandbox_prefix):
        return None, "Error: Path traversal not allowed"
    return target, None


# ── file_read ─────────────────────────────────────────────────────

def _file_read(path: str, encoding: str = "utf-8") -> str:
    target, err = _safe_path(path)
    if err:
        return err

    if not target.exists():
        return f"Error: File not found: {path}"
    if target.is_dir():
        return f"Error: Path is a directory, not a file: {path}"

    file_size = target.stat().st_size
    if file_size > MAX_FILE_SIZE:
        return f"Error: File too large ({file_size} bytes, max {MAX_FILE_SIZE} bytes)"

    try:
        return target.read_text(encoding=encoding)
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


FILE_READ_PARAMETERS: dict = {
    "type": "object",
    "properties": {
        "path": {
            "type": "string",
            "description": "File path relative to sandbox directory",
        },
        "encoding": {
            "type": "string",
            "description": "File encoding, default utf-8",
        },
    },
    "required": ["path"],
}

file_read_tool = Tool(
    name="file_read",
    description=(
        "Read the content of a file inside the sandbox directory. "
        "The path is relative to the sandbox root (~/.microagent/sandbox). "
        "Use this tool when you need to read a file's content."
    ),
    parameters=FILE_READ_PARAMETERS,
    func=_file_read,
)


# ── file_write ────────────────────────────────────────────────────

def _file_write(path: str, content: str, mode: str = "overwrite") -> str:
    # Ensure sandbox directory exists
    SANDBOX_DIR.mkdir(parents=True, exist_ok=True)

    target, err = _safe_path(path)
    if err:
        return err

    if len(content.encode("utf-8")) > MAX_WRITE_SIZE:
        return f"Error: Content too large ({len(content)} chars, max {MAX_WRITE_SIZE} bytes)"

    write_mode = "a" if mode == "append" else "w"
    try:
        # Create parent dirs inside sandbox if needed
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")
        written = len(content.encode("utf-8"))
        return f"Written {written} bytes to {path}"
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


FILE_WRITE_PARAMETERS: dict = {
    "type": "object",
    "properties": {
        "path": {
            "type": "string",
            "description": "File path relative to sandbox directory",
        },
        "content": {
            "type": "string",
            "description": "Content to write",
        },
        "mode": {
            "type": "string",
            "description": "'overwrite' or 'append', default 'overwrite'",
        },
    },
    "required": ["path", "content"],
}

file_write_tool = Tool(
    name="file_write",
    description=(
        "Write content to a file inside the sandbox directory. "
        "The path is relative to the sandbox root (~/.microagent/sandbox). "
        "Supports 'overwrite' (default) and 'append' modes. "
        "Use this tool when you need to create or update a file."
    ),
    parameters=FILE_WRITE_PARAMETERS,
    func=_file_write,
)
