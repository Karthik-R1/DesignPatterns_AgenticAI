"""
Pattern: Planning (Strategic Roadmap)
Description: Deconstructs a high-level CIO goal into a phased 
             implementation plan with defined milestones.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Roadmap_App"

# 2. Define the Agent
# Ensure name uses underscores to satisfy Pydantic/Validator constraints
planner_agent = Agent(
    name="Strategic_Roadmap_Architect",
    model=OLLAMA_MODEL,
    instruction=(
        "You are a Senior IT Program Manager. Your task is to break down any CIO objective "
        "into exactly three logical phases: \n"
        "1. Phase I: Discovery & Requirements\n"
        "2. Phase II: Implementation & Migration\n"
        "3. Phase III: Governance & Continuous Optimization."
    )
)

# 3. Planning Execution Logic
async def execute_planning(user_query: str):
    session_service = InMemorySessionService()
    SID = "planning_session_06"
    
    yield "🗺️ **Step 1:** Initializing Roadmap Architect and deconstructing goal..."
    
    # Establish session state
    await session_service.create_session(user_id="cio_admin", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=planner_agent, session_service=session_service, app_name=APP_NAME)
    
    yield "🧠 **Step 2:** Generating phased milestones and resource dependencies..."
    
    response_text = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    # Run the agentic workflow
    async for event in runner.run_async(user_id="cio_admin", session_id=SID, new_message=msg):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
    yield "✅ **Step 3:** Roadmap synthesis complete. Formatting for Executive review."
    
    # Final Structured Output
    yield f"### 🚀 Multi-Phase IT Strategic Roadmap\n\n{response_text}"

# --- REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD ---
async def run_pattern(user_query: str):
    """
    The master entry point used by the Master Validator and Streamlit UI.
    This function MUST be named 'run_pattern' and be async.
    """
    return execute_planning(user_query)

# Local test block
if __name__ == "__main__":
    async def local_test():
        test_query = "Migrate our core banking application to a multi-cloud environment."
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n[Status]: {update}")
            
    asyncio.run(local_test())