"""
TASK 1: Tool-Calling AI Agent
Streamlit UI — app.py
"""

import asyncio
import streamlit as st

from agents import Runner
from agent import agent
import tools as tools_module

# ─────────────────────────────────────────────
# STREAMLIT UI
# ─────────────────────────────────────────────

st.set_page_config(
    page_title="Agentic AI Tool Calling Agent",
    page_icon="🤖"
)

st.title("🤖 Agentic AI Tool Calling Agent")

# ─────────────────────────────────────────────
# MEMORY
# ─────────────────────────────────────────────

if "history" not in st.session_state:
    st.session_state.history = []

# ─────────────────────────────────────────────
# INPUT
# ─────────────────────────────────────────────

user_input = st.text_input(
    "Ask something:",
    placeholder="e.g. What's the weather in Karachi, calculate 5×9, and tell me today's date"
)

# ─────────────────────────────────────────────
# RUN AGENT
# ─────────────────────────────────────────────

if st.button("Run Agent"):

    if user_input:

        # Reset tool tracker before every new run
        tools_module.reset_tools()

        async def run_agent():
            return await Runner.run(agent, user_input)

        try:
            result = asyncio.run(run_agent())

            # Capture all tools used during this run
            used = list(tools_module.tools_used) if tools_module.tools_used else ["No tool used"]

            st.session_state.history.append({
                "question": user_input,
                "answer": result.final_output,
                "tools": used
            })

        except Exception as e:
            st.error(f"Error: {str(e)}")

# ─────────────────────────────────────────────
# OUTPUT
# ─────────────────────────────────────────────

for item in reversed(st.session_state.history):

    st.markdown("---")

    st.markdown("### 🧑 You:")
    st.write(item["question"])

    st.markdown("### 🛠 Tools Used:")
    for t in item["tools"]:
        st.success(t)

    st.markdown("### 🤖 Agent:")
    st.write(item["answer"])
