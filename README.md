# AI Coder Assistant with Human-in-the-Loop (HITL)

An advanced AI agent built with **LangGraph** and **LangChain** that acts as an autonomous coding assistant. The agent takes natural language prompts, generates Python code, and pauses execution to ask for human approval before running the code on the local machine.

# Architecture

- **Frontend:** Next.js, React, TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python
- **AI Framework:** LangChain + LangGraph
- **LLM:** Groq (Qwen3-27B)

# Key Features

- **Tool Calling:** Converts natural language requests into structured Python scripts.
- **Stateful Graph:** Uses LangGraph `StateGraph` to manage agent state, memory, and chat history.
- **Human-in-the-Loop (HITL):** Pauses execution and waits for human approval before running generated code.
- **Checkpointing:** Uses `MemorySaver` to maintain state while waiting for approval.
- **Code Execution:** Executes approved Python code using a local subprocess.
- **Execution Feedback:** Captures `stdout` and `stderr` and sends the results back to the LLM for analysis.

# Workflow

```text
User Prompt
     ↓
LangGraph Agent
     ↓
Generate Python Code
     ↓
Human Approval
   ↙       ↘
Reject    Approve
  ↓          ↓
Stop      Execute Code
             ↓
       stdout / stderr
             ↓
        LLM Analysis
             ↓
        Final Response