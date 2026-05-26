"""
tools.py — Tool definitions for the Tool-Calling AI Agent
"""

import json
import requests
from datetime import datetime

# Track which tools were used in current run
tools_used: list[str] = []


def reset_tools():
    global tools_used
    tools_used = []


# ── Tool functions ────────────────────────────────────────────────────────

def get_current_datetime() -> str:
    """Get the current date, time, and day of week."""
    tools_used.append("get_current_datetime")
    now = datetime.now()
    return json.dumps({
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A"),
    })


def calculate(expression: str) -> str:
    """Evaluate a math expression. Supports +, -, *, /, (), %."""
    tools_used.append(f"calculate({expression})")
    try:
        allowed = set("0123456789+-*/(). %")
        if not all(c in allowed for c in expression):
            return json.dumps({"error": "Invalid characters in expression"})
        result = eval(expression)
        return json.dumps({"expression": expression, "result": result})
    except Exception as e:
        return json.dumps({"error": str(e)})


def get_weather(city: str) -> str:
    """Get current weather for a city."""
    tools_used.append(f"get_weather({city})")
    try:
        resp = requests.get(f"https://wttr.in/{city}?format=j1", timeout=10)
        data = resp.json()
        current = data["current_condition"][0]
        return json.dumps({
            "city": city,
            "temp_c": current["temp_C"],
            "description": current["weatherDesc"][0]["value"],
        })
    except Exception as e:
        return json.dumps({"error": str(e)})


# ── Groq tool schema (for function calling) ───────────────────────────────

TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "get_current_datetime",
            "description": "Get the current date, time, and day of week.",
            "parameters": {"type": "object", "properties": {}, "required": []},
        },
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Evaluate a math expression. Supports +, -, *, /, (), %.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {"type": "string", "description": "Math expression to evaluate, e.g. '5 * 9 + 3'"},
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string", "description": "City name, e.g. 'Karachi'"},
                },
                "required": ["city"],
            },
        },
    },
]

# Map tool name → function
TOOL_MAP = {
    "get_current_datetime": get_current_datetime,
    "calculate": calculate,
    "get_weather": get_weather,
}
