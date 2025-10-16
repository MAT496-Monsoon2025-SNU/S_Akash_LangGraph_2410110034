from langchain_core.messages import SystemMessage
from langchain_openai import ChatOpenAI

from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

def reverse_string(text: str) -> str:
    """Reverses string.

    Args:
        text: The string to be reversed.
    """
    return text[::-1]

def add_string(text: str, salutation: str = "Here you go: ") -> str:
    """Adds a given string to the beginning of a string.

    Args:
        text: The main text.
        salutation: The phrase to add at the beginning.
    """
    return salutation + text

def wrap_text_with_symbols(text: str, symbol: str = "*") -> str:
    """wraps the given text in a specific symbol.

    Args:
        text: The text that's being wrapped.
        symbol: The symbol to use for wrapping, default is *
    """
    return symbol + text + symbol

def to_uppercase(text: str) -> str:
    """Converts a string to uppercase"""
    return text.upper()

tools = [reverse_string, add_string, wrap_text_with_symbols, to_uppercase]

# Define LLM with bound tools
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools(tools)

# System message
sys_msg = SystemMessage(content="You are a helpful assistant tasked with writing performing arithmetic on a set of inputs.")

# Node
def assistant(state: MessagesState):
   return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("assistant", assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    tools_condition,
)
builder.add_edge("tools", "assistant")

# Compile graph
graph = builder.compile()
