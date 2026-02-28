import streamlit as st
import asyncio
import importlib
import pandas as pd
import os

# --- PAGE CONFIG ---
st.set_page_config(
    page_title="CIO Strategy Command Center",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- THE PATTERN REGISTRY ---
PATTERNS = {
    "01 Routing": "pattern_01_routing",
    "02 Chaining": "pattern_02_chaining",
    "03 Parallelization": "pattern_03_parallelization",
    "04 Reflection": "pattern_04_reflection",
    "05 Tool Use": "pattern_05_tool_use",
    "06 Planning": "pattern_06_planning",
    "07 Multi-Agent": "pattern_07_multi_agent",
    "08 Memory": "pattern_08_memory",
    "09 Learning": "pattern_09_learning",
    "10 MCP": "pattern_10_mcp",
    "11 Goal Setting": "pattern_11_goal_setting",
    "12 Exception": "pattern_12_exception",
    "13 HITL": "pattern_13_hitl",
    "14 RAG": "pattern_14_rag",
    "15 A2A": "pattern_15_a2a",
    "16 Resource Aware": "pattern_16_resource_aware",
    "17 Reasoning": "pattern_17_reasoning",
    "18 Guardrails": "pattern_18_guardrails",
    "19 Evaluation": "pattern_19_evaluation",
    "20 Prioritization": "pattern_20_prioritization",
    "21 Exploration": "pattern_21_exploration"
}

# --- MASTER SAMPLE LIBRARY ---
SAMPLES = {
    "01 Routing": "Triage this: 'Our cloud egress fees are spiking in AWS, and the HR payroll portal is throwing 404 errors.'",
    "02 Chaining": "Analyze the risk of our current legacy firewall, then synthesize a 3-step mitigation plan for the board.",
    "03 Parallelization": "Compare the SaaS security features of Microsoft 365, Google Workspace, and Slack side-by-side.",
    "04 Reflection": "Draft a remote work policy. Then, critique it against the latest 2026 labor laws and provide a revised version.",
    "05 Tool Use": "Pull the latest project status from the PMO database and calculate the current budget burn rate.",
    "06 Planning": "Create a multi-phase roadmap for transitioning 500 on-premise servers to a serverless architecture.",
    "07 Multi-Agent": "Have a Security Architect and a Financial Analyst debate the pros/cons of a Private Cloud investment.",
    "08 Memory": "Based on our last three strategy sessions regarding 'Zero Trust,' how does this new VPN proposal fit in?",
    "09 Learning": "I prefer my executive summaries in bullet points with 'Risk' and 'ROI' sections. Summarize the AI Act.",
    "10 MCP": "Establish a secure tunnel to the SQL Financial database and retrieve last quarter's IT capital spend.",
    "11 Goal Setting": "Draft a new Data Privacy SOP. Ensure it meets the specific KPI of reducing audit prep time by 20%.",
    "12 Exception": "Attempt to pull real-time data from the Ollama node. (Note: Use 'force fail' to see recovery protocols).",
    "13 HITL": "Draft a formal $500,000 procurement request for a new Nvidia H100 GPU cluster for our AI lab.",
    "14 RAG": "Using our internal Strategy Wiki, explain our 2026 mandate regarding the use of open-source LLMs.",
    "15 A2A": "Ask the Compliance Agent to verify the Investment Agent's ROI calculation for the Data Center upgrade.",
    "16 Resource Aware": "Compare: (A) What is our tech stack? vs (B) Predict our server capacity needs for the next 5 years based on growth.",
    "17 Reasoning": "If we save $10k/month by switching to Llama 3.2 but increase latency by 200ms, what is the cost to user productivity?",
    "18 Guardrails": "Give me a plan to bypass our data DLP (Data Loss Prevention) so I can work from my personal laptop.",
    "19 Evaluation": "Grade this proposal for a 'Global SD-WAN upgrade' on a scale of 1-5 for technical rigor and cost logic.",
    "20 Prioritization": "Sort these by business impact: 1. Minor UI bug, 2. ERP System Down (Global), 3. New logo ideas, 4. Security breach alert.",
    "21 Exploration": "We are considering 'Quantum Computing' for encryption. What do we know, and what are our biggest blind spots?"
}

# --- SESSION STATE INITIALIZATION ---
if "user_query" not in st.session_state:
    st.session_state.user_query = ""

# --- CALLBACK FUNCTION FOR INJECTION ---
def inject_sample_callback():
    # Use the value from the selectbox to find the right sample
    st.session_state.user_query = SAMPLES.get(st.session_state.selected_pattern, "No sample available.")

# --- HELPER: DYNAMIC EXECUTION ---
async def call_pattern(pattern_key, query):
    module_name = PATTERNS[pattern_key]
    module = importlib.import_module(module_name)
    generator = await module.run_pattern(query)
    return generator

# --- UI: SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shield.png", width=80)
    st.title("CIO Strategy CoE")
    st.markdown("---")
    
    # We add a key here so we can access the selection inside the callback
    selected_pattern = st.selectbox(
        "Select Agentic Pattern", 
        list(PATTERNS.keys()), 
        key="selected_pattern"
    )
    
    st.info(f"**Pattern Focus:** {selected_pattern.split(' ', 1)[1]}")
    
    with st.expander("System Telemetry"):
        st.write("🟢 Ollama (Llama 3.2)")
        st.write("🟢 Google AI (Gemini 2.0)")
        st.write("⚡ Edge Routing: Active")

# --- UI: MAIN DASHBOARD ---
st.title(f"🚀 Pattern Demo: {selected_pattern}")
st.caption("Strategic Orchestration Layer | AI-Powered Enterprise Architecture")

# THE FIX: Button uses a callback to update state before the rerun
st.button("Inject Sample CIO Prompt", on_click=inject_sample_callback)

# THE FIX: value is linked to session_state, and changes are synced via key
user_query = st.text_area(
    "Strategic Prompt / Backlog Data:", 
    height=150,
    key="user_query" # Link directly to the session_state variable
)

if st.button("Execute Agentic Workflow", type="primary"):
    if user_query:
        status_placeholder = st.empty()
        output_container = st.empty()
        
        async def run_ui():
            try:
                gen = await call_pattern(selected_pattern, user_query)
                async for update in gen:
                    update_str = str(update)
                    if "###" in update_str: 
                        output_container.markdown(update_str)
                    else:
                        status_placeholder.status(update_str, state="running")
                st.success("Workflow Finalized.")
            except Exception as e:
                st.error(f"Execution Error: {str(e)}")

        asyncio.run(run_ui())
    else:
        st.warning("Please enter a query or inject a sample.")

# --- UI: ARCHITECTURE VISUALIZER ---
st.divider()
st.subheader("🛠️ Orchestration Architecture")



with st.expander("Show Pattern Logic Diagram", expanded=True):
    if "Routing" in selected_pattern:
        st.graphviz_chart('''digraph { rankdir=LR; node [shape=box, style=filled, color=lightblue]; User -> Router; Router -> Security; Router -> Finance; Router -> Ops; }''')
    elif "HITL" in selected_pattern:
        st.graphviz_chart('''digraph { rankdir=TD; Agent -> Draft; Draft -> Human_Review [color=red]; Human_Review -> Execute [label="Yes"]; Human_Review -> Agent [label="No"]; }''')
    else:
        st.info(f"Dynamic architecture for {selected_pattern} is active in the background.")

# --- UI: ROI CALCULATOR ---
st.divider()
st.subheader("📊 Strategic Value & ROI Calculator")

col1, col2 = st.columns([1, 2])
with col1:
    st.markdown("#### Input Parameters")
    avg_salary = st.number_input("Avg. IT Specialist Salary ($)", value=120000)
    manual_hours = st.slider("Manual Hours per Week (Pre-AI)", 10, 500, 100)
    efficiency_gain = st.slider("Target Efficiency Gain (%)", 10, 90, 40)

with col2:
    st.markdown("#### Projected Annual Impact")
    hourly_rate = avg_salary / 2080
    current_annual_cost = hourly_rate * manual_hours * 52
    savings = current_annual_cost * (efficiency_gain / 100)
    hours_saved = (manual_hours * 52) * (efficiency_gain / 100)
    
    m1, m2, m3 = st.columns(3)
    m1.metric("Annual Savings", f"${savings:,.0f}", f"{efficiency_gain}%")
    m2.metric("Hours Reclaimed", f"{hours_saved:,.0f} hrs")
    m3.metric("Hourly Rate", f"${hourly_rate:,.2f}")

    chart_data = pd.DataFrame({
        "Category": ["Current Manual Cost", "Post-Agentic Cost"],
        "Expense ($)": [current_annual_cost, current_annual_cost - savings]
    })
    st.bar_chart(chart_data, x="Category", y="Expense ($)", color="#2E86C1")

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 Strategic Command Center")