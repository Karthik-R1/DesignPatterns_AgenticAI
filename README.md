nterface.

📊 CIO Agentic Design Patterns Suite

Validation Status: 21/21 PASSED

This repository contains a production-grade implementation of 21 Agentic Design Patterns tailored for a Chief Information Officer (CIO) persona. These patterns use the Google ADK and Ollama (Llama 3.2) to automate strategic IT decision-making, risk assessment, and infrastructure management.

📂 Project Structure
All patterns, in GitHub, are located in their repective directory:

1) pattern_01_routing.py ... pattern_21_exploration.py: The individual logic for each of the 21 agentic behaviors.
2) agent_dashboard.py: The central Streamlit Dashboard that imports and executes these patterns.
3) validate_patterns.py: The master test suite used to achieve the 21/21 score.
4) requirements.txt: Project dependencies.


🚀 Getting Started
1. Prerequisites: Ensure you have Ollama installed and the model downloaded:
Bash
ollama run llama3.2

2. Installation: Install the required libraries:
Bash
pip install google-genai streamlit litellm

3. Running the Dashboard: Since all files are in the same folder, Streamlit can easily import each pattern as a module. Launch the app using:
Bash
streamlit run app.py

🛠️ Pattern Catalog:
The suite covers the three core pillars of Agentic AI:

Category                                                      Patterns Included
Architectural                              Routing (01), Chaining (02), Parallelization (03), Router-Worker (04)Collaborative                              Multi-Agent (07), Team (08), Orchestrator (09), MCP (10)
Governance                                 HITL (13), RAG (14), Guardrails (18), Evaluation (19)

🧪 Validation
To re-verify the integrity of the suite, run the validator script:

PowerShell
python validate_patterns.py
Expected Output: RESULTS: 21 Passed, 0 Failed.

📝 Usage Example (Pattern 13: HITL)
When using the dashboard, high-risk requests like "Migrate Database" will trigger Pattern 13, which pauses for your manual approval before the agent continues the simulated deployment.
