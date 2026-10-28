"""Bash execution tool with safety restrictions."""
from __future__ import annotations

import shlex
import subprocess
import sys

from .base import Tool

# ── Safety constants ──────────────────────────────────────────────
BLOCKED_COMMANDS = [
    "rm", "rmdir", "del", "format", "mkfs",       # delete / format
    "sudo", "su", "chmod", "chown",                # privilege escalation
    "curl", "wget", "nc", "netcat",                # network (not in Phase 2.3)
    "python", "python3", "pip",                    # prevent recursive self-invocation
]

BLOCKED_OPERATORS = [">", ">>"]  # redirect write (File IO tool handles this)

MAX_OUTPUT_CHARS = 2000
TIMEOUT_SECONDS = 10

# On Windows, ALLOWED_ENV is None (inherit current env, no sandbox)
# On Linux/macOS, restrict to minimal PATH
if sys.platform == "win32":
    _SAFE_ENV = None
else:
    _SAFE_ENV = {
        "PATH": "/usr/bin:/bin",
        "HOME": "/tmp/microagent_sandbox",
    }


def _is_safe(command: str) -> tuple[bool, str]:
    """Check whether a command is safe to execute.

    Returns (is_safe, reason).
    """
    # Check redirect operators first (raw string scan)
    for op in BLOCKED_OPERATORS:
        if op in command:
            return False, f"redirect operator '{op}' is not allowed"

    # Parse with shlex; fall back to simple split on failure
    try:
        tokens = shlex.split(command)
    except ValueError:
        tokens = command.split()

    if not tokens:
        return False, "empty command"

    for token in tokens:
        # Strip common path prefixes to get the base command
        base = token.rsplit("/", maxsplit=1)[-1]
        base = base.rsplit("\\", maxsplit=1)[-1]
        base_lower = base.lower()
        for blocked in BLOCKED_COMMANDS:
            if base_lower == blocked.lower():
                return False, f"command '{blocked}' is blocked for safety"

    return True, ""


def _run_bash(command: str) -> str:
    is_safe, reason = _is_safe(command)
    if not is_safe:
        return f"Error: Command blocked for safety: {reason}"

    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            env=_SAFE_ENV,
            encoding="utf-8",
            errors="replace",
        )
        output = result.stdout + result.stderr
        if len(output) > MAX_OUTPUT_CHARS:
            output = output[:MAX_OUTPUT_CHARS] + "\n[output truncated]"
        return output or "(no output)"
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {TIMEOUT_SECONDS}s"
    except Exception as e:
        return f"Error: {type(e).__name__}: {e}"


BASH_PARAMETERS: dict = {
    "type": "object",
    "properties": {
        "command": {
            "type": "string",
            "description": "The bash command to execute",
        }
    },
    "required": ["command"],
}

bash_tool = Tool(
    name="bash",
    description=(
        "Execute a bash command and return its output. "
        "Use for: listing files, checking system info, running scripts, text processing with grep/awk/sed. "
        "Do NOT use for: file writes (use file_write), web requests (use web_search), anything requiring sudo."
    ),
    parameters=BASH_PARAMETERS,
    func=_run_bash,
)
