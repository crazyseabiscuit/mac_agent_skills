"""LangChain-compatible GLM client for ZhipuAI."""
import os
from pathlib import Path
from typing import Any, List, Optional
from langchain_community.chat_models import ChatZhipuAI
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, BaseMessage
from memory_manager import MemoryManager


class GLMClient:
    """Minimal LangChain-compatible client for GLM models."""
    
    @staticmethod
    def _load_config():
        """Load configuration from properties file."""
        config_path = Path(__file__).parent / "config.properties"
        config = {}
        if config_path.exists():
            for line in config_path.read_text().splitlines():
                if "=" in line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    config[key.strip()] = value.strip()
        return config
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        streaming: Optional[bool] = None,
        skills_dir: Optional[str] = None,
        memory_dir: Optional[str] = None,
        enable_memory: bool = True,
    ):
        """Initialize GLM client.
        
        Args:
            api_key: ZhipuAI API key (defaults to ZHIPUAI_API_KEY env var)
            model: Model name (defaults to config.properties)
            temperature: Sampling temperature (defaults to config.properties)
            streaming: Enable streaming responses (defaults to config.properties)
            skills_dir: Path to skills directory (auto-loads all SKILL.md files)
            memory_dir: Directory for long-term memory (defaults to .memories/)
            enable_memory: Enable long-term memory (default: True)
        """
        if api_key:
            os.environ["ZHIPUAI_API_KEY"] = api_key
        
        config = self._load_config()
        model = model or config.get("glm.model", "glm-4.7")
        temperature = temperature if temperature is not None else float(config.get("glm.temperature", "0.5"))
        streaming = streaming if streaming is not None else config.get("glm.streaming", "false").lower() == "true"
        
        self.chat = ChatZhipuAI(
            model=model,
            temperature=temperature,
            streaming=streaming,
        )
        
        # Initialize memory manager
        self.memory: Optional[MemoryManager] = None
        if enable_memory:
            self.memory = MemoryManager(memory_dir=memory_dir)
        
        # Load skills
        self.skills_context = self._load_skills(skills_dir)
    
    def _load_skills(self, skills_dir: Optional[str]) -> str:
        """Load all SKILL.md files from skills directory."""
        if not skills_dir:
            default_dir = Path(__file__).parent / "skills"
            if default_dir.exists():
                skills_dir = str(default_dir)
            else:
                return ""
        
        skills_path = Path(skills_dir)
        if not skills_path.exists():
            return ""
        
        skills = []
        for skill_dir in skills_path.iterdir():
            if skill_dir.is_dir():
                skill_file = skill_dir / "SKILL.md"
                if skill_file.exists():
                    skills.append(skill_file.read_text())
        
        return "\n\n---\n\n".join(skills) if skills else ""
    
    def invoke(self, messages: List[BaseMessage]) -> str:
        """Send messages and get response.
        
        Args:
            messages: List of message objects (SystemMessage, HumanMessage, AIMessage)
            
        Returns:
            Response content as string
        """
        # Inject skills into system message if available
        if self.skills_context and messages:
            for i, msg in enumerate(messages):
                if isinstance(msg, SystemMessage):
                    messages[i] = SystemMessage(content=f"{msg.content}\n\n# Available Skills\n\n{self.skills_context}")
                    break
            else:
                # No system message found, prepend one
                messages.insert(0, SystemMessage(content=f"# Available Skills\n\n{self.skills_context}"))
        
        # Inject long-term memory into system message if enabled
        if self.memory and messages:
            memory_summary = self.memory.get_memory_summary()
            if memory_summary.strip():
                for i, msg in enumerate(messages):
                    if isinstance(msg, SystemMessage):
                        messages[i] = SystemMessage(content=f"{msg.content}\n\n{memory_summary}")
                        break
        
        response = self.chat.invoke(messages)
        
        # Save to long-term memory if enabled
        if self.memory and messages:
            for msg in messages:
                if isinstance(msg, HumanMessage):
                    self.memory.add_to_history("user", msg.content)
            self.memory.add_to_history("assistant", response.content)
        
        return response.content
    
    async def ainvoke(self, messages: List[BaseMessage]) -> str:
        """Async version of invoke."""
        response = await self.chat.agenerate([messages])
        return response.generations[0][0].text


# Example usage
if __name__ == "__main__":
    # Initialize client (uses config.properties)
    client = GLMClient(
        api_key=os.getenv("ZHIPUAI_API_KEY"),
    )
    
    # Create messages
    messages = [
        SystemMessage(content="You are a helpful assistant."),
        HumanMessage(content="What is LangChain?"),
    ]
    
    # Get response
    response = client.invoke(messages)
    print(response)
