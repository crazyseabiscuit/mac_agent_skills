"""Long-term and short-term memory management for GLM agents."""
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage


class MemoryManager:
    """Manages both short-term (session) and long-term (persistent) memory."""
    
    def __init__(self, memory_dir: Optional[str] = None):
        """Initialize memory manager.
        
        Args:
            memory_dir: Directory to store long-term memories (defaults to .memories/)
        """
        if memory_dir is None:
            memory_dir = Path(__file__).parent / ".memories"
        
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(exist_ok=True)
        
        # Short-term memory (current session)
        self.short_term: Dict[str, Any] = {
            "messages": [],
            "context": {},
            "created_at": datetime.now().isoformat(),
        }
        
        # Long-term memory files paths
        self.preferences_file = self.memory_dir / "preferences.json"
        self.context_file = self.memory_dir / "context.json"
        self.history_file = self.memory_dir / "history.json"
    
    def save_preference(self, key: str, value: Any) -> None:
        """Save a user preference to long-term memory.
        
        Args:
            key: Preference key
            value: Preference value
        """
        preferences = self._load_json(self.preferences_file)
        preferences[key] = value
        preferences["updated_at"] = datetime.now().isoformat()
        self._save_json(self.preferences_file, preferences)
    
    def get_preference(self, key: str, default: Any = None) -> Any:
        """Retrieve a preference from long-term memory.
        
        Args:
            key: Preference key
            default: Default value if not found
            
        Returns:
            Preference value or default
        """
        preferences = self._load_json(self.preferences_file)
        return preferences.get(key, default)
    
    def save_context(self, key: str, value: Any) -> None:
        """Save context information to long-term memory.
        
        Args:
            key: Context key
            value: Context value
        """
        context = self._load_json(self.context_file)
        context[key] = value
        context["updated_at"] = datetime.now().isoformat()
        self._save_json(self.context_file, context)
    
    def get_context(self, key: str, default: Any = None) -> Any:
        """Retrieve context from long-term memory.
        
        Args:
            key: Context key
            default: Default value if not found
            
        Returns:
            Context value or default
        """
        context = self._load_json(self.context_file)
        return context.get(key, default)
    
    def get_all_context(self) -> Dict[str, Any]:
        """Get all context information."""
        return self._load_json(self.context_file)
    
    def add_to_history(self, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        """Add message to long-term conversation history.
        
        Args:
            role: Message role (user/assistant)
            content: Message content
            metadata: Optional metadata
        """
        if self.history_file.exists():
            with open(self.history_file, "r") as f:
                history = json.load(f)
        else:
            history = []
        
        entry = {
            "timestamp": datetime.now().isoformat(),
            "role": role,
            "content": content,
        }
        if metadata:
            entry["metadata"] = metadata
        
        history.append(entry)
        with open(self.history_file, "w") as f:
            json.dump(history, f, indent=2)
    
    def get_history(self, limit: Optional[int] = None) -> List[Dict]:
        """Retrieve conversation history.
        
        Args:
            limit: Maximum number of entries to return
            
        Returns:
            List of history entries
        """
        if self.history_file.exists():
            with open(self.history_file, "r") as f:
                history = json.load(f)
        else:
            history = []
        
        if limit:
            return history[-limit:]
        return history
    
    def clear_short_term_memory(self) -> None:
        """Clear short-term memory (messages for current session)."""
        self.short_term["messages"] = []
        self.short_term["context"] = {}
    
    def add_short_term_message(self, message: BaseMessage) -> None:
        """Add message to short-term memory.
        
        Args:
            message: LangChain message object
        """
        msg_dict = {
            "role": "user" if isinstance(message, HumanMessage) else "assistant",
            "content": message.content,
            "type": type(message).__name__,
        }
        self.short_term["messages"].append(msg_dict)
    
    def get_short_term_messages(self) -> List[Dict]:
        """Get all short-term messages."""
        return self.short_term["messages"]
    
    def get_memory_summary(self) -> str:
        """Get a summary of long-term memory for system prompt injection.
        
        Returns:
            Formatted string with memory information
        """
        preferences = self._load_json(self.preferences_file)
        context = self._load_json(self.context_file)
        history_len = len(self._load_json(self.history_file))
        
        summary = "## Your Long-Term Memory\n\n"
        
        if preferences:
            summary += "### User Preferences\n"
            for key, value in preferences.items():
                if key != "updated_at":
                    summary += f"- {key}: {value}\n"
            summary += "\n"
        
        if context:
            summary += "### Context Information\n"
            for key, value in context.items():
                if key != "updated_at":
                    summary += f"- {key}: {value}\n"
            summary += "\n"
        
        summary += f"### Conversation History\n- Total messages: {history_len}\n"
        
        return summary
    
    def export_long_term_memory(self, filepath: str) -> None:
        """Export long-term memory to JSON file.
        
        Args:
            filepath: Path to export file
        """
        export_data = {
            "preferences": self._load_json(self.preferences_file),
            "context": self._load_json(self.context_file),
            "history": self._load_json(self.history_file),
            "exported_at": datetime.now().isoformat(),
        }
        with open(filepath, "w") as f:
            json.dump(export_data, f, indent=2)
    
    def import_long_term_memory(self, filepath: str) -> None:
        """Import long-term memory from JSON file.
        
        Args:
            filepath: Path to import file
        """
        with open(filepath, "r") as f:
            data = json.load(f)
        
        if "preferences" in data:
            self._save_json(self.preferences_file, data["preferences"])
        if "context" in data:
            self._save_json(self.context_file, data["context"])
        if "history" in data:
            self._save_json(self.history_file, data["history"])
    
    def _load_json(self, filepath: Path) -> Dict:
        """Load JSON file, return empty dict if not exists."""
        if filepath.exists():
            with open(filepath, "r") as f:
                return json.load(f)
        return {}
    
    def _save_json(self, filepath: Path, data: Dict) -> None:
        """Save JSON file."""
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)
