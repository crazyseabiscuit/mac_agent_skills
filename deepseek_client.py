#!/usr/bin/env python3
"""DeepSeek LangChain client."""
import os
from langchain_openai import ChatOpenAI


def create_deepseek_client(
    model="deepseek-chat",
    api_key=None,
    temperature=0.7,
    max_tokens=None,
):
    """Create a DeepSeek client using LangChain.
    
    Args:
        model: Model name (default: deepseek-chat)
        api_key: DeepSeek API key (defaults to DEEPSEEK_API_KEY env var)
        temperature: Sampling temperature (0-2)
        max_tokens: Maximum tokens to generate
    
    Returns:
        ChatOpenAI instance configured for DeepSeek
    """
    api_key = api_key or os.getenv("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY not found in environment")
    
    return ChatOpenAI(
        model=model,
        api_key=api_key,
        base_url="https://api.deepseek.com",
        temperature=temperature,
        max_tokens=max_tokens,
    )


if __name__ == "__main__":
    # Example usage
    client = create_deepseek_client()
    
    response = client.invoke("你好，请介绍一下你自己")
    print(response.content)
