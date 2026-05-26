"""
agent.py — Groq-based tool-calling agent
"""

import os
import json
from dotenv import load_dotenv
from groq import Groq
from tools import TOOL_SCHEMAS, TOOL_MAP, tools_used

load_dotenv()

MODEL = "llama-3.3-70b-versatile"  # Best Groq model for tool calling


def run_agent(user_input: str) -> str:
    """Run the agent with tool-calling loop. Returns final answer."""
    api_key = os.getenv("GROQ_API_KEY", "")
    if not api_key or api_key == "your_groq_api_key_here":
        return "⚠️ GROQ_API_KEY missing! Add it to .env file."

    client = Groq(api_key=api_key)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a tool-calling AI assistant.\n"
                "- Use calculate for any math\n"
                "- Use get_weather for weather questions\n"
                "- Use get_current_datetime for date/time\n"
                "Always use tools when needed. Return a clear, helpful answer."
            ),
        },
        {"role": "user", "content": user_input},
    ]

    # Agentic loop — keeps going until no more tool calls
    for _ in range(10):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
            max_tokens=1024,
        )

        msg = response.choices[0].message

        # No tool calls — we have the final answer
        if not msg.tool_calls:
            return msg.content or "No response."

        # Add assistant message with tool calls
        messages.append({
            "role": "assistant",
            "content": msg.content or "",
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {"name": tc.function.name, "arguments": tc.function.arguments},
                }
                for tc in msg.tool_calls
            ],
        })

        # Execute each tool and add results
        for tc in msg.tool_calls:
            fn_name = tc.function.name
            fn_args = json.loads(tc.function.arguments) if tc.function.arguments else {}

            if fn_name in TOOL_MAP:
                result = TOOL_MAP[fn_name](**fn_args)
            else:
                result = json.dumps({"error": f"Unknown tool: {fn_name}"})

            messages.append({
                "role": "tool",
                "tool_call_id": tc.id,
                "content": result,
            })

    return "Agent loop exceeded. Please try again."
