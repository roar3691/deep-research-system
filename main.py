# deep_research_system/main.py
import os
import uuid
import requests
import json
from typing import Dict, List, TypedDict
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# Check for Tavily API key
if not TAVILY_API_KEY:
    raise ValueError("TAVILY_API_KEY is not set in the .env file")

# Initialize Tavily tool
tavily_tool = TavilySearchResults(max_results=5)

# OpenRouter LLM client
class OpenRouterLLM:
    def __init__(self, model="thudm/glm-4-32b:free"):
        self.model = model
        self.api_key = OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1/chat/completions"

    def invoke(self, prompt: str) -> str:
        response = requests.post(
            url=self.base_url,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "Deep Research System",
            },
            data=json.dumps({
                "model": self.model,
                "messages": [{"role": "user", "content": prompt}],
            })
        )
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    def bind_tools(self, tools):
        def tool_bound_invoke(prompt: str) -> Dict:
            content = self.invoke(prompt)
            return {
                "content": content,
                "tool_calls": [{"name": "tavily_search_results_json", "args": {"query": prompt}}]
            }
        return tool_bound_invoke

# Initialize LLM
llm = OpenRouterLLM()

# Define state for LangGraph
class ResearchState(TypedDict):
    query: str
    research_data: List[Dict]
    draft_answer: str
    final_answer: str

# Research Agent Node
def research_agent(state: ResearchState) -> ResearchState:
    query = state["query"]
    prompt = (
        f"You are a research agent. Use the Tavily search tool to gather relevant information for the query: {query}. "
        "Summarize the findings in a structured format with source URLs."
    )
    chain = llm.bind_tools([tavily_tool])
    response = chain(prompt)
    
    research_data = []
    if isinstance(response, dict) and "tool_calls" in response:
        for tool_call in response["tool_calls"]:
            if tool_call["name"] == tavily_tool.name:
                results = tavily_tool.invoke(tool_call["args"])
                for result in results:
                    summary = llm.invoke(
                        f"Summarize this content in 2-3 sentences: {result['content']}"
                    )
                    research_data.append({
                        "content": result["content"],
                        "url": result["url"],
                        "summary": summary
                    })
    
    return {"research_data": research_data}

# Answer Drafter Agent Node
def answer_drafter(state: ResearchState) -> ResearchState:
    research_data = state["research_data"]
    query = state["query"]
    
    context = "\n\n".join(
        f"Source: {data['url']}\nSummary: {data['summary']}\nContent: {data['content']}"
        for data in research_data
    )
    
    prompt = (
        f"You are an answer drafter. Using the following research data, draft a concise and accurate answer to the query: {query}\n\n{context}"
    )
    draft_answer = llm.invoke(prompt)
    
    return {"draft_answer": draft_answer}

# Final Answer Refiner Node
def final_answer_refiner(state: ResearchState) -> ResearchState:
    draft_answer = state["draft_answer"]
    query = state["query"]
    
    prompt = (
        f"You are a final answer refiner. Review the draft answer and refine it to be clear, concise, and professional: {draft_answer}\n\nQuery: {query}"
    )
    final_answer = llm.invoke(prompt)
    
    return {"final_answer": final_answer}

# Define LangGraph workflow
def create_workflow():
    workflow = StateGraph(ResearchState)
    
    workflow.add_node("research_agent", research_agent)
    workflow.add_node("answer_drafter", answer_drafter)
    workflow.add_node("final_answer_refiner", final_answer_refiner)
    
    workflow.set_entry_point("research_agent")
    workflow.add_edge("research_agent", "answer_drafter")
    workflow.add_edge("answer_drafter", "final_answer_refiner")
    workflow.add_edge("final_answer_refiner", END)
    
    return workflow.compile()

# Function to run the research system
def run_deep_research(query: str) -> Dict:
    app = create_workflow()
    initial_state = ResearchState(
        query=query,
        research_data=[],
        draft_answer="",
        final_answer=""
    )
    result = app.invoke(initial_state)
    return result