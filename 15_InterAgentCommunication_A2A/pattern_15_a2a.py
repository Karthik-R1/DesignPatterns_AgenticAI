import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_A2A_Mesh"

# 1. The Service Agent
compliance_agent = Agent(
    name="Compliance_Auditor", 
    model=OLLAMA_MODEL, 
    instruction="Check IT plans for GDPR/ISO compliance. Return 'PASSED' or 'FAILED' with reasons."
)

# 2. THE WRAPPER (Fixes BaseToolset Error)
async def check_compliance(plan_details: str) -> str:
    """Sends a strategic plan to the Compliance Auditor for verification."""
    session_service = InMemorySessionService()
    await session_service.create_session(user_id="sys", session_id="tmp_a2a", app_name=APP_NAME)
    runner = Runner(agent=compliance_agent, session_service=session_service, app_name=APP_NAME)
    msg = types.Content(role='user', parts=[types.Part(text=plan_details)])
    async for event in runner.run_async(user_id="sys", session_id="tmp_a2a", new_message=msg):
        if event.is_final_response():
            return event.content.parts[0].text
    return "Compliance check unavailable."

# 3. The Lead Agent using the function as a tool
lead_agent = Agent(
    name="Lead_Strategist",
    model=OLLAMA_MODEL,
    tools=[check_compliance],
    instruction="Draft an IT strategy. You MUST call check_compliance before finalizing."
)

async def execute_pattern(user_query: str):
    session_service = InMemorySessionService()
    await session_service.create_session(user_id="cio", session_id="a2a_main", app_name=APP_NAME)
    runner = Runner(agent=lead_agent, session_service=session_service, app_name=APP_NAME)
    yield "🔗 **Establishing Agent-to-Agent handshake...**"
    response = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    async for event in runner.run_async(user_id="cio", session_id="a2a_main", new_message=msg):
        if event.is_final_response():
            response = event.content.parts[0].text
    yield f"### 🛡️ Verified Strategy\n\n{response}"

async def run_pattern(user_query: str):
    return execute_pattern(user_query)