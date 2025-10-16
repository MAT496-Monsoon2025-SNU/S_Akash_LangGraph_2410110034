import random 
from typing import Literal
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END

# State
class State(TypedDict):
    graph_state: str

# Conditional edge
def analyze_text_mood(state) -> Literal["exclamation_node", "question_node", "thought_node", "shout_node", "statement_node"]:
    user_input = state['graph_state'] 
    uppercase_check = user_input[18:]
    if user_input.endswith("?"):
        return "question_node"
    elif user_input.endswith("!"):
        return "exclamation_node"
    elif user_input.endswith("..."):
        return "thought_node"
    elif uppercase_check.isupper():
        return "shout_node"
    else:
        return "statement_node"

# Nodes
def node_1(state):
    print("---Node 1---")
    return {"graph_state": "Your message was: " + state['graph_state']} #change: prefixed string to original graph state

def exclamation_node(state):
    print("--Exclamation Node---")
    return {"graph_state": state['graph_state'] + " You sound very excited!"}

def question_node(state):
    print("---Question Node---")
    return {"graph_state": state['graph_state'] + " Good question."}

def thought_node(state):
    print("---Thought Node---")
    return {"graph_state": state['graph_state'] + " Thats an interesting thought."}

def shout_node(state):
    print("---Shout Node---")
    return {"graph_state": state['graph_state'] + " You seem angry. What's wrong?"}

def statement_node(state):
    print("--- Statement Node---")
    return {"graph_state": state['graph_state'] + " This is a standard statement."}

# Build graph
builder = StateGraph(State)
builder.add_node("node_1", node_1)
builder.add_node("exclamation_node", exclamation_node)
builder.add_node("question_node", question_node)
builder.add_node("shout_node", shout_node)
builder.add_node("thought_node", thought_node)
builder.add_node("statement_node", statement_node)

# Logic
builder.add_edge(START, "node_1")
builder.add_conditional_edges("node_1", analyze_text_mood)
builder.add_edge("exclamation_node", END)
builder.add_edge("question_node", END)
builder.add_edge("shout_node", END)
builder.add_edge("thought_node", END)
builder.add_edge("statement_node", END)
# Add
graph = builder.compile()
