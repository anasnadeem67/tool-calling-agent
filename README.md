# 🤖 Tool-Calling AI Agent — Task 1

Nexe-Agent Internship | Beginner Task

## Features
- ✅ Function calling (calculate, weather, datetime)
- ✅ JSON response from tools
- ✅ Error handling

## Setup

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your keys:

```bash
cp .env.example .env
```

## Run

```bash
streamlit run app.py
```

## Project Structure

```
tool_calling_agent/
├── app.py            # Streamlit UI
├── agent.py          # Agent + OpenRouter model setup
├── tools.py          # Tool definitions
├── requirements.txt
├── .env              # API keys (not committed)
└── .env.example      # Template
```
