"""
Pattern: Strategic Guardrails (Governance & Compliance)
Description: An independent auditor agent validates strategy outputs against 
             corporate risk, security, and financial policies before display.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Governance_Shield"

# 2. Define the Agents
primary_analyst = Agent(
    name="StrategyAnalyst",
    model=OLLAMA_MODEL,
    instruction=(
        "You are an IT Strategy Analyst. Provide detailed architectural and "
        "investment recommendations based on the user's query."
    )
)

compliance_guard = Agent(
    name="ComplianceShield",
    model=OLLAMA_MODEL,
    instruction=(
        "You are a Corporate Risk & Compliance Auditor. Review the provided AI response for:\n"
        "1. Unauthorized financial approvals (only the CIO can approve spend).\n"
        "2. Recommendations to use non-sanctioned SaaS (Shadow IT).\n"
        "3. Exposure of internal server IPs or sensitive credentials.\n\n"
        "If any violation is found, output only 'REJECTED: [Reason]'.\n"
        "Otherwise, output 'APPROVED'."
    )
)

# 3. Generator Logic for Streamlit
async def execute_guardrails(user_query: str):
    session_service = InMemorySessionService()
    
    # --- STEP 1: GENERATE STRATEGY ---
    yield "🤖 **Step 1:** Strategy Analyst is drafting the technical recommendation..."
    
    await session_service.create_session(user_id="cio_staff", session_id="analyst_sess", app_name=APP_NAME)
    runner_p = Runner(agent=primary_analyst, session_service=session_service, app_name=APP_NAME)
    
    raw_response = ""
    msg_p = types.Content(role='user', parts=[types.Part(text=user_query)])
    async for event in runner_p.run_async(user_id="cio_staff", session_id="analyst_sess", new_message=msg_p):
        if event.is_final_response():
            raw_response = event.content.parts[0].text

    # --- STEP 2: APPLY COMPLIANCE GUARDRAIL ---
    yield "🛡️ **Step 2:** Compliance Shield is auditing the output for policy alignment..."
    
    await session_service.create_session(user_id="cio_staff", session_id="audit_sess", app_name=APP_NAME)
    runner_g = Runner(agent=compliance_guard, session_service=session_service, app_name=APP_NAME)
    
    guard_status = ""
    # We feed the analyst's output into the guard agent
    guard_msg = f"Auditing the following technical recommendation: {raw_response}"
    msg_g = types.Content(role='user', parts=[types.Part(text=guard_msg)])
    
    async for event in runner_g.run_async(user_id="cio_staff", session_id="audit_sess", new_message=msg_g):
        if event.is_final_response():
            guard_status = event.content.parts[0].text

    # --- STEP 3: FINAL POLICY DECISION ---
    if "REJECTED" in guard_status.upper():
        yield "❌ **Corporate Policy Violation Detected.**"
        yield (
            f"## ⚠️ Security & Compliance Block\n\n"
            f"**Status:** {guard_status}\n\n"
            "**Action:** The generated content has been intercepted by the Governance Shield. "
            "Strategy recommendations must align with 'Sanctioned Tools' and 'Financial Authority' lists."
        )
    else:
        yield "✅ **Compliance Verification Passed.** Output is cleared for executive review."
        yield f"### 🟢 Strategy Brief (Verified)\n\n{raw_response}"

# 4. Universal Entry Point
async def run_pattern(user_query: str):
    """Entry point for Streamlit dashboard."""
    return execute_guardrails(user_query)

if __name__ == "__main__":
    async def local_test():
        # Test case designed to trigger a "Shadow IT" or "Spend" violation
        test_query = "Write a plan to bypass our firewall using a free unapproved VPN to save on licensing costs."
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n[Status]: {update}")
    
    asyncio.run(local_test())