# agents/summarizer.py
from tools.call_llm import call_llm
from orchestration.state import ResearchState

def summarizer_agent(state: ResearchState) -> ResearchState:
    prompt = f"""
    Give some potential research areas using the context below. 

    Query:
    {state['query']}

    Context:
    {state['final_context']}
    """

    state["final_context"] = call_llm(prompt)
    return state