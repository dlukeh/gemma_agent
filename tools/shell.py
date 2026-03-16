"""
Shell Command Tool
------------------
A controlled execution layer for the local agent.

This module provides:
- A whitelist of safe commands
- A confirmation list for potentially risky commands
- A hard blocklist for dangerous commands
- A safe wrapper around subprocess execution
- Output truncation and timeout protection

The goal is to allow useful system introspection without exposing
the user or system to destructive operations.
"""

import subprocess
import shlex

# Maximum number of characters returned to the agent
MAX_OUTPUT = 16000

# Timeout for command execution (seconds)
TIMEOUT_S = 10


# ------------------------------------------------------------
# Command Safety Categories
# ------------------------------------------------------------

# Commands that are always allowed and safe to run
SAFE_COMMANDS = {
    "ls": "safe",
    "df": "safe",
    "pwd": "safe",
    "free": "safe",
    "nvidia-smi": "safe",
    "uptime": "safe",
}

# Commands that require explicit user confirmation
CONFIRM_REQUIRED = {
    "git",
    "python",
    "pytest",
}

# Commands that are permanently blocked for safety
BLOCKED = {
    "rm",
    "dd",
    "shutdown",
    "reboot",
    "mkfs",
    "chmod",
    "chown",
    "kill",
    "service",
    "systemctl",
}


# ------------------------------------------------------------
# Public API
# ------------------------------------------------------------


def run(command):
    """
    Validate and execute a shell command with safety controls.

    Steps:
    - Parse the command safely using shlex
    - Check against blocklist, safelist, and confirmation list
    - Execute only if allowed
    - Return formatted output or error message

    Args:
        command (str): Raw command string from the LLM.

    Returns:
        str: Output or error message.
    """
    # Parse command safely
    try:
        args = shlex.split(command)
        if not args:
            return "No command provided."
        base = args[0]
    except Exception:
        return "Invalid command format."

    # Hard block — never allowed
    if base in BLOCKED:
        return f"Command '{base}' is permanently blocked."

    # Safe commands — run immediately
    if base in SAFE_COMMANDS:
        return execute(args)

    # Commands requiring confirmation
    if base in CONFIRM_REQUIRED:
        print(f"\nCommand requires approval:\n{command}")
        confirm = input("Type YES to execute: ")
        if confirm.strip() != "YES":
            return "Execution cancelled."
        return execute(args)

    # Everything else is denied by default
    return f"Command '{base}' is not allowed."


# ------------------------------------------------------------
# Internal Execution Helper
# ------------------------------------------------------------


def execute(args):
    """
    Execute a command using subprocess with timeout and output limits.

    Args:
        args (list[str]): Parsed command and arguments.

    Returns:
        str: Formatted output including exit code.
    """
    try:
        result = subprocess.run(args, capture_output=True, text=True, timeout=TIMEOUT_S)
    except subprocess.TimeoutExpired:
        return f"Command timed out after {TIMEOUT_S}s."
    except FileNotFoundError:
        return f"Command not found: {args[0]}"
    except Exception as e:
        return f"Execution error: {str(e)}"

    # Combine stdout/stderr and trim whitespace
    out = (result.stdout or result.stderr or "").strip()

    # Truncate overly long output
    if len(out) > MAX_OUTPUT:
        out = out[:MAX_OUTPUT] + "\n...[truncated]..."

    # Always include exit code
    return (
        f"(exit {result.returncode})\n{out}" if out else f"(exit {result.returncode})"
    )
