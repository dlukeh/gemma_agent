"""
Gatekeeper Pro
--------------
Advanced safety layer that inspects both the tool name AND the arguments.
"""

# 1. Update allowed tools list
ALLOWED_TOOLS = {
    "run_shell",
    "get_current_time_in_timezone",
    "duckduckgo_search",
    "visit_webpage",
}

# 2. Define high-risk patterns
BLOCKED_SHELL_PATTERNS = {
    "rm ",
    "sudo ",
    "chmod ",
    "chown ",
    "wget ",
    "curl ",
    "/etc/",
    ".ssh",
    "poweroff",
    "reboot",
    "> /dev/",
}


def evaluate(tool_name, args):
    """
    Evaluates safety based on tool name and specific argument content.
    Returns: (status, reason)
    """
    # Check if tool is even in the building
    if tool_name not in ALLOWED_TOOLS:
        return ("deny", f"Unauthorized tool: {tool_name}")

    # Argument-level validation
    tool_args = args.get("command") or args.get("url") or args.get("query") or ""

    # Logic for Shell Safety
    if tool_name == "run_shell":
        cmd_lower = str(tool_args).lower()
        for pattern in BLOCKED_SHELL_PATTERNS:
            if pattern in cmd_lower:
                return (
                    "deny",
                    f"Security violation: Command contains forbidden pattern '{pattern}'",
                )

    # Logic for Web Safety (Preventing local network SSRF)
    if tool_name == "visit_webpage":
        url = str(tool_args).lower()
        if any(local in url for local in ["localhost", "127.0.0.1", "192.168.", "10."]):
            return (
                "deny",
                "Security violation: Attempted access to local network resource",
            )

    return ("allow", None)
