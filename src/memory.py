"""
Memory System for the Agent
Implements both short-term (conversation) and long-term (vector store) memory
"""

from typing import List, Dict, Optional
from datetime import datetime
import json
from pathlib import Path


class ConversationMemory:
    """Manages conversation history and context"""
    
    def __init__(self, max_messages: int = 50):
        self.max_messages = max_messages
        self.conversations: Dict[str, List[Dict]] = {}
    
    def add_message(self, thread_id: str, role: str, content: str, metadata: Optional[Dict] = None):
        """Add a message to conversation history"""
        if thread_id not in self.conversations:
            self.conversations[thread_id] = []
        
        message = {
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        
        self.conversations[thread_id].append(message)
        
        # Keep only recent messages
        if len(self.conversations[thread_id]) > self.max_messages:
            self.conversations[thread_id] = self.conversations[thread_id][-self.max_messages:]
    
    def get_conversation(self, thread_id: str) -> List[Dict]:
        """Retrieve conversation history"""
        return self.conversations.get(thread_id, [])
    
    def clear_conversation(self, thread_id: str):
        """Clear conversation history for a thread"""
        if thread_id in self.conversations:
            del self.conversations[thread_id]


class LongTermMemory:
    """
    Simulates a vector database for long-term memory
    In production, use Chroma, Pinecone, or Qdrant
    """
    
    def __init__(self, storage_path: str = "data/memory.json"):
        self.storage_path = Path(storage_path)
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        self.memories: List[Dict] = self._load_memories()
    
    def _load_memories(self) -> List[Dict]:
        """Load memories from disk"""
        if self.storage_path.exists():
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return []
    
    def _save_memories(self):
        """Save memories to disk"""
        with open(self.storage_path, 'w') as f:
            json.dump(self.memories, f, indent=2)
    
    def store(self, content: str, metadata: Dict, category: str = "general"):
        """
        Store a memory
        
        Args:
            content: The content to remember
            metadata: Additional metadata (source, importance, etc.)
            category: Category of memory (research, task, preference, etc.)
        """
        memory = {
            "id": f"mem_{len(self.memories)}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "content": content,
            "metadata": metadata,
            "category": category,
            "timestamp": datetime.now().isoformat(),
            "access_count": 0
        }
        
        self.memories.append(memory)
        self._save_memories()
    
    def search(self, query: str, category: Optional[str] = None, limit: int = 5) -> List[Dict]:
        """
        Search memories (simplified keyword matching)
        In production, use semantic search with embeddings
        
        Args:
            query: Search query
            category: Filter by category
            limit: Maximum number of results
        
        Returns:
            List of relevant memories
        """
        results = []
        query_lower = query.lower()
        
        for memory in self.memories:
            # Filter by category if specified
            if category and memory["category"] != category:
                continue
            
            # Simple keyword matching (in production, use embeddings)
            content_lower = memory["content"].lower()
            if any(word in content_lower for word in query_lower.split()):
                memory["access_count"] += 1
                results.append(memory)
        
        # Sort by relevance (access count as proxy) and limit
        results.sort(key=lambda x: x["access_count"], reverse=True)
        self._save_memories()
        
        return results[:limit]
    
    def get_recent(self, category: Optional[str] = None, limit: int = 10) -> List[Dict]:
        """Get recent memories"""
        filtered = [m for m in self.memories if not category or m["category"] == category]
        filtered.sort(key=lambda x: x["timestamp"], reverse=True)
        return filtered[:limit]


class MemoryManager:
    """Unified memory management interface"""
    
    def __init__(self, storage_path: str = "data/memory.json"):
        self.conversation_memory = ConversationMemory()
        self.long_term_memory = LongTermMemory(storage_path)
    
    def remember(self, thread_id: str, content: str, category: str = "general", 
                 metadata: Optional[Dict] = None):
        """Store something in long-term memory"""
        self.long_term_memory.store(
            content=content,
            metadata=metadata or {"thread_id": thread_id},
            category=category
        )
    
    def recall(self, query: str, category: Optional[str] = None) -> List[Dict]:
        """Recall relevant memories"""
        return self.long_term_memory.search(query, category)
    
    def get_context(self, thread_id: str, query: Optional[str] = None) -> str:
        """
        Get relevant context for the agent
        Combines conversation history with relevant long-term memories
        """
        # Get conversation history
        conv_history = self.conversation_memory.get_conversation(thread_id)
        
        # Get relevant long-term memories if query provided
        relevant_memories = []
        if query:
            relevant_memories = self.long_term_memory.search(query, limit=3)
        
        # Format context
        context_parts = []
        
        if relevant_memories:
            context_parts.append("Relevant past information:")
            for mem in relevant_memories:
                context_parts.append(f"- {mem['content']}")
        
        if conv_history:
            recent_messages = conv_history[-5:]  # Last 5 messages
            context_parts.append("\nRecent conversation:")
            for msg in recent_messages:
                context_parts.append(f"{msg['role']}: {msg['content'][:100]}")
        
        return "\n".join(context_parts)


# Example usage
if __name__ == "__main__":
    memory = MemoryManager()
    
    # Store some memories
    memory.remember(
        thread_id="user_123",
        content="User prefers detailed explanations with code examples",
        category="preference"
    )
    
    memory.remember(
        thread_id="user_123",
        content="Researched LangGraph architecture and found it uses StateGraph for workflows",
        category="research"
    )
    
    # Recall memories
    results = memory.recall("LangGraph")
    print("Recalled memories:", json.dumps(results, indent=2))
    
    # Get context
    context = memory.get_context("user_123", "LangGraph")
    print("\nContext:", context)
