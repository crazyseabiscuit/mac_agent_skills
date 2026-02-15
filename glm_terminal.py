#!/usr/bin/env python3
"""Interactive GLM agent for Mac terminal."""
import os
import sys
import warnings
import subprocess
import json
import readline  # Enable better line editing (backspace, arrow keys, etc.)
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langchain_core.tools import tool
from glm_langchain_client import GLMClient

warnings.filterwarnings("ignore", message=".*HMAC key.*")

# Import save_user_profile for automatic profile updating
try:
    from save_user_profile import save_analyzed_user_profile
    SAVE_PROFILE_AVAILABLE = True
except ImportError:
    SAVE_PROFILE_AVAILABLE = False


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


def create_memory_tool(client):
    """Create tool for AI to save user preferences and context."""
    @tool
    def save_user_memory(preference_key: str = None, preference_value: str = None, 
                        context_key: str = None, context_value: str = None) -> str:
        """Save user preferences or context to long-term memory.
        Use this when user mentions their preferences, interests, or background information.
        
        Args:
            preference_key: Key for user preference (e.g., "language", "content_type")
            preference_value: Value for the preference
            context_key: Key for user context (e.g., "project", "primary_interest")
            context_value: Value for the context
        
        Returns:
            Confirmation message
        """
        if not client.memory:
            return "Memory not enabled"
        
        saved = []
        if preference_key and preference_value:
            client.memory.save_preference(preference_key, preference_value)
            saved.append(f"preference: {preference_key}={preference_value}")
        
        if context_key and context_value:
            client.memory.save_context(context_key, context_value)
            saved.append(f"context: {context_key}={context_value}")
        
        return f"✓ Saved to memory: {'; '.join(saved)}" if saved else "No data to save"
    
    return save_user_memory


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
    
    system_prompt = """You are a helpful AI assistant with access to various tools.

When user asks you to search or find information, you MUST execute the actual command:

**News Search** (for general news, sports, tech, etc.):
EXECUTE: python skills/news-search/search_news.py "search query" --limit 10

**China Content Search** (for Chinese movies, TV shows, entertainment):
EXECUTE: python skills/china-search/china_search.py "search query" --type [movie|tv|entertainment]

**Task Management**:
- List tasks: EXECUTE: python skills/personal-assistant/task_manager.py list
- Add task: EXECUTE: python skills/personal-assistant/task_manager.py add "task description" --priority [high|medium|low] --due [date]

IMPORTANT: 
1. When you need to search or check information, respond with EXACTLY this format on a new line:
   EXECUTE: [command]
2. After seeing search results, you will be asked to summarize them in Chinese.
3. When user mentions their preferences, interests, or background, respond with:
   SAVE_MEMORY: preference_key=value OR context_key=value

Do NOT make up information. Always execute the command first to get real data."""
    
    messages = [SystemMessage(content=system_prompt)]
    
    print(f"GLM Chat (using {current_model})")
    print("Type 'exit' or 'quit' to end, 'clear' to reset, 'save-pref key value' to save preference\n")
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ["exit", "quit"]:
                # Save user profile before exiting
                if SAVE_PROFILE_AVAILABLE:
                    print("\n💾 Saving user profile before exit...")
                    try:
                        save_analyzed_user_profile()
                        print("✅ User profile saved successfully!\n")
                    except Exception as e:
                        print(f"⚠️ Could not save profile: {e}\n")
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
                
                # Check if AI wants to save memory
                if "SAVE_MEMORY:" in response:
                    lines = response.split("\n")
                    for line in lines:
                        if line.startswith("SAVE_MEMORY:"):
                            mem_data = line.replace("SAVE_MEMORY:", "").strip()
                            if "=" in mem_data:
                                key, value = mem_data.split("=", 1)
                                key = key.strip()
                                value = value.strip()
                                # Determine if preference or context based on key
                                if key in ["language", "content_type", "region_preference", "preferred_style"]:
                                    client.memory.save_preference(key, value)
                                    print(f"[Saved preference: {key}={value}]")
                                else:
                                    client.memory.save_context(key, value)
                                    print(f"[Saved context: {key}={value}]")
                
                # Check if response contains command to execute
                executed_command = False
                if "EXECUTE:" in response:
                    lines = response.split("\n")
                    for line in lines:
                        if line.startswith("EXECUTE:"):
                            cmd = line.replace("EXECUTE:", "").strip()
                            print(f"\n[Executing: {cmd}]\n")
                            output = execute_command(cmd)
                            # Debug: check if output is empty
                            if not output or not output.strip():
                                print("[Warning: Command produced no output]")
                                output = "Command executed but produced no output."
                            # Print the actual output to user
                            print(output)
                            print()  # Extra newline for readability
                            # Add command result to context and ask AI to summarize
                            messages.append(AIMessage(content=f"Command executed: {cmd}\nResult: {output}"))
                            messages.append(HumanMessage(content="请用中文总结上面的搜索结果，提取关键信息。"))
                            # Get AI's summary
                            summary = client.invoke(messages)
                            print(f"\nAssistant: {summary}\n")
                            messages.append(AIMessage(content=summary))
                            executed_command = True
                            break
                
                # Print normal AI responses (only if we didn't execute a command)
                if not executed_command:
                    print(f"\nAssistant: {response}\n")
                    messages.append(AIMessage(content=response))
                
                # Periodically update user profile (every 5 exchanges = 10 messages)
                if SAVE_PROFILE_AVAILABLE and len(messages) % 10 == 0:
                    try:
                        save_analyzed_user_profile()
                    except Exception as e:
                        # Silently fail - don't disrupt user experience
                        pass
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
            # Save user profile before exiting on Ctrl+C
            if SAVE_PROFILE_AVAILABLE:
                print("\n\n💾 Saving user profile...")
                try:
                    save_analyzed_user_profile()
                    print("✅ User profile saved successfully!")
                except Exception as e:
                    print(f"⚠️ Could not save profile: {e}")
            print("Goodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            messages.pop()  # Remove failed user message


if __name__ == "__main__":
    main()
