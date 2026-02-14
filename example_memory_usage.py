#!/usr/bin/env python3
"""Simple example of using long-term memory."""
import os
from langchain_core.messages import HumanMessage, SystemMessage
from glm_langchain_client import GLMClient


def main():
    """Example: Using long-term memory with GLM."""
    
    # Initialize client with memory enabled
    client = GLMClient(
        api_key=os.getenv("ZHIPUAI_API_KEY"),
        enable_memory=True
    )
    
    # Example 1: Save user preferences
    print("1️⃣  Saving preferences...")
    client.memory.save_preference("language", "Chinese")
    client.memory.save_preference("style", "concise")
    
    # Example 2: Save context
    print("2️⃣  Saving context...")
    client.memory.save_context("user_name", "Alice")
    client.memory.save_context("project", "AI Assistant")
    
    # Example 3: Use in conversation
    print("3️⃣  Sending message (memory will be auto-injected)...")
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="Who am I and what am I working on?")
    ]
    
    try:
        response = client.invoke(messages)
        print(f"\n📝 Assistant: {response}\n")
    except Exception as e:
        print(f"Note: API call requires valid ZHIPUAI_API_KEY")
        print(f"Error: {e}\n")
    
    # Example 4: View memory
    print("4️⃣  Viewing long-term memory:")
    print(client.memory.get_memory_summary())
    
    # Example 5: Export for backup
    print("5️⃣  Exporting memory...")
    client.memory.export_long_term_memory("memory_backup.json")
    print("✓ Memory exported to memory_backup.json")
    
    print("\n✨ Examples complete!")


if __name__ == "__main__":
    main()
