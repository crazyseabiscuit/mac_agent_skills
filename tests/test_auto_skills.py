#!/usr/bin/env python3
"""Test GLM client with auto-loaded skills."""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from glm_langchain_client import GLMClient
from langchain_core.messages import HumanMessage

# Initialize client - skills auto-load from ./skills directory
client = GLMClient(model="glm-4.6v", temperature=0.7)

# Simple query
response = client.invoke([
    HumanMessage(content="帮我添加一个任务：明天开会")
])

print(response)
