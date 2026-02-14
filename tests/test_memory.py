#!/usr/bin/env python3
"""Demo script showing long-term memory functionality."""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from glm_langchain_client import GLMClient


def demo_memory():
    """Demonstrate long-term memory features."""
    
    print("=" * 60)
    print("Long-Term Memory Demo")
    print("=" * 60)
    
    # Initialize client with memory enabled
    client = GLMClient(
        api_key=os.getenv("ZHIPUAI_API_KEY"),
        enable_memory=True,
        memory_dir=".demo_memories"
    )
    
    if not client.memory:
        print("Error: Memory not initialized")
        return
    
    print("\n1. Saving Preferences to Long-Term Memory")
    print("-" * 60)
    client.memory.save_preference("user_name", "Alice")
    client.memory.save_preference("language", "Chinese")
    client.memory.save_preference("timezone", "Asia/Shanghai")
    print("✓ Saved: user_name, language, timezone")
    
    print("\n2. Saving Context Information")
    print("-" * 60)
    client.memory.save_context("project", "AI Assistant")
    client.memory.save_context("team_size", "5")
    print("✓ Saved: project, team_size")
    
    print("\n3. Retrieving Preferences")
    print("-" * 60)
    name = client.memory.get_preference("user_name")
    lang = client.memory.get_preference("language")
    print(f"  User Name: {name}")
    print(f"  Language: {lang}")
    
    print("\n4. Memory Summary (will be injected into system prompt)")
    print("-" * 60)
    summary = client.memory.get_memory_summary()
    print(summary)
    
    print("\n5. Checking Memory Files")
    print("-" * 60)
    memory_dir = Path(".demo_memories")
    if memory_dir.exists():
        files = list(memory_dir.glob("*.json"))
        for f in files:
            size = f.stat().st_size
            print(f"  ✓ {f.name} ({size} bytes)")
    
    print("\n6. Simulating Message History")
    print("-" * 60)
    client.memory.add_to_history("user", "Hello, can you help me?")
    client.memory.add_to_history("assistant", "Of course! I'm here to help.")
    client.memory.add_to_history("user", "What's the current project status?")
    client.memory.add_to_history("assistant", "The project is progressing well...")
    history = client.memory.get_history()
    print(f"✓ Added {len(history)} messages to history")
    print(f"  Last message: {history[-1]['role']}: {history[-1]['content'][:50]}...")
    
    print("\n7. Exporting Memory")
    print("-" * 60)
    export_file = ".demo_memories_export.json"
    client.memory.export_long_term_memory(export_file)
    print(f"✓ Exported to {export_file}")
    
    print("\n8. Clearing Short-Term Memory")
    print("-" * 60)
    client.memory.clear_short_term_memory()
    print("✓ Short-term memory cleared")
    print(f"  Messages in short-term: {len(client.memory.get_short_term_messages())}")
    
    print("\n" + "=" * 60)
    print("Demo Complete!")
    print("=" * 60)
    print(f"\nMemory directory: {memory_dir.absolute()}")
    print("Files created:")
    print("  - preferences.json")
    print("  - context.json")
    print("  - history.json")
    print("\nTo clean up, run: rm -rf .demo_memories .demo_memories_export.json")


if __name__ == "__main__":
    try:
        demo_memory()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
