"use client";

import { useState } from "react";

export default function Home() {
  const [input, setInput] = useState("");
  const [status, setStatus] = useState("Waiting for action...");
  const [toolCalls, setToolCalls] = useState<any>(null);
  const [threadId, setThreadId] = useState("");
  const [responses, setResponses] = useState<string[]>([]);

  const sendMessage = async () => {
    if (!input) return;
    
    setStatus("Asking AI to write code...");
    setToolCalls(null);
    setResponses([]);
    
    try {
      const res = await fetch("http://localhost:8000/start-chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input })
      });
      const data = await res.json();
      
      setThreadId(data.thread_id);
      
      if (data.status === "PAUSED_BEFORE_TOOL") {
        setStatus("AI PAUSED! Review the code before running.");
        setToolCalls(data.tool_calls);
      } else {
        setStatus("Complete!");
        setResponses(prev => [...prev, data.initial_response]);
      }
      setInput("");
    } catch (err) {
      setStatus("Error connecting to backend.");
    }
  };

  const approveTool = async () => {
    setStatus("Approved! Executing code...");
    try {
      const res = await fetch("http://localhost:8000/approve-tool", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ thread_id: threadId })
      });
      const data = await res.json();
      setStatus("Complete!");
      setToolCalls(null);
      setResponses(prev => [...prev, data.final_response]);
    } catch (err) {
      setStatus("Error connecting to backend.");
    }
  };

  // NEW: Reject function
  const rejectTool = async () => {
    setStatus("Rejected! Telling AI to try again...");
    try {
      const res = await fetch("http://localhost:8000/reject-tool", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ thread_id: threadId })
      });
      const data = await res.json();
      setStatus("Complete!");
      setToolCalls(null);
      setResponses(prev => [...prev, data.final_response]);
    } catch (err) {
      setStatus("Error connecting to backend.");
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-8 md:p-24 bg-gray-50">
      <div className="bg-white p-8 rounded-xl shadow-lg w-full max-w-3xl">
        <h1 className="text-2xl font-bold mb-6 text-black">AI Coder Assistant</h1>
        
        <div className="mb-4 flex flex-col sm:flex-row gap-2">
          <input 
            type="text" 
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
            placeholder="Try: 'Write a python script to calculate the first 10 fibonacci numbers'"
            className="flex-1 border border-gray-300 p-3 rounded-lg text-black focus:outline-none focus:ring-2 focus:ring-blue-600"
          />
          <button 
            onClick={sendMessage}
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition"
          >
            Send
          </button>
        </div>

        <div className="mb-4 p-4 bg-gray-100 rounded-lg">
          <p className="text-gray-700 font-semibold">Status:</p>
          <p className="text-gray-900">{status}</p>
        </div>

        {toolCalls && toolCalls.length > 0 && (
          <div className="mb-4 p-4 border-2 border-yellow-400 bg-yellow-50 rounded-lg">
            <p className="font-bold text-yellow-800">⚠️ Human Approval Required</p>
            <p className="text-sm text-yellow-700 mt-2 mb-2">
              AI wants to run: <code className="bg-yellow-200 px-1 rounded font-mono">{toolCalls[0].name}</code>
            </p>
            <p className="text-sm text-yellow-700 font-semibold mb-1">Code to execute:</p>
            <pre className="bg-yellow-200 p-3 rounded text-black text-sm overflow-x-auto whitespace-pre-wrap font-mono">
{toolCalls[0].args.code}
            </pre>
            
            {/* BUTTONS CONTAINER */}
            <div className="flex gap-2 mt-4">
              <button 
                onClick={approveTool}
                className="flex-1 bg-green-600 text-white py-3 rounded-lg font-semibold hover:bg-green-700 transition"
              >
                Approve & Run
              </button>
              
              {/* NEW REJECT BUTTON */}
              <button 
                onClick={rejectTool}
                className="flex-1 bg-red-600 text-white py-3 rounded-lg font-semibold hover:bg-red-700 transition"
              >
                Reject Code
              </button>
            </div>
          </div>
        )}

        <div className="space-y-3 mt-6">
          {responses.map((resp, index) => (
            <div key={index} className="p-4 bg-blue-50 border border-blue-200 rounded-lg text-blue-900 whitespace-pre-wrap break-words">
              <strong>AI:</strong> {resp}
            </div>
          ))}
        </div>
      </div>
    </main>
  );
}