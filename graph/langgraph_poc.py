# graph/langgraph_poc.py
from langgraph.graph import StateGraph, START

def run_poc_graph():
    # Import nodes (functions) from agents
    from agents.jira_agent import fetch_ticket
    from agents.github_agent import analyze_repo

    # Define your state structure
    from typing_extensions import TypedDict
    class PoCState(TypedDict):
        ticket: dict
        analysis: dict

    builder = StateGraph(PoCState)

    builder.add_node(fetch_ticket)
    builder.add_node(analyze_repo)

    builder.add_edge(START, "fetch_ticket")
    builder.add_edge("fetch_ticket", "analyze_repo")

    graph = builder.compile()

    print("✅ LangGraph compiled successfully!")
    graph.invoke({})
