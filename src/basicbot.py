from typing import Annotated, TypedDict

from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages


# -----------------------------
# 1. Create Ollama LLM
# -----------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# -----------------------------
# 2. Create State
# -----------------------------

class State(TypedDict):
    messages: Annotated[list, add_messages]


# -----------------------------
# 3. Create chatbot node
# -----------------------------

def chatbot(state: State):

    response = llm.invoke(state["messages"])

    return {
        "messages": [response]
    }


# -----------------------------
# 4. Build Graph
# -----------------------------

graph_builder = StateGraph(State)

graph_builder.add_node("chatbot", chatbot)

graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


# -----------------------------
# 5. Compile
# -----------------------------

graph = graph_builder.compile()


# -----------------------------
# 6. Run chatbot
# -----------------------------

if __name__ == "__main__":

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() in ["exit", "quit"]:
            break

        result = graph.invoke(
            {
                "messages": [
                    ("user", user_input)
                ]
            }
        )

        print("\nAI:", result["messages"][-1].content)