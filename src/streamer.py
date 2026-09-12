from langchain_ollama import ChatOllama
from langgraph.graph import START, END, StateGraph
from langgraph.graph.message import add_messages

from typing import Annotated, TypedDict


# -----------------------------
# State
# -----------------------------

class State(TypedDict):
    messages: Annotated[list, add_messages]


# -----------------------------
# Ollama
# -----------------------------

llm = ChatOllama(
    model="llama3.2",
    temperature=0
)


# -----------------------------
# Chatbot
# -----------------------------

def chatbot(state: State):

    response = llm.invoke(
        state["messages"]
    )

    return {
        "messages": [response]
    }


# -----------------------------
# Graph
# -----------------------------

builder = StateGraph(State)

builder.add_node(
    "chatbot",
    chatbot
)

builder.add_edge(
    START,
    "chatbot"
)

builder.add_edge(
    "chatbot",
    END
)

graph = builder.compile()


# -----------------------------
# Streaming
# -----------------------------

if __name__ == "__main__":

    print("Stock Screener AI")
    print("Type 'exit' to quit.")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        print("\nAI: ", end="")

        for chunk in graph.stream(
            {
                "messages": [
                    ("user", user_input)
                ]
            },
            stream_mode="updates"
        ):

            if "chatbot" in chunk:

                message = chunk["chatbot"]["messages"][-1]

                print(
                    message.content,
                    end="",
                    flush=True
                )

        print()