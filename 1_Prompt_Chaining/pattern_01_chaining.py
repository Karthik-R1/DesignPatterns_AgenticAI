"""
Pattern: Prompting (Chain-of-Thought Strategy)
Description: Uses structured prompting to force the agent to reason through 
             complex IT problems step-by-step before providing a conclusion.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Prompt_Chain"

# 2. Define the Agent with Reasoning Instruction
reasoning_agent = Agent(
    name="Reasoning_Strategist",
    model=OLLAMA_MODEL,
    instruction=(
        "You are a logic-driven CIO Advisor. For every request, you MUST follow this structure: "
        "1. Identify the core business problem. "
        "2. List technical constraints. "
        "3. Evaluate three possible solutions. "
        "4. Provide a final recommendation based on the highest ROI."
    )
)

# 3. Execution Logic
async def execute_prompting(user_query: str):
    session_service = InMemorySessionService()
    SID = "prompt_session_02"
    
    yield "🧠 **Step 1:** Initializing Chain-of-Thought reasoning protocols..."
    
    await session_service.create_session(user_id="cio_lead", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=reasoning_agent, session_service=session_service, app_name=APP_NAME)
    
    # We wrap the user query in a 'Prompt Template' to ensure high-quality output
    structured_prompt = (
        f"Please perform a deep-dive analysis on the following: {user_query}. "
        "Remember to think step-by-step and identify hidden risks."
    )
    
    yield "📝 **Step 2:** Deconstructing the query into logical business segments..."
    
    response_text = ""
    msg = types.Content(role='user', parts=[types.Part(text=structured_prompt)])
    
    async for event in runner.run_async(user_id="cio_lead", session_id=SID, new_message=msg):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
    yield "✅ **Step 3:** Reasoning complete. Formatting final executive report."
    yield f"### 💡 Logic-Based Strategic Analysis\n\n{response_text}"

# --- REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD ---
async def run_pattern(user_query: str):
    """
    The master entry point used by the Master Validator and Streamlit UI.
    This function MUST be named 'run_pattern' and be async.
    """
    return execute_prompting(user_query)

if __name__ == "__main__":
    async def local_test():
        test_query = "Should we adopt a Decentralized Identity (DID) system this year?"
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n{update}")
            
    asyncio.run(local_test())