"""
agent.py — Agent setup using OpenRouter (loaded from .env)
"""

import os
from dotenv import load_dotenv

from agents import Agent, ModelSettings
from agents.models.openai_chatcompletions import OpenAIChatCompletionsModel
from agents.tracing import set_tracing_disabled
from openai import AsyncOpenAI

from tools import get_current_datetime, calculate, get_weather

# ─────────────────────────────────────────────
# LOAD ENV
# ─────────────────────────────────────────────

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BASE_URL = os.getenv("BASE_URL", "https://openrouter.ai/api/v1")
MODEL = os.getenv("MODEL", "openrouter/auto")

# Disable tracing — no OPENAI_API_KEY needed
set_tracing_disabled(True)

# ─────────────────────────────────────────────
# OPENROUTER CLIENT
# ─────────────────────────────────────────────

openrouter_client = AsyncOpenAI(
    api_key=OPENROUTER_API_KEY,
    base_url=BASE_URL,
)

model = OpenAIChatCompletionsModel(
    model=MODEL,
    openai_client=openrouter_client,
)

# ─────────────────────────────────────────────
# AGENT
# ─────────────────────────────────────────────

agent = Agent(
    name="ToolAgent",

    model=model,

    model_settings=ModelSettings(max_tokens=1024),

    tools=[
        get_current_datetime,
        calculate,
        get_weather
    ],

    instructions="""
You are a tool-calling AI assistant.

Rules:
- Use calculate tool for math
- Use get_weather tool for weather
- Use get_current_datetime for date/time

Always use tools when needed.
"""
)
