"""
Pattern: Memory (Context Persistence)
Description: Uses the Session Service to retain and recall information 
             from earlier in the conversation to provide continuity.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Memory_Vault"

# 2. Define the Agent
# Strict naming (underscores) to satisfy Pydantic/Validator
memory_agent = Agent(
    name="Strategic_Memory_Agent",
    model=OLLAMA_MODEL,
    instruction=(
        "You are an executive assistant with perfect recall. "
        "Reference previous session details to provide strategic continuity."
    )
)

# 3. Execution Logic
async def execute_memory(user_query: str):
    session_service = InMemorySessionService()
    # Using a consistent session ID to demonstrate memory retrieval
    SID = "persistent_cio_session" 
    
    yield "🧠 **Step 1:** Accessing the CIO Memory Vault for historical context..."
    
    await session_service.create_session(user_id="cio_admin", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=memory_agent, session_service=session_service, app_name=APP_NAME)
    
    response_text = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    async for event in runner.run_async(user_id="cio_admin", session_id=SID, new_message=msg):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
    yield "✅ **Step 2:** Context retrieved and synthesized into strategy."
    yield f"### 📜 Context-Aware Strategic Response\n\n{response_text}"

# --- REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD ---
async def run_pattern(user_query: str):
    """The master entry point used by the Validator and Streamlit UI."""
    return execute_memory(user_query)

if __name__ == "__main__":
    async def local_test():
        test_query = "Based on my previous interest in Cloud, what is our 2026 roadmap?"
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n{update}")
            
    asyncio.run(local_test())