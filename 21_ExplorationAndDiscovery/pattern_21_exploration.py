"""
Pattern: Exploration (Strategic Gap Analysis)
Description: Performs recursive discovery to identify institutional 'knowns' 
             and critical research 'unknowns' for new IT initiatives.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

import nest_asyncio
nest_asyncio.apply()

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Exploration_Suite"

# 2. Define the Agent
# Focuses on recursive discovery rather than just answering.
explorer_agent = Agent(
    name="DiscoveryLead",
    model=OLLAMA_MODEL,
    instruction=(
        "You are a Strategic Discovery Agent for the CIO Office. Your goal is to map "
        "the landscape of a new technology or initiative. Analyze the user's prompt: "
        "1. **Established Facts:** List 3 industry 'knowns' or standard practices regarding this. "
        "2. **Critical Blind Spots:** Identify 3 major unknowns (risks, dependencies, or costs) "
        "that require deeper research before executive approval. "
        "3. **Next Steps:** Suggest a high-level roadmap for the discovery phase."
        "Format the output as a clean Executive Discovery Roadmap."
    )
)

async def execute_exploration(user_query: str):
    """Asynchronous generator for Streamlit status updates and roadmap generation."""
    session_service = InMemorySessionService()
    SID = "discovery_sess_001"
    
    # --- Step 1: Initialization ---
    yield "🔍 Scanning internal and industry trends for context..."
    await session_service.create_session(user_id="cio_staff", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=explorer_agent, session_service=session_service, app_name=APP_NAME)
    
    # --- Step 2: Recursive Discovery ---
    yield "🧠 Categorizing institutional knowns vs. strategic blind spots..."
    
    response_text = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    async for event in runner.run_async(user_id="cio_staff", session_id=SID, new_message=msg):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
    # --- Step 3: Final Yield ---
    yield f"### 🧭 CIO Exploration & Discovery Roadmap\n{response_text}"

async def run_pattern(user_query: str):
    """Entry point for the Streamlit dashboard."""
    return execute_exploration(user_query)

if __name__ == "__main__":
    async def main():
        # Example: Exploring a complex, emerging technology mandate
        test_query = "Assess the feasibility of implementing Quantum-resistant cryptography across our legacy financial apps."
        gen = await run_pattern(test_query)
        async for update in gen:
            print(update)
    
    asyncio.run(main())