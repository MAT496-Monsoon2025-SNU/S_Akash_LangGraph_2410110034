from langchain_openai import ChatOpenAI
from langgraph.graph import MessagesState
from langgraph.graph import StateGraph, START, END
from langgraph.prebuilt import ToolNode, tools_condition
import random
from typing import Literal

# Tool
def get_daily_quote(category: Literal["inspiration", "funny", "fact"]) -> str:
    """Provides a random quote from a selected category.

    Args:
        category: The category of quote to be retrieved
    """
    quotes = {
        "inspiration": [
            "Always go too far, because that's where you'll find the truth.",
            "Whoever gives nothing, has nothing. The greatest misfortune is not to be unloved, but not to love."
        ],
        "funny": [
            "One day I'm gonna make the onions cry.",
            "When life gives you lemons, make lime juice. Life will be all like Whaaaat?"
        ],
        "fact": [
            "Japan has one vending machine for every 40 people.",
            "William Shakespeare invented over 1,700 words."
        ]
    }
    
    if category in quotes:
        return random.choice(quotes[category])
    else:
        return "Sorry, no quotes for that category."

# LLM with bound tool
llm = ChatOpenAI(model="gpt-4o")
llm_with_tools = llm.bind_tools([get_daily_quote])

# Node
def tool_calling_llm(state: MessagesState):
    return {"messages": [llm_with_tools.invoke(state["messages"])]}

# Build graph
builder = StateGraph(MessagesState)
builder.add_node("tool_calling_llm", tool_calling_llm)
builder.add_node("tools", ToolNode([get_daily_quote]))
builder.add_edge(START, "tool_calling_llm")
builder.add_conditional_edges(
    "tool_calling_llm",
    tools_condition,
)
builder.add_edge("tools", END)

# Compile graph
graph = builder.compile()