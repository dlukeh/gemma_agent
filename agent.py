import json
import requests
import re
from pathlib import Path

# Tool Imports (Ensure these exist in your /tools and /core folders)
from tools.shell import run as run_shell
from tools.timezone import get_current_time_in_timezone
from core.gatekeeper import evaluate as gatekeeper_check

# ============================================================
# Configuration
# ============================================================

AGENT_ROOT = Path(__file__).parent.resolve()
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "gemma3:12b"  # Adjust based on your needs and hardware

SYSTEM_PROMPT_PATH = AGENT_ROOT / "config" / "system_prompt.txt"
MEMORY_FILE = AGENT_ROOT / "memory" / "profile.json"
SYSTEM_PROMPT = SYSTEM_PROMPT_PATH.read_text()

# ============================================================
# Helper Functions
# ============================================================


def extract_tool_call(text):
    """Finds the FIRST tool call and returns the parsed JSON."""
    pattern = r"<tool_call>(.*?)</tool_call>"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            return None
    return None


def load_memory():
    if MEMORY_FILE.exists():
        return json.loads(MEMORY_FILE.read_text())
    return {"task_history": []}


def save_memory(memory):
    MEMORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    MEMORY_FILE.write_text(json.dumps(memory, indent=2))


# ============================================================
# LLM Interaction
# ============================================================


def call_llm(messages):
    """Sends messages with strict Stop Tokens to prevent 'rambunctious' chatter."""
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0,  # Keep at 0 for tool-calling stability
            "stop": [
                "<end_of_turn>",  # The primary stop signal for Gemma 3
                "</tool_call>",  # Hard stop for your custom tool tags
                "User:",  # Safety stop if it tries to roleplay as you
                "###",  # Prevents it from leaking prompt headers
            ],
            "num_ctx": 8192,
        },
    }

    response = requests.post(OLLAMA_URL, json=payload)
    response.raise_for_status()
    # Since we use a stop token, we manually re-append it if the model cut off there
    content = response.json()["message"]["content"].strip()
    if "<tool_call>" in content and "</tool_call>" not in content:
        content += "</tool_call>"
    return content


# ============================================================
# Agent Loop
# ============================================================


def main():
    memory = load_memory()
    print(f"--- Local Agent Active [Model: {MODEL}] ---")

    while True:
        user_input = input("\nUser: ")
        if user_input.lower() in ("exit", "quit"):
            break

        # Start conversation with System Prompt + Memory + User Task
        messages = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"History: {json.dumps(memory['task_history'])}\nTask: {user_input}",
            },
        ]

        # 1. GENERATION PHASE (Model decides if it needs a tool)
        llm_output = call_llm(messages)

        # Parse output
        tool_data = extract_tool_call(llm_output)
        clean_response = re.sub(
            r"<tool_call>.*?</tool_call>", "", llm_output, flags=re.DOTALL
        ).strip()

        if clean_response:
            print(f"\nAgent: {clean_response}")

        # 2. EXECUTION PHASE (If tool detected)
        if tool_data:
            tool_name = tool_data.get("tool")
            # Handle different JSON keys for different tools
            cmd = (
                tool_data.get("command")
                or tool_data.get("query")
                or tool_data.get("url")
            )

            # Gatekeeper Check
            status, reason = gatekeeper_check(tool_name, {"command": cmd})
            if status == "deny":
                print(f"![Blocked]: {reason}")
                continue

            print(f"[*Executing {tool_name}*]: {cmd}")

            # Tool Selection
            if tool_name == "run_shell":
                result = run_shell(cmd)
            elif tool_name == "get_current_time_in_timezone":
                result = get_current_time_in_timezone(cmd)
            elif tool_name == "duckduckgo_search":
                # Ensure you've updated web_search.py to use the DDGS library
                from tools.web_search import duckduckgo_search

                result = duckduckgo_search(cmd)
            elif tool_name == "visit_webpage":
                from tools.visit_webpage import visit_webpage

                result = visit_webpage(cmd)
            else:
                result = "Error: Tool not implemented."

            # 3. FEEDBACK PHASE (Feeding the tool result back to the model for a final answer)
            messages.append({"role": "assistant", "content": llm_output})
            messages.append(
                {
                    "role": "user",
                    "content": f"TOOL RESULT: {result}\nNow provide the final summary or next step.",
                }
            )

            final_response = call_llm(messages)
            print(f"\nAgent: {final_response}")

            # Update Memory
            memory["task_history"].append(
                {"action": f"{tool_name}: {cmd}", "result": final_response}
            )
            memory["task_history"] = memory["task_history"][-5:]
            save_memory(memory)


if __name__ == "__main__":
    main()
