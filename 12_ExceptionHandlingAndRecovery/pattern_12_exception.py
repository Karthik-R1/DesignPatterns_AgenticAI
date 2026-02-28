"""
Pattern: Exception Handling (Resilient Operations)
Description: Demonstrates how the system handles tool or system failures 
             gracefully by catching errors and providing fallbacks.
"""
import asyncio
import random
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Resilience_App"

# 2. THE RESILIENT TOOL
def query_legacy_system(system_name: str) -> str:
    """
    Simulates a query to a flaky legacy IT system.
    Returns data on success, or raises an error on connection failure.
    """
    # Simulate a high-pressure environment where systems fail 50% of the time
    if random.choice([True, False]):
        raise ConnectionError(f"Critical failure: {system_name} is currently unreachable.")
    
    return f"SUCCESS: {system_name} reporting 99.9% uptime and stable throughput."

# 3. Define the Resilient Agent
# Using underscores in names is mandatory for Pydantic validation
resilient_agent = Agent(
    name="System_Recovery_Agent",
    model=OLLAMA_MODEL,
    tools=[query_legacy_system],
    instruction=(
        "You are a system resilience specialist. Use the 'query_legacy_system' tool to check health. "
        "If a tool call fails, DO NOT crash. Instead, explain the failure to the CIO "
        "and provide a manual fallback recommendation based on historical averages."
    )
)

# 4. Execution Logic with UI Updates
async def execute_resilience(user_query: str):
    session_service = InMemorySessionService()
    SID = "resilience_session_12"
    
    yield "🛡️ **Step 1:** Initializing failover protocols and probing legacy systems..."
    
    await session_service.create_session(user_id="cio_admin", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=resilient_agent, session_service=session_service, app_name=APP_NAME)
    
    yield "🧠 **Step 2:** Executing tool calls with internal error-trapping logic..."
    
    response_text = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    try:
        async for event in runner.run_async(user_id="cio_admin", session_id=SID, new_message=msg):
            if event.is_final_response():
                response_text = event.content.parts[0].text
    except Exception as e:
        # Final safety net for the generator itself
        response_text = f"The system encountered a fatal error during processing: {str(e)}"
            
    yield "✅ **Step 3:** System response generated (Resilience active)."
    yield f"### 🔋 System Availability Report\n\n{response_text}"

# --- REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD ---
async def run_pattern(user_query: str):
    """The master entry point used by the Validator and Streamlit UI."""
    return execute_resilience(user_query)

if __name__ == "__main__":
    async def local_test():
        test_query = "Check the health of our Mainframe ERP and provide a status update."
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n[Status]: {update}")
            
    asyncio.run(local_test())