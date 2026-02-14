#!/usr/bin/env python3
"""Interactive GLM agent for Mac terminal."""
import os
import sys
import warnings
import subprocess
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from glm_langchain_client import GLMClient

warnings.filterwarnings("ignore", message=".*HMAC key.*")


def execute_command(cmd):
    """Execute shell command and return output."""
    try:
        # Set environment variables from config before executing
        config_path = os.path.join(os.path.dirname(__file__), "config.properties")
        env = os.environ.copy()
        
        if os.path.exists(config_path):
            for line in open(config_path):
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    # Convert property keys to env vars (e.g., gnews.api_key -> GNEWS_API_KEY)
                    if key == "gnews.api_key":
                        env["GNEWS_API_KEY"] = value
        
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, env=env)
        return result.stdout if result.returncode == 0 else f"Error: {result.stderr}"
    except Exception as e:
        return f"Error: {e}"


def main():
    """Run interactive GLM chat in terminal."""
    config_path = os.path.join(os.path.dirname(__file__), "config.properties")
    config = {}
    if os.path.exists(config_path):
        for line in open(config_path):
            if "=" in line and not line.startswith("#"):
                key, value = line.split("=", 1)
                config[key.strip()] = value.strip()
    
    primary_model = config.get("glm.model", "glm-4.6v")
    fallback_model = config.get("glm.fallback_model", "glm-4.7")
    
    client = GLMClient(api_key=os.getenv("ZHIPUAI_API_KEY"), model=primary_model)
    current_model = primary_model
    
    system_prompt = """You are a helpful AI assistant with access to task management tools.

When user asks about tasks, you MUST execute the actual command and report real results:
- To list tasks: python skills/personal-assistant/task_manager.py list
- To add task: python skills/personal-assistant/task_manager.py add "task description" --priority [high|medium|low] --due [date]

IMPORTANT: When you need to check tasks, respond with EXACTLY this format:
EXECUTE: python skills/personal-assistant/task_manager.py list

Do NOT make up task information. Always execute the command first."""
    
    messages = [SystemMessage(content=system_prompt)]
    
    print(f"GLM Chat (using {current_model})")
    print("Type 'exit' or 'quit' to end, 'clear' to reset, 'save-pref key value' to save preference\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit"]:
                break
            
            if user_input.lower() == "clear":
                messages = [SystemMessage(content=system_prompt)]
                print("Chat history cleared.\n")
                continue
            
            # Handle save-pref command
            if user_input.lower().startswith("save-pref "):
                parts = user_input.split(" ", 2)
                if len(parts) >= 3:
                    key, value = parts[1], parts[2]
                    if client.memory:
                        client.memory.save_preference(key, value)
                        print(f"Preference saved: {key} = {value}\n")
                    else:
                        print("Memory not enabled.\n")
                continue
            
            # Handle show-memory command
            if user_input.lower() == "show-memory":
                if client.memory:
                    print(client.memory.get_memory_summary())
                else:
                    print("Memory not enabled.\n")
                continue
            
            messages.append(HumanMessage(content=user_input))
            
            try:
                response = client.invoke(messages)
                
                # Check if response contains command to execute
                if "EXECUTE:" in response:
                    lines = response.split("\n")
                    for line in lines:
                        if line.startswith("EXECUTE:"):
                            cmd = line.replace("EXECUTE:", "").strip()
                            print(f"\n[Executing: {cmd}]")
                            output = execute_command(cmd)
                            print(f"[Output: {output}]")
                            # Add command result to context
                            messages.append(AIMessage(content=f"Command executed: {cmd}\nResult: {output}"))
                            # Ask for interpretation
                            messages.append(HumanMessage(content="Based on the actual result above, answer my question."))
                            response = client.invoke(messages)
                
                print(f"\nAssistant: {response}\n")
                messages.append(AIMessage(content=response))
            except Exception as e:
                if "429" in str(e) and current_model == primary_model:
                    print(f"\n{primary_model} error, switching to {fallback_model}...\n")
                    client = GLMClient(api_key=os.getenv("ZHIPUAI_API_KEY"), model=fallback_model)
                    current_model = fallback_model
                    response = client.invoke(messages)
                    print(f"\nAssistant: {response}\n")
                    messages.append(AIMessage(content=response))
                else:
                    raise
            
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            messages.pop()  # Remove failed user message


if __name__ == "__main__":
    main()
