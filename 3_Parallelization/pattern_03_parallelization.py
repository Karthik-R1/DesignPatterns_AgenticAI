"""
Pattern: Parallelization (Multi-Agent Consensus)
Description: Executes multiple agentic queries simultaneously to compare 
             different perspectives (e.g., Risk vs. Growth) in real-time.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Parallel_App"

# 2. Define specialized agents for parallel analysis
# Names use underscores to pass Pydantic validation
risk_agent = Agent(
    name="Risk_Assessor",
    model=OLLAMA_MODEL,
    instruction="Analyze the query strictly from a security, compliance, and risk perspective."
)

growth_agent = Agent(
    name="Growth_Strategist",
    model=OLLAMA_MODEL,
    instruction="Analyze the query strictly from a business growth, ROI, and efficiency perspective."
)

# 3. Parallel Execution Logic
async def execute_parallel(user_query: str):
    session_service = InMemorySessionService()
    SID = "parallel_session_03"
    
    yield "⚡ **Step 1:** Initializing parallel workstreams for Risk and Growth analysis..."
    
    await session_service.create_session(user_id="cio_lead", session_id=SID, app_name=APP_NAME)
    
    # Helper function to run a single agent and return its final string
    async def run_single_agent(agent, query):
        runner = Runner(agent=agent, session_service=session_service, app_name=APP_NAME)
        msg = types.Content(role='user', parts=[types.Part(text=query)])
        final_text = ""
        async for event in runner.run_async(user_id="cio_lead", session_id=SID, new_message=msg):
            if event.is_final_response():
                final_text = event.content.parts[0].text
        return final_text

    yield "🚦 **Step 2:** Launching concurrent agentic evaluations (Asynchronous Gathering)..."

    # CORE PARALLEL LOGIC
    # asyncio.gather fires both tasks at once
    risk_task = run_single_agent(risk_agent, user_query)
    growth_task = run_single_agent(growth_agent, user_query)
    
    # Wait for both to finish
    results = await asyncio.gather(risk_task, growth_task)
    risk_output, growth_output = results

    yield "✅ **Step 3:** Merging divergent perspectives into a unified Executive Consensus."
    
    # Final Structured Output for the Dashboard
    summary = (
        f"### 🛡️ Risk & Compliance Perspective\n{risk_output}\n\n"
        f"### 📈 Growth & ROI Perspective\n{growth_output}\n\n"
        f"---\n"
        f"**Strategic Consensus:** By balancing these parallel insights, we recommend "
        f"proceeding with caution under the specified risk mitigations."
    )
    yield summary

# --- REQUIRED ENTRY POINT FOR MASTER VALIDATOR ---
async def run_pattern(user_query: str):
    """
    The master entry point used by the Master Validator and Streamlit UI.
    This function MUST be named 'run_pattern' and be async.
    """
    return execute_parallel(user_query)

if __name__ == "__main__":
    async def local_test():
        test_query = "Should we move our core database to a serverless architecture?"
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n[Status]: {update}")
            
    asyncio.run(local_test())