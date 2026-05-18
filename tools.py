"""
tools.py — Tool definitions for the Tool-Calling AI Agent
"""

import json
import requests
from datetime import datetime
from agents import function_tool

# ─────────────────────────────────────────────
# TOOL TRACKER — list so multiple tools show up
# ─────────────────────────────────────────────

tools_used: list[str] = []


def reset_tools():
    global tools_used
    tools_used = []


# ─────────────────────────────────────────────
# TOOLS
# ─────────────────────────────────────────────

@function_tool
def get_current_datetime() -> str:

    tools_used.append("get_current_datetime")

    now = datetime.now()

    return json.dumps({
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "day": now.strftime("%A"),
    })


@function_tool
def calculate(expression: str) -> str:

    tools_used.append(f"calculate({expression})")

    try:
        allowed = set("0123456789+-*/(). %")

        if not all(c in allowed for c in expression):
            return json.dumps({"error": "Invalid characters"})

        result = eval(expression)

        return json.dumps({
            "expression": expression,
            "result": result
        })

    except Exception as e:
        return json.dumps({"error": str(e)})


@function_tool
def get_weather(city: str) -> str:

    tools_used.append(f"get_weather({city})")

    try:
        resp = requests.get(
            f"https://wttr.in/{city}?format=j1",
            timeout=10
        )

        data = resp.json()
        current = data["current_condition"][0]

        return json.dumps({
            "city": city,
            "temp_c": current["temp_C"],
            "description": current["weatherDesc"][0]["value"]
        })

    except Exception as e:
        return json.dumps({"error": str(e)})
