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

## Module 1: Video 6 (Agent)
- Made an agent using the ReAct principle which basically feeds tool outputs back into the tool calling nodes as many times as needed and uses the previous outputs as new inputs. 
- Changes: Replaced the arithmetic functions with string operation functions that reverse text, add text to the start of a text, etc. Changed the user instructions to match the same. Tested it in Langsmith as a trace. 

## Module 1: Video 7 (Agent with Memory)
- Made the agent remember the outputs of its previous tool calling loops, ie gave it memory. This was implemented using MemorySaver() which is a type of checkpoint in LangGraph. Using a particular thread id for each user-input tool call, we can use the memory functionality.
- Changes: Again added my own string operation functions and using these tools, I ran the agent with memory and changed the user instructions accordingly. Also edited the agent.py file with these new tools and ran it on studio. 

# Module 2
## Module 2: Video 1 (State Schema)
- Learnt about the different types of datatypes and typed state schemas, in specific learnt that both the TypedDict schema and the Dataclass schema do not enforce typehints at runtime so no validation error is raised even though it should be.  This was fixed using Pydantic wherein we implemented a validation error to be raised. 
- Changes: Changed the default "mood" literal to a list of movies. Added more graph nodes as well. These changes were done thrice: in TypeDict, Dataclass and Pydantic 

## Module 2: Video 2 (State Reducers)
- Learnt that the way steps in a graph work is such that, when two nodes execute in parallel, by default the prior values are overwritten in the same step, so an error occurs. So reducers are brought in to fix this by adding to a list the new value along with the initial value instead of overriding the same. This can be implemented using Annotated keys
- Changes: Similar to the first video, I used a list of movies. The foo key of type int was changed to movie key of string type. Changed the initial concatenation of integer operation to a concatenation of string operation. Changed up the questions asked while implementing add_messages and remove_messages reducers.  

## Module 2: Video 3 (Multiple Schemas)
- Learnt how to use private states to let certain nodes privately exchange information without it being in the final output. Learnt to use a custom i/o schema to filter out contents in the graph's input and output. 
- Changes: In the demonstration of private states, I replaced the default variables of int type with movie and title_change variables of string type to carry on with the idea I had in the first two modules. Also changed up the prompts inside the input/output schema. 

## Module 2: Video 4 (Trim Filter Messages)
- Learnt how to use reducers, filters and trimmers to restrict the amount of conversation history that is fed to the model - this is to both preserve actual response time and save money used in token spending
- Changed the prompts used to demonstrate filters and trimmers to inquire about dystopian novels. Saw the same in action as a Langsmith trace in the website

## Module 2: Video 5 (Chatbot w/ Summarization and Memory)
- Learnt how to summarize conversation history with a py function and implement it using Langgraph's checkpointers (persistence). The summary function is only called when there's more than a particular number of messages in conversation history (conditional edge for the same). This seems to be a more resource-efficient way to keep only useful information as compared to trims/filters/reducers.
- Changed the number of messages required for the summary function to be called to 8, and extended the conversation (with a new topic on my favourite movies) to test the same. Saw all the traces in Langgraph, which are attached in the notebook itself.

## Module 2: Video 6 (Chatbot with External Memory)
- With in-memory checkpointers, once you restart the notebook, you'll lose all previous conversation history. Using an external database (in this case sqlite) fixes this as the LLM consistently fetches conversation history from the database so there is permanent persistence. This is also the most effective way to minimize token usage
- Changes: Changed all the prompts and added a few more. Before changing the prompts, I ran the default prompts. The LLM remembers the default prompts in the output of my new prompts (reflected in the notebook) as expected. Finally used the studio files and ran chatbot.py in studio.

## Module 3: Video 1 (Streaming)
- Learnt about streaming in Langgraph wherein there's two ways of which streaming updates returns only individual state updates after calling a node and streaming values returns full state up to the point of calling that node. Also learnt about .astream_events to stream tokens from the LLM which uses 4 keys, mainly event, name, data, metadata.
- Changes: Changed convo requirement for summarize_conversation to be called from 6 to 8. Then extended .astream_events' token streaming ability to summarize_conversation. Wrote code for the same (thread id 6) with 9 human messages to test this out. Also rewrote all the prompts.

## Module 3: Video 2 (Breakpoints)
- Learnt about the usage of breakpoints as a first step in implementing human in the loop (sometimes we need a human who approves changes before production). Specifically learnt about the ability to use interrupt_before argument in builder.compile to interrupt node execution just before a node is about to run. 
- Changes: Added breakpoints before both assistant and tools by passing assistant to the interrupt_before argument. Tweaked user input to ask for both multiplication and addition, then added multiple breakpoints to the code that stop right before both the assistant node and the tool node for both tool calls. Tweaked builder.compile in agent.py (studio) to reflect this, output of which is in the notebook.

## Module 3: Video 3 (Editing State and Human Feedback)
- Previously we could only use breakpoints for interrupting node execution and approving/cancelling it. Now using graph.update_state we can also modify the graph's state by modifying the input given before the execution of that particular node. 
- Changes: Changed the tools from arithmetic operations to string operations and changed the prompts accordingly. Then, I changed the part where the LLM awaits user input to take multiple user inputs at multiple breakpoints, each modifying the previous input (did this with a while loop). 

## Module 3: Video 4 (Dynamic Breakpoints)
- Dynamic breakpoints are internal breakpoints that force the graph to break itself based on some condition already defined, using NodeInterrupt() - although NodeInterrupt now seems deprecated as we get warnings about it while using it. 
- Changes: After interruption at step 2 wherein the input cannot be more than 5 characters, I changed it so that instead of feeding a new input, the old input gets truncated to 5 characters (using basic python) and is then fed that to graph.update_state. Added a new dynamic breakpoint at the third step that stops execution if the input is STOP (or stop/Stop/etc). Updated dynamic_breakpoints.py to reflect the same.

## Module 3: Video 5 (Time Travel)
- Learnt the concepts of replaying and forking a particular checkpoint/step. Learnt how to use get_state_history() to view the full history of the graph's states. Forking can now re-invoke the graph from a previous checkpoint to use a new input for the same, without having to re-execute the graph entirely. Replays of a graph are just re-runs of a particular checkpoint, but without executing any nodes as the graph knows if that checkpoint has been executed before.
- Changes: Extended and changed the arithmetic operation tools, then changed up the prompts to call multiple tools at once. 

# Module 4
## Module 4: Video 1 (Parallelization)
- Learnt about parallel nodes which execute at the same time, used an add reducer to append the output of two nodes at the same time to actually implement this properly. There is also a default order for parallel nodes set by Langgraph, which we've changed here using a sorting function. Used Tavily to build a web search agent using parallel nodes for different types of searches. 
- Changes: Added more nodes that run in parallel. Added two sub-nodes within a parallel node to extend this functionality. Implemented a research article search function using Tavily that goes through a particular list of research websites to fetch answers and added this as a node. Updated studio file parallelization.py to reflect the same.

## Module 4: Video 2 (Sub-graphs)
- Learnt how to use sub-graphs within the same graph to handle multiple states in the same graph. This is implemented using overlapping keys to pass specific info to sub-graphs and then collate all relevant information back to the entry graph. 
- Changes: Created a new sub-graph, performance metrics, that outputs failure rate and total number of logs as metrics and linked this to the main graph along with the pre-existing other two. Added link to Langsmith trace for the same.  

## Module 4: Video 3 (Map-reduce)
- Map-reduce is a framework wherein "map" breaks tasks down into subtasks and runs them parallely, and "reduce" combines the results of the parallel subtasks. 
- Changes: Along with the pre-existing joke generation and best joke selection, I wrote code for pickup-line generation and best pickup line selection. Then ran this in parallel with the joke generator to pick the best overall joke/pickup line. Updated map-reduce.py to reflect these changes. Studio screenshot attached in the notebook.

## Module 4: Video 4 (Research Assistant)
- Using all the concepts covered in primarily this module and then previous modules (particularly parallelization, sub-graphs, map-reduce, dynamic breakpoints) a research assistant was created, wherein: first a topic is initialized, then a maximum number of analysts, then analysts are created by the LLM to match expertise in the topic. Questions are searched across varying sources using Tavily web scrapers, the web results for the same are then part of the context in the final answers. We save these QnAs to the interview state post which the LLM writes multiple passages as a summary based on the interview. 
- Changes: Changed the prompts to analyze singularity/AGI and the potential negative effects of the same. Added a search_research function along with the pre-existing search_web and search_wikipedia functions using Tavily. Ran the trace and studio files, screenshot of which linked in notebook.