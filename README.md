# Deep Research AI Agentic System with Streamlit UI

## Overview
This project implements a Deep Research AI Agentic System using LangChain, LangGraph, Tavily for web-based information gathering, OpenRouter for LLM interactions, and Streamlit for an interactive UI. The system features a multi-agent architecture with:
1. **Research Agent**: Crawls websites using Tavily and summarizes findings.
2. **Answer Drafter Agent**: Synthesizes research data into a coherent draft answer.
3. **Final Answer Refiner**: Polishes the draft into a professional response.

The project is deployed at: https://huggingface.co/spaces/roar3691/research-agent

## File Descriptions





**app.py**: The main entry point for the Streamlit web application. It defines the user interface, handles user input (research queries), and displays results. It imports the run_deep_research function from main.py to execute the agentic workflow and render outputs.



**main.py**: Contains the core logic of the multi-agent system. It defines the LangGraph workflow, agent nodes (Research Agent, Answer Drafter, Final Answer Refiner), Tavily search integration, and OpenRouter LLM client. It provides the run_deep_research function used by app.py.



**.env.example**: A template for the .env file, specifying required environment variables (TAVILY_API_KEY and OPENROUTER_API_KEY). Users must create a .env file based on this template with valid API keys.



**requirements.txt**: Lists the Python dependencies (langchain==0.2.16, langchain-community==0.2.17, langgraph==0.1.19, python-dotenv==1.0.1, requests==2.31.0, streamlit==1.31.0, protobuf==4.25.5) for installation via pip.





## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/roar3691/deep-research-system.git
2. Set up the virtual environment with conda:
   ```bash
   conda create -n tf_env python=3.12
   conda activate tf_env
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Set up environment variables in a `.env` file (use `.env.example` as a template):
   ```plaintext
   TAVILY_API_KEY=tavily_api_key
   OPENROUTER_API_KEY=openrouter_api_key
   ```
5. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## Usage
1. Open the Streamlit app in your browser (typically at `http://localhost:8501`).
2. Enter a research query (e.g., "What are the latest advancements in AI for healthcare?").
3. Click "Run Research" to view the final answer and research data.
4. Expand research data entries to see summaries and source content.

Alternatively, run the system programmatically:
```python
from main import run_deep_research
result = run_deep_research("What are the latest advancements in AI for healthcare?")
print(result["final_answer"])
```

## System Architecture
- **LangChain**: Manages tool integration (Tavily) and prompt templates.
- **LangGraph**: Orchestrates the agentic workflow with a stateful graph.
- **Tavily**: Provides web search capabilities for real-time data.
- **OpenRouter**: Powers LLM interactions using the `thudm/glm-4-32b:free` model.
- **Streamlit**: Provides an interactive UI for query input and result display.
- **Agents**:
  - Research Agent: Gathers and summarizes web data.
  - Answer Drafter: Compiles research into a draft response.
  - Final Refiner: Enhances clarity and professionalism.

## Notes
- A valid Tavily API key is required (obtain from https://tavily.com).
- The OpenRouter API key is included in `.env.example` for demonstration. Secure it in production.
- The tool-binding mechanism for Tavily is simplified for OpenRouter compatibility.
- Streamlit UI includes error handling, API key validation, and a loading spinner.

## Troubleshooting
- If `conda activate tf_env` fails, recreate the environment:
  ```bash
  conda create -n tf_env python=3.12
  conda activate tf_env
  ```
- If dependency conflicts occur, clear pip cache:
  ```bash
  pip cache purge
  pip install -r requirements.txt
  ```
- Verify `langchain-community`:
  ```bash
  pip show langchain-community
  ```


## Submission
This project is submitted for the Kairon Qualifying Assignment. For further details, contact [contact@kairon.co.in](mailto:contact@kairon.co.in).
