"""
Pattern: Evaluation (LLM-as-a-Judge)
Strategic Value: Automated Quality Assurance for Executive Reports.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Quality_Control"

# 2. Define the Agents
strategy_lead = Agent(
    name="Strategy_Lead_Agent", 
    model=OLLAMA_MODEL, 
    instruction="You are a Senior IT Strategist. Provide technically accurate solutions."
)

qa_judge = Agent(
    name="Executive_Auditor_Agent", 
    model=OLLAMA_MODEL, 
    instruction=(
        "You are a Quality Assurance Judge. Rate the provided strategy 1-5 on: "
        "1. Strategic Alignment, 2. Technical Feasibility, 3. Financial Logic."
    )
)

# 3. The Core Logic Function
async def execute_evaluation(user_query: str):
    session_service = InMemorySessionService()
    
    yield "🛠️ **Step 1:** Drafting technical proposal..."
    
    await session_service.create_session(user_id="cio", session_id="eval_w", app_name=APP_NAME)
    runner_w = Runner(agent=strategy_lead, session_service=session_service, app_name=APP_NAME)
    
    proposal_out = ""
    msg_w = types.Content(role='user', parts=[types.Part(text=user_query)])
    async for event in runner_w.run_async(user_id="cio", session_id="eval_w", new_message=msg_w):
        if event.is_final_response():
            proposal_out = event.content.parts[0].text

    yield "⚖️ **Step 2:** Scoring proposal against CIO rubric..."
    
    await session_service.create_session(user_id="cio", session_id="eval_e", app_name=APP_NAME)
    runner_e = Runner(agent=qa_judge, session_service=session_service, app_name=APP_NAME)
    
    eval_context = f"--- PROPOSAL ---\n{proposal_out}\nEvaluate against 1-5 rubric."
    msg_e = types.Content(role='user', parts=[types.Part(text=eval_context)])
    
    audit_report = ""
    async for event in runner_e.run_async(user_id="cio", session_id="eval_e", new_message=msg_e):
        if event.is_final_response():
            audit_report = event.content.parts[0].text

    yield f"### 📋 Strategic Proposal\n{proposal_out}\n\n---\n### ⭐ Auditor Scorecard\n{audit_report}"

# 4. REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD
async def run_pattern(user_query: str):
    """Entry point used by the Master Validator and Streamlit UI."""
    return execute_evaluation(user_query)

if __name__ == "__main__":
    async def local_test():
        gen = await run_pattern("Propose a cloud migration plan.")
        async for update in gen:
            print(update)
    asyncio.run(local_test())