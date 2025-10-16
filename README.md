# S_Akash_LangGraph_2410110034
Repo for my learnings from the LangGraph course as part of MAT496.

## Module 1: Video 1 (Motivation)
- Learnt about the control flow of Langgraph applications. Control flow can either be manual or created by the LLM itself. The more autonomy you give to the LLM, the less reliable it becomes, and Langgraph tries to bridge that gap. 
- No code executed in this video.

## Module 1: Video 2 (Simple Graph)
- Learnt about a simple graph structure that has nodes and edges which can be conditional as well. Also learnt about graph states. Learnt how to build a graph using the graph builder, StateGraph()
- Changes: Changed the video's conditional nodes: now it checks the string input to see what the user's mood is like. The nodes, instead of being selected randomly, look at the input text to see what it's trying to convey (eg. it's in all caps, the user may be angry). To this extent, I added more conditional nodes (5 in total). Also prefixed a string to the initial state of the graph

## Module 1: Video 3 (Studio)
- Learnt how to run a local development server for LangSmith using their own prebuilt studio. Can now visualize the studio on a browser once ran.
- Changes: I changed the simple.py file in the studio to match the graph I built in Video 2 and ran it on studio. Saved this run as a png in the Module 1 folder.

## Module 1: Video 4 (Chain)
- Relearnt tool calling. Then learnt how to use tools with graphs using a chain, ie a tool is initialized with a list of messages each comprising nodes in the graph 
- Changes: Made my own tool calling function that returns a specific category of quotes and tested it. Also changed up the initial messages. 

## Module 1: Video 5 (Router)
- In a chain, the LLM directly calls the tool and goes to the end node of the graph. With a router, it now has the option to choose whether to call a tool (with a specific tool calling node) and then go to the end node or directly go to t the end node. Also ran this on the studio
- Changes: Implemented the quote retrieval tool from the chain notebook. 
- Ran the same in LangSmith studio with modifications to the router.py file with the quote retrieval tool.