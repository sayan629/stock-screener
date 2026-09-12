from typing import Annotated, TypedDict

from langchain_core.messages import HumanMessage
from langgraph.graph.message import add_messages


class State(TypedDict):

    messages: Annotated[
        list,
        add_messages
    ]


# Initial state
state = {
    "messages": []
}


# Add first message
state["messages"] = add_messages(
    state["messages"],
    [
        HumanMessage(
            content="Hello"
        )
    ]
)

print("After first message:")
print(state["messages"])


# Add second message
state["messages"] = add_messages(
    state["messages"],
    [
        HumanMessage(
            content="Tell me about stocks."
        )
    ]
)

print("\nAfter second message:")
print(state["messages"])