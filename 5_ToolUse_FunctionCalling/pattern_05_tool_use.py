"""
Pattern: Tool Use (The Executive Assistant)
Description: Demonstrates an agent's ability to selectively call 
             external functions to retrieve live IT infrastructure data.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Tool_App"

# 2. THE TOOLS (Must be standard functions with docstrings for the validator)
def get_cloud_spend_report(department: str) -> str:
    """Retrieves the current month's cloud expenditure for a specific department."""
    # Mock data for demonstration
    spend_data = {
        "engineering": "$45,200 (12% over budget)",
        "marketing": "$12,400 (On track)",
        "sales": "$8,900 (Under budget)"
    }
    result = spend_data.get(department.lower(), "Department not found in financial database.")
    return f"FINANCIAL_REPORT: {department.upper()} spend is {result}."

def check_system_latency(region: str) -> str:
    """Checks real-time network latency for global data center regions."""
    # Mock latency data
    latency = {"us-east": "24ms", "eu-west": "110ms", "ap-south": "320ms"}
    result = latency.get(region.lower(), "No data for this region.")
    return f"NETWORK_STATUS: Latency for {region} is {result}."

# 3. Define the Agent
# Strict naming (underscores) prevents Pydantic BaseToolset errors
it_assistant = Agent(
    name="IT_Operations_Assistant",
    model=OLLAMA_MODEL,
    tools=[get_cloud_spend_report, check_system_latency],
    instruction=(
        "You are an IT Operations Assistant. Use the provided tools to answer "
        "questions about cloud spending or network latency. Do not guess; "
        "if the tool doesn't provide data, say you don't know."
    )
)

# 4. Tool-Use Execution Logic
async def execute_tool_use(user_query: str):
    session_service = InMemorySessionService()
    SID = "tool_session_05"
    
    yield "🔧 **Step 1:** Parsing request to identify required system tools..."
    
    await session_service.create_session(user_id="cio_lead", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=it_assistant, session_service=session_service, app_name=APP_NAME)
    
    yield "📡 **Step 2:** Executing external function calls and retrieving live data..."
    
    response_text = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    async for event in runner.run_async(user_id="cio_lead", session_id=SID, new_message=msg):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
    yield "✅ **Step 3:** Data retrieval complete. Synthesizing IT status report."
    yield f"### 🛠️ Live IT Operations Report\n\n{response_text}"

# --- REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD ---
async def run_pattern(user_query: str):
    """
    The master entry point used by the Master Validator and Streamlit UI.
    This function MUST be named 'run_pattern' and be async.
    """
    return execute_tool_use(user_query)

if __name__ == "__main__":
    async def local_test():
        test_query = "How much did the Engineering department spend on cloud this month?"
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n{update}")
            
    asyncio.run(local_test())