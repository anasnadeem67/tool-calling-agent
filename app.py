"""
TASK 1: Tool-Calling AI Agent — Streamlit UI
"""

import streamlit as st
import tools as tools_module
from agent import run_agent

st.set_page_config(page_title="Tool-Calling AI Agent", page_icon="🤖")
st.title("🤖 Tool-Calling AI Agent")
st.caption("Ask about weather, math, or date/time — the agent will call the right tools.")

if "history" not in st.session_state:
    st.session_state.history = []

user_input = st.text_input(
    "Ask something:",
    placeholder="e.g. What's the weather in Karachi and what is 5 * 9?"
)

if st.button("Run Agent"):
    if user_input.strip():
        tools_module.reset_tools()
        with st.spinner("Thinking…"):
            answer = run_agent(user_input.strip())
        used = list(tools_module.tools_used) if tools_module.tools_used else ["No tool used"]
        st.session_state.history.append({
            "question": user_input.strip(),
            "answer": answer,
            "tools": used,
        })
    else:
        st.warning("Please enter a question.")

for item in reversed(st.session_state.history):
    st.markdown("---")
    st.markdown("### 🧑 You:")
    st.write(item["question"])
    st.markdown("### 🛠 Tools Used:")
    for t in item["tools"]:
        st.success(t)
    st.markdown("### 🤖 Agent:")
    st.write(item["answer"])
