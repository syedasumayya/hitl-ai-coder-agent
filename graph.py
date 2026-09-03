import os
from typing import TypedDict, Annotated, List
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

# Import the tools we created
from tools import tools

# Load environment variables
load_dotenv()

# 1. DEFINE THE STATE (Memory)
class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

# 2. INITIALIZE THE LLM (The Brain)
llm = ChatGroq(
    model="qwen/qwen3.8-27b",  
    temperature=0,          
    api_key=os.getenv("GROQ_API_KEY")
)
llm_with_tools = llm.bind_tools(tools)

# ... [imports and state setup above] ...

# 3. DEFINE THE NODES (The Workers)
# Node A: The Agent Node (Talks to LLM)
def call_model(state: AgentState):
    messages = state["messages"]
    
    # ADD A SYSTEM PROMPT TO FORCE TOOL USAGE
    from langchain_core.messages import SystemMessage
    system_prompt = SystemMessage(content=(
        "You are an expert AI Coder. "
        "Whenever the user asks you to write code or calculate something, "
        "you MUST use the `execute_python_code` tool to run it. "
        "DO NOT just write the code in a markdown block. "
        "Always call the tool to get the real output."
    ))
    
    # Prepend the system prompt to the messages
    full_messages = [system_prompt] + messages
    
    response = llm_with_tools.invoke(full_messages)
    return {"messages": [response]}

# Node B: The Tool Node (Runs the Python functions)
# LangGraph has a built-in ToolNode that automatically reads the LLM's tool_calls and runs them
tool_node = ToolNode(tools)

# ... [Keep the imports and Nodes 1, 2, 3 from before] ...

# 4. BUILD THE GRAPH
workflow = StateGraph(AgentState)

workflow.add_node("agent", call_model)
workflow.add_node("tools", tool_node)

workflow.set_entry_point("agent")

def should_continue(state: AgentState) -> str:
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tools"
    return END

workflow.add_conditional_edges("agent", should_continue)
workflow.add_edge("tools", "agent")

# 5. ADD MEMORY (Checkpointer)
# This allows the graph to save its state when it pauses.
from langgraph.checkpoint.memory import MemorySaver
memory = MemorySaver()

# 6. COMPILE THE GRAPH WITH AN INTERRUPT
# We add `interrupt_before=["tools"]`. 
# This tells the graph: "Before you run any tools, STOP and wait."
app_graph = workflow.compile(checkpointer=memory, interrupt_before=["tools"])