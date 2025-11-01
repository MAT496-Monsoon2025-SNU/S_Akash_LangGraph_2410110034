import operator
from typing import Annotated
from typing_extensions import TypedDict

from pydantic import BaseModel

from langchain_openai import ChatOpenAI 

from langgraph.types import Send
from langgraph.graph import END, StateGraph, START

# Prompts we will use
subjects_prompt = """Generate a list of 3 sub-topics that are all related to this overall topic: {topic}."""
joke_prompt = """Generate a joke about {subject}"""
best_joke_prompt = """Below are a bunch of jokes about {topic}. Select the best one! Return the ID of the best one, starting 0 as the ID for the first joke. Jokes: \n\n  {jokes}"""

pickup_line_subjects_prompt = "Generate a list of 3 sub-topics for pickup lines related to the overall topic: {topic}."
pickup_line_prompt = "Generate a pickup line about {subject}."
best_pickup_line_prompt = """Select the best pickup line about {topic} from the following list.
Return only the ID of the best one, where the first pickup line is ID 0. Pickup Lines: \n\n
{pickup_lines}"""
best_overall_prompt = """Below are a joke and a pickup line. Select best one overall.
Return your choice as either joke or pickup_line.

Joke: {joke}
Pickup Line: {pickup_line}
"""

model = ChatOpenAI(model="gpt-4o-mini", temperature=0) 

# Define the state
class Subjects(BaseModel):
    subjects: list[str]

class BestJoke(BaseModel):
    id: int

class BestPickupLine(BaseModel):
    id: int

class FinalChoice(BaseModel):
    choice: str

class OverallState(TypedDict):
    topic: str
    subjects: list
    jokes: Annotated[list, operator.add]
    best_selected_joke: str
    pickup_line_topic: str
    pickup_line_subjects: list
    pickup_lines: Annotated[list, operator.add]
    best_selected_pickup_line: str
    final_selection: str    

def generate_joke_topics(state: OverallState):
    prompt = subjects_prompt.format(topic=state["topic"])
    response = model.with_structured_output(Subjects).invoke(prompt)
    return {"subjects": response.subjects}

class JokeState(TypedDict):
    subject: str

class Joke(BaseModel):
    joke: str

def generate_joke(state: JokeState):
    prompt = joke_prompt.format(subject=state["subject"])
    response = model.with_structured_output(Joke).invoke(prompt)
    return {"jokes": [response.joke]}

def continue_to_jokes(state: OverallState):
    return [Send("generate_joke", {"subject": s}) for s in state["subjects"]]

def best_joke(state: OverallState):
    jokes = "\n\n".join(state["jokes"])
    prompt = best_joke_prompt.format(topic=state["topic"], jokes=jokes)
    response = model.with_structured_output(BestJoke).invoke(prompt)
    return {"best_selected_joke": state["jokes"][response.id]}

def generate_pickup_line_topics(state: OverallState):
    prompt = pickup_line_subjects_prompt.format(topic=state["pickup_line_topic"])
    response = model.with_structured_output(Subjects).invoke(prompt)
    return {"pickup_line_subjects": response.subjects}

def continue_to_pickup_lines(state: OverallState):
    return [Send("generate_pickup_line", {"subject": s}) for s in state["pickup_line_subjects"]]

class PickupLineState(TypedDict):
    subject: str

def generate_pickup_line(state: PickupLineState):
    prompt = pickup_line_prompt.format(subject=state["subject"])
    response = model.invoke(prompt)
    return {"pickup_lines": [response.content]}

def best_pickup_line(state: OverallState):
    pickup_lines_string = "\\n\\n".join(state["pickup_lines"])
    prompt = best_pickup_line_prompt.format(topic=state["pickup_line_topic"], pickup_lines=pickup_lines_string)
    response = model.with_structured_output(BestPickupLine).invoke(prompt)
    return {"best_selected_pickup_line": state["pickup_lines"][response.id]}


def best_overall(state: OverallState):
    """Selects the best overall from best joke and best pickup line"""
    prompt = best_overall_prompt.format(
        joke=state["best_selected_joke"],
        pickup_line=state["best_selected_pickup_line"]
    )
    response = model.with_structured_output(FinalChoice).invoke(prompt)
    
    if response.choice == "joke":
        selection = state["best_selected_joke"]
    else:
        selection = state["best_selected_pickup_line"]
        
    return {"final_selection": selection}



from IPython.display import Image, display
from langgraph.graph import StateGraph, START, END

graph = StateGraph(OverallState)
graph.add_node("generate_joke_topics", generate_joke_topics)
graph.add_node("generate_joke", generate_joke)
graph.add_node("best_joke", best_joke)
graph.add_node("generate_pickup_line_topics", generate_pickup_line_topics)
graph.add_node("generate_pickup_line", generate_pickup_line)
graph.add_node("best_pickup_line", best_pickup_line)
graph.add_node("best_overall", best_overall)

graph.add_edge(START, "generate_joke_topics")
graph.add_edge(START, "generate_pickup_line_topics")

graph.add_conditional_edges("generate_joke_topics", continue_to_jokes, ["generate_joke"])
graph.add_edge("generate_joke", "best_joke")

graph.add_conditional_edges("generate_pickup_line_topics", continue_to_pickup_lines, ["generate_pickup_line"])
graph.add_edge("generate_pickup_line", "best_pickup_line")

graph.add_edge("best_joke", "best_overall")
graph.add_edge("best_pickup_line", "best_overall")
graph.add_edge("best_overall", END)

app = graph.compile()
