"""
Pattern: Resource-Aware (Strategic Cost Optimization)
Description: Dynamically routes queries between local 'Eco' models and cloud 'Premium' 
             models to balance reasoning depth with operational cost.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration - Tiered Compute Strategy
# Tier 1: Local / Low Cost / High Speed
ECO_MODEL = LiteLlm(model="ollama_chat/llama3.2") 
# Tier 2: Cloud / High Reasoning / Premium Cost
PREMIUM_MODEL = LiteLlm(model="google/gemini-2.0-flash") 

APP_NAME = "CIO_Unit_Economics_Engine"

# 2. Define specialized Agents based on Tier
triage_bot = Agent(
    name="FastResponder", 
    model=ECO_MODEL, 
    instruction="You are a speed-optimized assistant. Provide brief, factual answers for routine IT queries."
)

strategic_brain = Agent(
    name="DeepReasoningEngine", 
    model=PREMIUM_MODEL, 
    instruction="You are a high-reasoning strategy consultant. Provide deep analysis, complex math, and long-range planning."
)

# 3. Generator Logic for Streamlit
async def execute_resource_aware(user_query: str):
    session_service = InMemorySessionService()
    SID = "res_optimize_sess"
    
    yield "🔍 **Analyzing Compute Intensity:** Profiling query for cost-effective routing..."
    
    # --- STRATEGIC CLASSIFICATION LOGIC ---
    # Heuristic: Complex strategic requests get the 'Brain', routine requests get the 'Edge'
    strategic_keywords = ["roadmap", "investment", "architecture", "security", "analyze", "budget", "forecast"]
    is_premium_req = any(k in user_query.lower() for k in strategic_keywords) or len(user_query) > 200
    
    selected_agent = strategic_brain if is_premium_req else triage_bot
    tier_label = "💎 PREMIUM CLOUD (Gemini 2.0)" if is_premium_req else "⚡ LOCAL EDGE (Llama 3.2)"
    
    yield f"🚀 **Routing Decision:** Assigning task to **{tier_label}**..."
    await asyncio.sleep(0.8) 
    
    await session_service.create_session(user_id="cio_admin", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=selected_agent, session_service=session_service, app_name=APP_NAME)
    
    response = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    async for event in runner.run_async(user_id="cio_admin", session_id=SID, new_message=msg):
        if event.is_final_response():
            response = event.content.parts[0].text
            
    yield f"### ⚖️ Compute Resource Allocation: {tier_label}\n\n{response}"

# 4. Universal Entry Point
async def run_pattern(user_query: str):
    """Entry point for Streamlit dashboard."""
    return execute_resource_aware(user_query)

if __name__ == "__main__":
    async def local_test():
        # Test Routine Case
        print("--- Testing Eco Route ---")
        gen1 = await run_pattern("What is the current time?")
        async for update in gen1: print(update)
        
        # Test Strategic Case
        print("\n--- Testing Premium Route ---")
        gen2 = await run_pattern("Analyze the long-term ROI of migrating our legacy ERP to a microservices architecture.")
        async for update in gen2: print(update)
    
    asyncio.run(local_test())