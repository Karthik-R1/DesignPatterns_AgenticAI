"""
Pattern: RAG (Retrieval-Augmented Generation)
Description: Demonstrates how an agent retrieves specific facts from a 
             knowledge base to augment its response for high accuracy.
"""
import asyncio
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.models.lite_llm import LiteLlm
from google.genai import types

# 1. Configuration
OLLAMA_MODEL = LiteLlm(model="ollama_chat/llama3.2")
APP_NAME = "CIO_RAG_Knowledge_Base"

# 2. THE RETRIEVAL TOOL (Simulating a Vector Database)
def search_knowledge_base(query: str) -> str:
    """Searches the corporate IT policy manual for specific regulations."""
    # Mock knowledge base entries
    kb = {
        "password": "POLICY_402: Passwords must be 16 characters and rotated every 90 days.",
        "cloud": "POLICY_771: All cloud deployments must use the US-EAST-1 region for compliance.",
        "remote": "POLICY_102: Remote work requires a company-issued VPN at all times."
    }
    
    # Simple keyword match for the mock
    for key in kb:
        if key in query.lower():
            return f"RETRIEVED_DOCUMENT: {kb[key]}"
    
    return "RETRIEVED_DOCUMENT: No specific policy found. Reverting to general industry best practices."

# 3. Define the Agent
rag_agent = Agent(
    name="Policy_Compliance_Bot",
    model=OLLAMA_MODEL,
    tools=[search_knowledge_base],
    instruction=(
        "You are an IT Compliance Auditor. When asked a question, you MUST search the "
        "knowledge base first. Your final answer must cite the POLICY_ID retrieved."
    )
)

# 4. Execution Logic
async def execute_rag(user_query: str):
    session_service = InMemorySessionService()
    SID = "rag_session_14"
    
    yield "📚 **Step 1:** Identifying key terms for knowledge base retrieval..."
    
    await session_service.create_session(user_id="cio_admin", session_id=SID, app_name=APP_NAME)
    runner = Runner(agent=rag_agent, session_service=session_service, app_name=APP_NAME)
    
    yield "🔍 **Step 2:** Querying vector database and augmenting prompt with retrieved context..."
    
    response_text = ""
    msg = types.Content(role='user', parts=[types.Part(text=user_query)])
    
    async for event in runner.run_async(user_id="cio_admin", session_id=SID, new_message=msg):
        if event.is_final_response():
            response_text = event.content.parts[0].text
            
    yield "✅ **Step 3:** Fact-check complete. Generating grounded response."
    yield f"### 📖 Grounded Policy Analysis\n\n{response_text}"

# --- REQUIRED ENTRY POINT FOR VALIDATOR & DASHBOARD ---
async def run_pattern(user_query: str):
    """The master entry point used by the Validator and Streamlit UI."""
    return execute_rag(user_query)

if __name__ == "__main__":
    async def local_test():
        test_query = "What is our corporate policy on password length?"
        gen = await run_pattern(test_query)
        async for update in gen:
            print(f"\n{update}")
            
    asyncio.run(local_test())