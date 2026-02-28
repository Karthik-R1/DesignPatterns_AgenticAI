"""
Pattern: Routing (The Intent Orchestrator)
Description: Classifies user intent and routes the query to 
             the most qualified specialized agent.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Router_App"

# 2. Define Specialized Expert Agents
# Note: Use underscores in names to pass Pydantic validation
security_expert = Agent(
    name="Security_Specialist",
    model=OLLAMA_MODEL,
    instruction="You are a CISO. Provide deep technical analysis on risks, firewalls, and compliance."
)

finance_expert = Agent(
    name="Finance_Specialist",
    model=OLLAMA_MODEL,
    instruction="You are an IT Financial Controller. Provide analysis on ROI, TCO, and budget impact."
)

# 3. Routing Execution Logic
async def execute_routing(user_query: str):
    session_service = InMemorySessionService()
    SID = "routing_session_01"
    
    yield "🎯 **Step 1:** Analyzing query intent for specialized routing..."
    
    # Simple keyword-based router logic
    query_text = user_query.lower()
    if any(word in query_text for word in ["security", "risk", "hack", "cyber", "vulnerability"]):
        selected_agent = security_expert
        route_label = "Cyber Security Division"
    else:
        # Default to Finance for ROI/Budget related queries
        selected_agent = finance_expert
        route_label = "IT Financial Operations"

    yield f"🧠 **Step 2:** Routing request to the **{route_label}**..."

    await session_service.create_session(user_id="cio_admin", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=selected_agent, session_service=session_service, app_name=APP_NAME)
    
    response_text = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    # Run the selected specialist agent
    async for event in runner.run_async(user_id="cio_admin", session_id=SID, new_message=msg):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
    yield "✅ **Step 3:** Specialist analysis complete. Synthesizing final report."
    yield f"### 🗺️ Routed Specialist Response ({route_label})\n\n{response_text}"

# --- REQUIRED ENTRY POINT FOR MASTER VALIDATOR ---
async def run_pattern(user_query: str):
    """
    The master entry point used by the Master Validator and Streamlit UI.
    This function MUST be named 'run_pattern' and be async.
    """
    return execute_routing(user_query)

if __name__ == "__main__":
    async def local_test():
        # Test with a security query
        test_query = "What are the risks of using outdated SSL certificates?"
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n{update}")
            
    asyncio.run(local_test())