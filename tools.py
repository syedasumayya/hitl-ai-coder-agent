from langchain_core.tools import tool
import subprocess

@tool
def execute_python_code(code: str) -> str:
    """Use this tool to run Python code. 
    Pass the full Python script as a string. 
    The tool will execute it and return the output or any errors."""
    try:
        # We run the code in a subprocess to capture output and errors safely
        result = subprocess.run(
            ["python", "-c", code],
            capture_output=True,
            text=True,
            timeout=10  # 10 second timeout to prevent infinite loops
        )
        
        if result.returncode == 0:
            # If code runs successfully
            output = result.stdout.strip()
            return f"Code executed successfully. Output:\n{output}"
        else:
            # If code throws an error
            error = result.stderr.strip()
            return f"Code failed with error:\n{error}"
            
    except Exception as e:
        return f"Tool execution failed: {str(e)}"

# List of tools for the LLM
tools = [execute_python_code]