#!/usr/bin/env python3
"""
LLM helper to ensure all calls use LangChain for LangSmith tracing
"""
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage

def call_llm(system_prompt: str, user_prompt: str, model: str = "gpt-4o-mini", temperature: float = 0.2, max_tokens: int = 2000) -> str:
    """
    Call LLM using LangChain (for LangSmith tracing).
    
    Args:
        system_prompt: System message content
        user_prompt: User message content
        model: Model name (default: gpt-4o-mini)
        temperature: Temperature (default: 0.2)
        max_tokens: Max tokens (default: 2000)
    
    Returns:
        Response content as string
    """
    llm = ChatOpenAI(model=model, temperature=temperature, max_tokens=max_tokens)
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt)
    ]
    response = llm.invoke(messages)
    return response.content.strip()
