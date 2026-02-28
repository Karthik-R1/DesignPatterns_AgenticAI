"""
Pattern: Multi-Control Plane (MCP)
Description: Demonstrates an agent acting as a central controller that 
             interfaces with multiple external control planes or environments.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_MCP_Orchestrator"

# 2. Control Plane Tools (The "Server" endpoints)
def query_production_plane(command: str) -> str:
    """Sends a management command to the Production Control Plane to verify live status."""
    return f"PROD_PLANE: Command '{command}' verified. Status: Stable. Uptime: 99.99%."

def query_staging_plane(command: str) -> str:
    """Sends a management command to the Staging/Dev Control Plane for testing."""
    return f"STAGING_PLANE: Command '{command}' executed. Status: Syncing with main branch."

# 3. Define the Agent
# Naming with underscores ensures Pydantic validation passes
mcp_agent = Agent(
    name="Infrastructure_Controller",
    model=OLLAMA_MODEL,
    tools=[query_production_plane, query_staging_plane],
    instruction=(
        "You are a Multi-Control Plane orchestrator. Your role is to determine which "
        "environment (Production or Staging) a user's request pertains to and use the "
        "appropriate tool to execute the check. Always report the status back to the CIO."
    )
)

# 4. MCP Execution Logic
async def execute_mcp(user_query: str):
    session_service = InMemorySessionService()
    SID = "mcp_session_10"
    
    yield "🌐 **Step 1:** Establishing secure handshakes with distributed Control Planes..."
    
    await session_service.create_session(user_id="cio_admin", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=mcp_agent, session_service=session_service, app_name=APP_NAME)
    
    yield "📡 **Step 2:** Routing environment-specific commands via MCP protocols..."
    
    response_text = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    async for event in runner.run_async(user_id="cio_admin", session_id=SID, new_message=msg):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
    yield "✅ **Step 3:** Multi-plane synchronization complete. Reporting results..."
    yield f"### 🕹️ Multi-Control Plane Execution Report\n\n{response_text}"

# --- REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD ---
async def run_pattern(user_query: str):
    """
    The master entry point used by the Master Validator and Streamlit UI.
    This function MUST be named 'run_pattern' and be async.
    """
    return execute_mcp(user_query)

if __name__ == "__main__":
    async def local_test():
        test_query = "Check the health of the Production Plane and ensure Staging is ready for deployment."
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n[Status]: {update}")
            
    asyncio.run(local_test())