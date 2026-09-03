# 🤖 AI Coder Assistant with Human-in-the-Loop (HITL)

An advanced AI agent built with **LangGraph** and **LangChain** that acts as an autonomous coder. The agent takes natural language prompts, writes Python code, and pauses execution to ask for human approval before running the code on the local machine.

# 🧠 Why Human-in-the-Loop (HITL)?

Allowing an AI to automatically write and execute code locally can be dangerous. This project uses **Human-in-the-Loop (HITL)** to keep the human in control.

The AI generates the code and pauses before execution. The user reviews the code in the UI and chooses:

* **Approve** → Execute the generated Python code.
* **Reject** → Send the rejection back to the AI and generate a new solution.

# 🏗️ Architecture

* **Frontend:** Next.js, React, TypeScript, Tailwind CSS
* **Backend:** FastAPI, Python
* **AI Framework:** LangChain + LangGraph
* **LLM:** Groq (`qwen3.8-27b`)
* **Checkpointing:** LangGraph `MemorySaver`
* **Code Execution:** Python Subprocess

# 🔄 Workflow

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
AI Retry   Execute Code
             ↓
       stdout / stderr
             ↓
        LLM Analysis
             ↓
       Final Response
```

# ✨ Key Features

* **Stateful Graph:** Uses LangGraph `StateGraph` to manage chat history and agent state.
* **Tool Calling:** Converts natural language requests into structured Python scripts.
* **Human-in-the-Loop:** Pauses execution until the user approves or rejects the generated code.
* **Checkpointing:** Uses `MemorySaver` to preserve graph state while waiting for approval.
* **Code Execution:** Executes approved Python code using a local subprocess.
* **Execution Feedback:** Captures `stdout` and `stderr` and sends the results back to the LLM.
* **AI Retry:** Generates an improved solution when the user rejects the code.

# 🚀 How to Run Locally

# Backend Setup

## 1. Create Virtual Environment

```bash
python -m venv venv
```

## 2. Activate Virtual Environment

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

## 3. Install Dependencies

```bash
pip install fastapi uvicorn langchain langgraph langchain-groq python-dotenv pydantic
```

## 4. Add Groq API Key

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

## 5. Start Backend

```bash
uvicorn main:app --reload
```

Backend runs at:

```text
http://localhost:8000
```

# Frontend Setup

## 1. Navigate to Frontend

```bash
cd frontend
```

## 2. Install Dependencies

```bash
npm install
```

## 3. Start Development Server

```bash
npm run dev
```

Frontend runs at:

```text
http://localhost:3000
```

# 💬 Example

```text
User:
Create a Python script to calculate the factorial of a number.

        ↓

AI generates Python code

        ↓

Human reviews the code

        ↓

Approve / Reject

        ↓

If Approved → Execute Code

        ↓

Capture stdout / stderr

        ↓

LLM analyzes the result

        ↓

Final Response
```

# 🔐 Security

Since the application executes AI-generated code locally, production environments should use additional security measures:

* Docker/container sandboxing
* Execution timeouts
* CPU and memory limits
* Restricted filesystem access
* Restricted network access
* Code validation

# 🎯 Project Purpose

This project demonstrates how to build a **stateful AI coding agent** using:

* LangGraph
* LangChain
* Groq LLM
* Human-in-the-Loop workflows
* State checkpointing
* Python code execution
* AI-powered error analysis

# 🔮 Future Improvements

* Docker-based code sandboxing
* Authentication
* Persistent checkpoints
* Streaming responses
* Automated code testing
* Execution history
* Cloud deployment
* Advanced security controls

# 👩‍💻 Author

**Summaya Zahid**

AI/ML Engineer | Software Engineer
