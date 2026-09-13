import json
import uuid

import pandas as pd
import streamlit as st
from langchain_core.messages import ToolMessage, HumanMessage

from flow import graph


# --------------------------------------------------
# PAGE CONFIG
# --------------------------------------------------

st.set_page_config(
    page_title="Stock Screener Assistant",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.4rem;
        font-weight: 700;
        margin-bottom: 0;
    }

    .subtitle {
        color: #888;
        font-size: 1rem;
        margin-top: 4px;
        margin-bottom: 25px;
    }

    .badge {
        display: inline-block;
        padding: 5px 12px;
        border-radius: 20px;
        background-color: #1f2937;
        color: #9ca3af;
        font-size: 0.8rem;
        margin-bottom: 20px;
    }

    .tool-card {
        padding: 12px;
        border-radius: 10px;
        background-color: #111827;
        border: 1px solid #374151;
        margin: 8px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

if "display_messages" not in st.session_state:
    st.session_state.display_messages = []


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.markdown("## 📈 Stock Screener")

    st.caption("AI-powered stock screening")

    st.divider()

    st.markdown("### Session")

    if st.button("🗑️ Clear conversation", use_container_width=True):

        st.session_state.thread_id = str(uuid.uuid4())
        st.session_state.display_messages = []

        st.rerun()

    st.divider()

    st.markdown("### 💡 Example prompts")

    examples = [
        "What are today's biggest gainers?",
        "Show me undervalued large cap stocks",
        "Find aggressive small cap stocks",
        "Which stocks are most shorted right now?",
        "Any good high yield bond funds?",
    ]

    for example in examples:
        if st.button(example, use_container_width=True):
            st.session_state.example_prompt = example


# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.markdown(
    '<div class="main-title">📈 Stock Screener Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="subtitle">'
    "Ask in plain English — the AI decides when to run a screener."
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    '<span class="badge">🟢 llama3.2 · Ollama</span>',
    unsafe_allow_html=True,
)


# --------------------------------------------------
# EMPTY STATE
# --------------------------------------------------

if not st.session_state.display_messages:

    st.info(
        "👋 Welcome! Ask me about stock gainers, losers, "
        "small caps, undervalued stocks, mutual funds, or bonds."
    )


# --------------------------------------------------
# DISPLAY CHAT HISTORY
# --------------------------------------------------

for message in st.session_state.display_messages:

    role = message["role"]
    content = message["content"]

    if role == "user":

        with st.chat_message("user"):
            st.write(content)

    elif role == "assistant":

        with st.chat_message("assistant"):

            st.write(content)

    elif role == "tool":

        with st.chat_message("assistant", avatar="🔧"):

            try:

                data = json.loads(content)

                if isinstance(data, list) and data:

                    df = pd.DataFrame(data)

                    st.markdown(
                        '<div class="tool-card">'
                        "📊 Screener Results"
                        "</div>",
                        unsafe_allow_html=True,
                    )

                    st.dataframe(
                        df,
                        use_container_width=True,
                        hide_index=True,
                    )

                elif isinstance(data, dict) and "error" in data:

                    st.error(data["error"])

                else:

                    st.json(data)

            except Exception:

                st.code(content)


# --------------------------------------------------
# INPUT
# --------------------------------------------------

prompt = st.chat_input(
    "Ask about stocks, funds, bonds..."
)


# Handle example prompt
if "example_prompt" in st.session_state:

    prompt = st.session_state.example_prompt

    del st.session_state.example_prompt


# --------------------------------------------------
# PROCESS USER MESSAGE
# --------------------------------------------------

if prompt:

    # Display user message immediately
    st.session_state.display_messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.write(prompt)

    try:

        with st.chat_message("assistant"):

            with st.spinner("Analyzing your request..."):

                result = graph.invoke(
                    {
                        "messages": [
                            {
                                "role": "user",
                                "content": prompt,
                            }
                        ]
                    },
                    config={
                        "configurable": {
                            "thread_id": st.session_state.thread_id
                        }
                    },
                )

        # ------------------------------------------
        # Extract messages generated by this request
        # ------------------------------------------

        messages = result["messages"]

        # Process tool results
        for message in messages:

            if isinstance(message, ToolMessage):

                st.session_state.display_messages.append(
                    {
                        "role": "tool",
                        "content": message.content,
                    }
                )

        # ------------------------------------------
        # Get final assistant response
        # ------------------------------------------

        assistant_message = None

        for message in reversed(messages):

            if hasattr(message, "content"):

                if message.__class__.__name__ == "AIMessage":

                    if message.content:

                        assistant_message = message.content
                        break

        if assistant_message:

            st.session_state.display_messages.append(
                {
                    "role": "assistant",
                    "content": assistant_message,
                }
            )

    except Exception as e:

        error_message = f"Something went wrong: {str(e)}"

        st.session_state.display_messages.append(
            {
                "role": "assistant",
                "content": error_message,
            }
        )

    st.rerun()