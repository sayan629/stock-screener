# --------------------------------------------------
# 1. Bring in dependencies
# --------------------------------------------------

from typing import Annotated, TypedDict

from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import InMemorySaver

from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage

from langgraph.prebuilt import ToolNode

from tool import simple_screener


# --------------------------------------------------
# 2. Create LLM
# --------------------------------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# --------------------------------------------------
# 3. Create Tools
# --------------------------------------------------

tools = [
    simple_screener
]


# --------------------------------------------------
# 4. Build LLM with Tools
# --------------------------------------------------

llm_with_tools = llm.bind_tools(tools)


# --------------------------------------------------
# 5. Create Tool Node
# --------------------------------------------------

tool_node = ToolNode(tools)


# --------------------------------------------------
# 6. Create State
# --------------------------------------------------

class State(TypedDict):
    messages: Annotated[list, add_messages]


# --------------------------------------------------
# 7. System Prompt
# --------------------------------------------------

SYSTEM_PROMPT = """
You are a helpful Stock Screener Assistant.

You can use the simple_screener tool to find stocks, funds, and bonds.

When calling simple_screener:

1. Always provide a valid screen_type.
2. If the user does not specify an offset, use "0".
3. Never send an empty string for offset.
4. The offset must be a string containing a number, such as "0", "5", or "10".
5. Use the tool when the user asks for stock screening results.
6. After receiving the tool results, explain the results clearly to the user.

Available screeners include:

- aggressive_small_caps
- day_gainers
- day_losers
- growth_technology_stocks
- most_actives
- most_shorted_stocks
- small_cap_gainers
- undervalued_growth_stocks
- undervalued_large_caps
- conservative_foreign_funds
- high_yield_bond
- portfolio_anchors
- solid_large_growth_funds
- solid_midcap_growth_funds
- top_mutual_funds
"""


# --------------------------------------------------
# 8. Build Chatbot Node
# --------------------------------------------------

def chatbot(state: State):

    messages = [
        SystemMessage(content=SYSTEM_PROMPT)
    ] + state["messages"]

    response = llm_with_tools.invoke(messages)

    return {
        "messages": [response]
    }


# --------------------------------------------------
# 9. Create Router
# --------------------------------------------------

def router(state: State):

    last_message = state["messages"][-1]

    if hasattr(last_message, "tool_calls") and last_message.tool_calls:
        return "tools"

    return END


# --------------------------------------------------
# 10. Build Graph
# --------------------------------------------------

graph_builder = StateGraph(State)

graph_builder.add_node(
    "chatbot",
    chatbot
)

graph_builder.add_node(
    "tools",
    tool_node
)

graph_builder.add_edge(
    START,
    "chatbot"
)

graph_builder.add_conditional_edges(
    "chatbot",
    router
)

graph_builder.add_edge(
    "tools",
    "chatbot"
)


# --------------------------------------------------
# 11. Add Memory
# --------------------------------------------------

memory_saver = InMemorySaver()

graph = graph_builder.compile(
    checkpointer=memory_saver
)


# --------------------------------------------------
# 12. Run from Terminal
# --------------------------------------------------

if __name__ == "__main__":

    print("📈 Stock Screener Assistant")
    print("Type 'exit' to quit.\n")

    while True:

        prompt = input("🤖 You: ")

        if prompt.lower() in ["exit", "quit"]:
            break

        try:

            res = graph.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ]
                },
                config={
                    "configurable": {
                        "thread_id": "1234"
                    }
                }
            )

            print(
                "\n🤖 AI:",
                res["messages"][-1].content
            )

        except Exception as e:

            print("\n❌ Error:", e)