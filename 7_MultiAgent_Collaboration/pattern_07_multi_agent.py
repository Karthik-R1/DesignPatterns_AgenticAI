"""
Pattern: Multi-Agent Collaboration
Description: Demonstrates two specialized agents (Architect and Security) 
             collaborating on a single CIO request to ensure a balanced response.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_MultiAgent_App"

# 2. Define specialized agents
# Note: Use underscores in names to satisfy Pydantic regex requirements
architect_agent = Agent(
    name="System_Architect",
    model=OLLAMA_MODEL,
    instruction="You are a Lead Solutions Architect. Focus on scalability, performance, and integration."
)

security_agent = Agent(
    name="Security_Officer",
    model=OLLAMA_MODEL,
    instruction="You are a Chief Information Security Officer. Focus on vulnerabilities, encryption, and compliance."
)

# 3. Execution Logic (Collaboration)
async def execute_multiagent(user_query: str):
    session_service = InMemorySessionService()
    SID = "multiagent_session_07"
    
    yield "🤝 **Step 1:** Initializing collaborative session between Architect and Security..."
    
    await session_service.create_session(user_id="cio_lead", session_id=SID, app_name=APP_NAME)
    
    # Helper to run an agent
    async def get_agent_response(agent, prompt):
        runner = Runner(agent=agent, session_service=session_service, app_name=APP_NAME)
        msg = types.Content(role='user', parts=[types.Part(text=prompt)])
        final_text = ""
        async for event in runner.run_async(user_id="cio_lead", session_id=SID, new_message=msg):
            if event.is_final_response():
                final_text = event.content.parts[0].text
        return final_text

    # Phase 1: Architect Drafts
    yield "🏗️ **Step 2:** System Architect is drafting the technical blueprint..."
    architect_draft = await get_agent_response(architect_agent, f"Draft a technical architecture for: {user_query}")

    # Phase 2: Security Reviews
    yield "🛡️ **Step 3:** Security Officer is reviewing the blueprint for vulnerabilities..."
    security_review = await get_agent_response(security_agent, f"Review this architecture and find 3 risks: {architect_draft}")

    yield "✅ **Step 4:** Collaboration complete. Merging insights."
    
    final_report = (
        f"## 🏛️ Collaborative IT Report\n\n"
        f"### 📐 Architect's Blueprint\n{architect_draft}\n\n"
        f"### 🔐 Security Review\n{security_review}\n\n"
        f"---\n"
        f"**CIO Summary:** The architecture is sound but requires the 3 security mitigations listed above."
    )
    yield final_report

# --- REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD ---
async def run_pattern(user_query: str):
    """
    The master entry point used by the Master Validator and Streamlit UI.
    This function MUST be named 'run_pattern' and be async.
    """
    return execute_multiagent(user_query)

if __name__ == "__main__":
    async def local_test():
        test_query = "Build a cloud-native customer portal for 10 million users."
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n{update}")
            
    asyncio.run(local_test())