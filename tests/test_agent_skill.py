#!/usr/bin/env python3
"""GLM Agent with personal assistant skill."""
import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from glm_langchain_client import GLMClient
from langchain_core.messages import SystemMessage, HumanMessage

# Load skill
SKILL_PATH = Path(__file__).parent.parent / "skills" / "personal-assistant" / "SKILL.md"
skill_content = SKILL_PATH.read_text()

# Initialize GLM client
client = GLMClient(model="glm-4.6v", temperature=0.7)

# System prompt with skill
system_prompt = f"""You are a personal assistant agent with access to task management and note-taking capabilities.

{skill_content}

When users ask about tasks, scheduling, or notes, use the instructions from the skill above to help them."""

def chat(user_message: str) -> str:
    """Send message to agent and get response."""
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_message)
    ]
    return client.invoke(messages)

if __name__ == "__main__":
    # Test cases
    test_queries = [
        "帮我添加一个任务：明天买菜，优先级高",
        "我想记录一个想法",
        "如何查看我的待办事项？",
    ]
    
    for query in test_queries:
        print(f"\n用户: {query}")
        response = chat(query)
        print(f"助手: {response}")
        print("-" * 50)
