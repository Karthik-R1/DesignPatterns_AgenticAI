"""
Pattern: Goal Setting (Strategic Alignment)
Description: Evaluates requests against specific Corporate KPIs to ensure alignment.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Goal_Setter"

goal_agent = Agent(
    name="KPI_Alignment_Agent",
    model=OLLAMA_MODEL,
    instruction=(
        "You are a Strategic Planner. Evaluate the user's request against "
        "three KPIs: 1. Operational Efficiency, 2. Cost Savings, 3. Revenue Growth. "
        "Assign a percentage alignment to each."
    )
)

async def execute_goal_setting(user_query: str):
    session_service = InMemorySessionService()
    SID = "goal_session_11"
    await session_service.create_session(user_id="cio", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=goal_agent, session_service=session_service, app_name=APP_NAME)
    
    yield "🎯 **Step 1:** Mapping request to Corporate Strategic Pillars..."
    
    response = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    async for event in runner.run_async(user_id="cio", session_id=SID, new_message=msg):
        if event.is_final_response():
            response = event.content.parts[0].text
            
    yield f"### 🏁 Strategic Alignment Report\n\n{response}"

# --- REQUIRED ENTRY POINT ---
async def run_pattern(user_query: str):
    return execute_goal_setting(user_query)