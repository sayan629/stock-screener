# 📈 Stock Screener Assistant

A local, chat-based stock screener agent. You ask questions in plain English (e.g. *"show me today's top gainers"*) and a [LangGraph](https://langchain-ai.github.io/langgraph/) agent — running on a local [Ollama](https://ollama.com/) model — decides when to call a Yahoo Finance screener tool and hands you back the results, right inside a Streamlit chat UI.

---

## How it works

```
 You type a question
        │
        ▼
 ┌─────────────┐        needs data?        ┌───────────────────┐
 │   chatbot   │ ─────────────────────────▶ │  simple_screener   │
 │ (llama3.2)  │ ◀───────────────────────── │  (Yahoo Finance)   │
 └─────────────┘        tool result         └───────────────────┘
        │
        ▼
 Final answer streamed back into the chat UI
```

- **`app.py`** — Streamlit chat interface. Renders the conversation, shows tool calls as collapsible cards, and keeps history per browser session.
- **`flow.py`** — The LangGraph agent: a `chatbot` node (the LLM), a `tools` node (runs `simple_screener` when the model asks for it), and a router that loops between them until the model has a final answer. Conversation memory is kept with an in-memory checkpointer, keyed by a `thread_id`.
- **`tool.py`** — A LangChain `@tool` that wraps `yfinance`'s predefined screener queries and returns a trimmed JSON list of matching assets.

---

## Requirements

- Python 3.10+
- [Ollama](https://ollama.com/) installed and running locally
- The `llama3.2` model pulled in Ollama

### Python packages

```bash
pip install streamlit pandas langgraph langchain langchain-ollama yfinance colorama
```

(If you keep a `requirements.txt`, put the same packages in there.)

---

## Setup

1. **Install and start Ollama**, then pull the model used by the agent:

   ```bash
   ollama pull llama3.2
   ollama serve
   ```

   Leave `ollama serve` running in the background (on macOS/Windows the Ollama app usually does this for you already).

2. **Install the Python dependencies** (ideally in a virtual environment):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # on Windows: .venv\Scripts\activate
   pip install streamlit pandas langgraph langchain langchain-ollama yfinance colorama
   ```

3. **Keep these files together** in one folder:

   ```
   project/
   ├── app.py
   ├── flow.py
   ├── tool.py
   └── .streamlit/
       └── config.toml
   ```

   The `.streamlit/config.toml` file pins the app to a dark theme so the colors always render correctly, regardless of your browser's light/dark setting.

---

## Running the app

**Chat UI (recommended):**

```bash
streamlit run app.py
```

This opens the app in your browser at `http://localhost:8501`.

**Terminal loop (no UI):**

```bash
python flow.py
```

Lets you chat with the same agent directly from the command line.

---

## Example prompts

- "What are today's biggest gainers?"
- "Show me undervalued large cap stocks"
- "Find aggressive small cap stocks"
- "Which stocks are most shorted right now?"
- "Any good high yield bond funds?"

## Available screeners

The agent can call `simple_screener` with any of these `screen_type` values:

| Screener | Description |
|---|---|
| `day_gainers` | Stocks up the most today |
| `day_losers` | Stocks down the most today |
| `most_actives` | Highest trading volume |
| `most_shorted_stocks` | Highest short interest |
| `growth_technology_stocks` | Fast-growing tech names |
| `aggressive_small_caps` | Higher-risk small caps |
| `small_cap_gainers` | Small caps up the most |
| `undervalued_growth_stocks` | Growth stocks trading cheap |
| `undervalued_large_caps` | Large caps trading cheap |
| `conservative_foreign_funds` | Lower-risk international funds |
| `high_yield_bond` | High-yield bond funds |
| `portfolio_anchors` | Stable, core-holding stocks |
| `solid_large_growth_funds` | Large-cap growth funds |
| `solid_midcap_growth_funds` | Mid-cap growth funds |
| `top_mutual_funds` | Top-rated mutual funds |

---

## Project structure

```
.
├── app.py               # Streamlit chat UI
├── flow.py               # LangGraph agent (chatbot + tool node + router)
├── tool.py                # simple_screener tool (Yahoo Finance)
└── .streamlit/
    └── config.toml       # Forces a consistent dark theme
```

---

## Troubleshooting

**"Something went wrong talking to the agent"**
Make sure `ollama serve` is running and `llama3.2` has been pulled (`ollama list` to check).

**Empty or missing results**
Yahoo Finance's predefined screeners occasionally return fewer than 5 rows, or none, depending on market hours and data availability. Try a different screener or increase the `offset`.

**Colors look wrong / inconsistent light and dark mode**
Make sure the `.streamlit/config.toml` file is present in the same folder you run `streamlit run app.py` from — Streamlit only picks up theme settings from a `.streamlit` folder relative to the working directory.

**Slow responses**
Local LLM inference speed depends on your machine's CPU/GPU. Smaller Ollama models will respond faster if `llama3.2` feels slow.

---

## Notes

- All data comes from Yahoo Finance's predefined screener queries via `yfinance` — it is for informational purposes only and is **not investment advice**.
- Conversation memory is in-memory only (`InMemorySaver`), so it resets when the app restarts.

---

**Made by [Sayan](https://www.linkedin.com/in/sayanpal04?utm_source=share_via&utm_content=profile&utm_medium=member_android)**