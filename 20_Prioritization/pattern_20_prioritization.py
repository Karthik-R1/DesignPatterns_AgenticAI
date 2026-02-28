"""
Pattern: Prioritization (The IT Governance Engine)
Description: Dynamically triages multiple IT requests by analyzing business impact, 
             operational risk, and executive urgency.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Triage_System"

# 2. Define the Governance Agent
triage_agent = Agent(
    name="GovernanceOrchestrator",
    model=OLLAMA_MODEL,
    instruction=(
        "You are a Senior IT Governance Manager. Given a list of IT requests or incidents: "
        "1. Categorize each into: P0 (Critical/Outage), P1 (High Impact), P2 (Medium), or P3 (Routine).\n"
        "2. Sort the list by Priority (P0 first).\n"
        "3. Provide a 'CIO Brief' for each: One sentence explaining the business risk of delaying the task.\n"
        "4. Format the output as an Executive Dashboard table."
    )
)

# 3. Generator Logic for Streamlit
async def execute_prioritization(user_query: str):
    session_service = InMemorySessionService()
    SID = "priority_triage_sess"
    
    yield "📋 **Step 1:** Ingesting IT request backlog and incident logs..."
    
    await session_service.create_session(user_id="cio_staff", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=triage_agent, session_service=session_service, app_name=APP_NAME)
    
    yield "⚖️ **Step 2:** Running Risk-Impact Analysis (WSJF Framework)..."
    
    response = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    async for event in runner.run_async(user_id="cio_staff", session_id=SID, new_message=msg):
        if event.is_final_response():
            response = event.content.parts[0].text
            
    yield "✅ **Step 3:** Dynamic Triage complete. Queue optimized for business continuity."
    yield f"### 📊 CIO Incident & Request Priority Matrix\n\n{response}"

# 4. Universal Entry Point
async def run_pattern(user_query: str):
    """Entry point for Streamlit dashboard."""
    return execute_prioritization(user_query)

if __name__ == "__main__":
    async def local_test():
        # A mix of routine requests, high-level strategy, and critical infrastructure issues
        test_backlog = """
        1. Update the 'Privacy Policy' footer text on the website.
        2. ERP System down in the EMEA region - 2000 users unable to process orders.
        3. Draft a whitepaper on the 2027 Hybrid Work strategy.
        4. Cybersecurity alert: Potential unauthorized access attempt on the Payroll DB.
        5. Senior VP of Sales needs a laptop battery replacement.
        """
        gen = await run_pattern(test_backlog)
        async for update in gen:
            print(f"\n{update}")
    
    asyncio.run(local_test())