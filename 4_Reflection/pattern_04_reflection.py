"""
Pattern: Reflection (Self-Correction Loop)
Description: The agent generates an initial strategy, critiques it for 
             weaknesses or risks, and then provides a refined final output.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Reflection_App"

# 2. Define the Agent
# Names must use underscores to pass Pydantic validation
reflection_agent = Agent(
    name="Self_Critical_Strategist",
    model=OLLAMA_MODEL,
    instruction=(
        "You are a meticulous CIO Advisor. For every request, follow this multi-step logic: "
        "1. Draft an initial technical recommendation. "
        "2. Critique that recommendation by identifying at least two potential failure points. "
        "3. Provide a final 'Refined Strategy' that addresses those flaws."
    )
)

# 3. Execution Logic
async def execute_reflection(user_query: str):
    session_service = InMemorySessionService()
    SID = "reflection_session_04"
    
    yield "✍️ **Step 1:** Drafting the initial strategic recommendation..."
    
    await session_service.create_session(user_id="cio_lead", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=reflection_agent, session_service=session_service, app_name=APP_NAME)
    
    # We explicitly prompt for the reflection cycle to ensure the model executes it
    reflection_prompt = (
        f"Perform a reflection cycle on the following request: {user_query}. "
        "Show your draft, your self-critique, and your final refined recommendation."
    )
    
    yield "🧐 **Step 2:** Agent is performing self-critique to identify hidden risks..."
    
    response_text = ""
    msg = types.Content(role='user', parts=[types.Part(text=reflection_prompt)])
    
    async for event in runner.run_async(user_id="cio_lead", session_id=SID, new_message=msg):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
    yield "✅ **Step 3:** Reflection complete. Presenting the refined strategy."
    yield f"### 🪞 Strategic Reflection & Refinement\n\n{response_text}"

# --- REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD ---
async def run_pattern(user_query: str):
    """
    The master entry point used by the Master Validator and Streamlit UI.
    This function MUST be named 'run_pattern' and be async.
    """
    return execute_reflection(user_query)

if __name__ == "__main__":
    async def local_test():
        test_query = "Should we adopt a 'Serverless-First' strategy for all new apps?"
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n{update}")
            
    asyncio.run(local_test())