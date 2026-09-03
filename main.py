from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from langchain_core.messages import HumanMessage, ToolMessage # <--- ADDED ToolMessage
from pydantic import BaseModel
import uuid

from graph import app_graph

app = FastAPI(title="HITL Support Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str

class ApproveRequest(BaseModel):
    thread_id: str

@app.get("/")
def read_root():
    return {"status": "success", "message": "Server is running."}

@app.post("/start-chat")
async def start_chat(request: ChatRequest):
    message = HumanMessage(content=request.message)
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    result = app_graph.invoke({"messages": [message]}, config=config)
    last_message = result["messages"][-1]
    
    if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
        return {
            "status": "PAUSED_BEFORE_TOOL",
            "tool_calls": last_message.tool_calls,
            "thread_id": thread_id,
            "initial_response": ""
        }
    else:
        return {
            "status": "COMPLETED",
            "tool_calls": [],
            "thread_id": thread_id,
            "initial_response": last_message.content
        }

@app.post("/approve-tool")
async def approve_tool(request: ApproveRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    result = app_graph.invoke(None, config=config)
    final_message = result["messages"][-1].content
    
    return {"status": "APPROVED_AND_COMPLETED", "final_response": final_message}

# NEW ENDPOINT FOR REJECTING
@app.post("/reject-tool")
async def reject_tool(request: ApproveRequest):
    config = {"configurable": {"thread_id": request.thread_id}}
    
    # 1. Get the current state of the graph
    current_state = app_graph.get_state(config)
    last_message = current_state.values["messages"][-1]
    
    # 2. Find the ID of the tool call the AI tried to make
    tool_call_id = last_message.tool_calls[0]["id"]
    
    # 3. Create a fake ToolMessage saying the human rejected it
    rejection_msg = ToolMessage(
        content="Error: The human reviewer rejected this code and blocked execution. Do not attempt to run it again. Apologize and ask the user what they want to do next.",
        tool_call_id=tool_call_id
    )
    
    # 4. Inject this message into the graph's memory as if the tool ran and returned this error
    app_graph.update_state(config, {"messages": [rejection_msg]}, as_node="tools")
    
    # 5. Resume the graph! It will route back to the agent with the rejection message
    result = app_graph.invoke(None, config=config)
    final_message = result["messages"][-1].content
    
    return {"status": "REJECTED_AND_COMPLETED", "final_response": final_message}