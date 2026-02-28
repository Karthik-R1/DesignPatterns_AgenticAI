"""
Pattern: Reasoning Model (The Logical Strategist)
Description: Forces the agent to perform an 'Inner Monologue' to de-risk complex 
             strategic IT decisions and surface hidden constraints.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Logic_Engine"

# 2. Define the Reasoning Agent
# We use system instructions to force a Chain-of-Thought (CoT) structure.
reasoning_agent = Agent(
    name="StrategicLogician",
    model=OLLAMA_MODEL,
    instruction=(
        "You are a Senior IT Strategy Consultant specializing in logical deduction. "
        "For every strategic inquiry: "
        "1. Start with a section titled '🧠 EXECUTIVE THOUGHT PROCESS' where you "
        "deconstruct the problem, list assumptions, and evaluate technical risks. "
        "2. Follow with a section titled '🎯 STRATEGIC RECOMMENDATION'. "
        "3. Include a final section '⚠️ RESIDUAL RISKS' for things that logic cannot yet solve."
    )
)

# 3. Generator Logic for Streamlit
async def execute_reasoning(user_query: str):
    session_service = InMemorySessionService()
    SID = "logic_sess_99"
    
    yield "🧠 Engaging high-reasoning 'Inner Monologue' (Chain-of-Thought)..."
    
    await session_service.create_session(user_id="cio_lead", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=reasoning_agent, session_service=session_service, app_name=APP_NAME)
    
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    response = ""
    # The async stream allows the UI to show progress while the 'Deep Thinking' happens
    async for event in runner.run_async(user_id="cio_lead", session_id=SID, new_message=msg):
        if event.is_final_response():
            response = event.content.parts[0].text
            
    yield "✅ Strategic deduction complete. Logic trail established."
    yield f"{response}"

# 4. Universal Entry Point
async def run_pattern(user_query: str):
    """Entry point for Streamlit dashboard."""
    return execute_reasoning(user_query)

if __name__ == "__main__":
    async def local_test():
        # A classic IT strategy 'trick' question regarding legacy migration
        test_query = (
            "If we migrate 10 servers to the cloud to save 20% on power, but our "
            "egress fees increase by $500 per server, do we actually save money "
            "if our current power bill is $4000 total?"
        )
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n[Update]: {update}")
    
    asyncio.run(local_test())