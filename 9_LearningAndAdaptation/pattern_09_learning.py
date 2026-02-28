"""
Pattern: Learning (Self-Correction & Feedback Loop)
Description: Demonstrates an agent's ability to ingest human feedback and 
             adapt its internal logic/output during a multi-turn interaction.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_Learning_System"

# 2. Define the Agent
# Note: Using underscores in the name to pass Pydantic validation
adaptive_agent = Agent(
    name="Adaptive_Strategy_Agent",
    model=OLLAMA_MODEL,
    instruction=(
        "You are an AI that learns from user feedback. If the user criticizes "
        "your style or depth, acknowledge it and apply the correction to the final output."
    )
)

# 3. Learning Logic
async def execute_learning(user_query: str):
    session_service = InMemorySessionService()
    SID = "learning_session_09"
    
    await session_service.create_session(user_id="cio_lead", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=adaptive_agent, session_service=session_service, app_name=APP_NAME)

    # --- PHASE 1: INITIAL ATTEMPT ---
    yield "🎓 **Step 1:** Generating initial proposal based on general standards..."
    
    initial_res = ""
    msg_1 = types.Content(role='user', parts=[types.Part(text=f"Draft an IT strategy for: {user_query}")])
    async for event in runner.run_async(user_id="cio_lead", session_id=SID, new_message=msg_1):
        if event.is_final_response():
            initial_res = event.content.parts[0].text

    # --- PHASE 2: SIMULATED FEEDBACK LOOP ---
    # In a real app, this would be a second user input. 
    # Here, we simulate the "Learning" step where the system applies a feedback constraint.
    yield "🔄 **Step 2:** Applying 'CIO Preference' learning (e.g., 'Be more concise and focus on ROI')..."
    
    feedback_context = (
        f"Your previous response was: {initial_res}\n\n"
        "FEEDBACK: This is too technical. Rewrite it for a Board of Directors. "
        "Focus on ROI and remove the jargon."
    )
    
    yield "📈 **Step 3:** Adapting logic and refining strategy based on feedback..."
    
    final_res = ""
    msg_2 = types.Content(role='user', parts=[types.Part(text=feedback_context)])
    async for event in runner.run_async(user_id="cio_lead", session_id=SID, new_message=msg_2):
        if event.is_final_response():
            final_res = event.content.parts[0].text

    yield "✅ **Learning Loop Complete.**"
    
    report = (
        f"### 🎯 Final Adaptive Strategy (Learned)\n{final_res}\n\n"
        f"---\n"
        f"### 🎓 Learning Metadata\n"
        f"**Initial Style:** Technical/Detailed\n"
        f"**Learned Preference:** Executive/ROI-Focused"
    )
    yield report

# --- REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD ---
async def run_pattern(user_query: str):
    """The master entry point used by the Validator and Streamlit UI."""
    return execute_learning(user_query)

if __name__ == "__main__":
    async def local_test():
        test_query = "Implementation of a 5G private network in our manufacturing plants."
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n{update}")
            
    asyncio.run(local_test())