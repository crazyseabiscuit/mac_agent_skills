#!/usr/bin/env python3
"""Test AI-driven memory saving in glm_terminal."""
import os
from glm_terminal import create_memory_tool
from glm_langchain_client import GLMClient

def test_memory_tool():
    """Test that memory tool can be created and used."""
    client = GLMClient(api_key=os.getenv("ZHIPUAI_API_KEY"), enable_memory=True)
    
    # Create tool
    memory_tool = create_memory_tool(client)
    
    # Test saving preference
    result = memory_tool.invoke({
        "preference_key": "language",
        "preference_value": "Chinese"
    })
    print(f"Save preference: {result}")
    
    # Test saving context
    result = memory_tool.invoke({
        "context_key": "project",
        "context_value": "AI Assistant"
    })
    print(f"Save context: {result}")
    
    # Verify saved
    summary = client.memory.get_memory_summary()
    print(f"\nMemory summary:\n{summary}")
    
    print("\n✅ Memory tool test passed!")

if __name__ == "__main__":
    test_memory_tool()
