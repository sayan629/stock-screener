# 1. Bring in dependencies
from typing import Annotated
from langgraph.graph import START, END, StateGraph
from langgraph.graph.messages import add_messages
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama
from colorama import Fore

# 2. Create LLM
llm = ChatOllama(
     model="llama3.2",
    temperature=0
)
# 3. Create State
class State(dict):
    messages: Annotated[list, add_messages] = []
    
# 4. Build LLM Mode
# 5. Assemble Graph
# 6. Add Memory and Compile Graph
# 7. Build call loop and run it
# 8. Create tool - DONE
# 9. Build LLM with tools
# 10. Create Tool Node
# 11. Create Router Node
# 12. Update graph for Tools
print("Graph initialized with tools.")
