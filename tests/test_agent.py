"""
Test suite for the Smart Research & Productivity Assistant
Demonstrates testing strategies for agentic AI systems
"""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent import (
    AgentState,
    web_search,
    create_task,
    list_tasks,
    update_task,
    summarize_research,
    should_continue
)
from memory import ConversationMemory, LongTermMemory, MemoryManager


class TestTools:
    """Test individual tool functions"""
    
    def test_web_search_returns_string(self):
        """Test that web_search returns a string response"""
        result = web_search.invoke({"query": "test query"})
        assert isinstance(result, str)
        assert "test query" in result.lower()
    
    def test_create_task_valid_input(self):
        """Test task creation with valid inputs"""
        result = create_task.invoke({
            "title": "Test Task",
            "description": "Test Description",
            "priority": "high"
        })
        
        # Parse JSON response
        import json
        result_dict = json.loads(result)
        
        assert result_dict["status"] == "success"
        assert "task_" in result_dict["task_id"]
        assert "Test Task" in result_dict["message"]
    
    def test_create_task_with_due_date(self):
        """Test task creation with optional due date"""
        result = create_task.invoke({
            "title": "Deadline Task",
            "description": "Has a deadline",
            "priority": "medium",
            "due_date": "2025-12-31"
        })
        
        assert "success" in result
    
    def test_list_tasks_returns_json(self):
        """Test that list_tasks returns valid JSON"""
        result = list_tasks.invoke({"status": "all"})
        
        import json
        tasks = json.loads(result)
        
        assert isinstance(tasks, list)
        if len(tasks) > 0:
            assert "id" in tasks[0]
            assert "title" in tasks[0]
    
    def test_update_task_status(self):
        """Test updating task status"""
        result = update_task.invoke({
            "task_id": "task_001",
            "status": "completed"
        })
        
        import json
        result_dict = json.loads(result)
        
        assert result_dict["status"] == "success"
        assert "task_001" in result_dict["message"]
    
    def test_summarize_research(self):
        """Test research summarization"""
        result = summarize_research.invoke({
            "topic": "AI Agents",
            "sources": ["url1", "url2", "url3"]
        })
        
        assert isinstance(result, str)
        assert "AI Agents" in result
        assert "3" in result  # Number of sources


class TestMemorySystem:
    """Test memory management"""
    
    def setup_method(self):
        """Set up test fixtures"""
        self.conv_memory = ConversationMemory(max_messages=5)
        # Use temporary path for testing
        import tempfile
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".json")
        self.long_memory = LongTermMemory(self.temp_file.name)
    
    def teardown_method(self):
        """Clean up test files"""
        import os
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)
    
    def test_conversation_memory_add_message(self):
        """Test adding messages to conversation memory"""
        self.conv_memory.add_message("thread_1", "user", "Hello")
        self.conv_memory.add_message("thread_1", "assistant", "Hi there!")
        
        conversation = self.conv_memory.get_conversation("thread_1")
        
        assert len(conversation) == 2
        assert conversation[0]["role"] == "user"
        assert conversation[0]["content"] == "Hello"
        assert conversation[1]["role"] == "assistant"
    
    def test_conversation_memory_max_messages(self):
        """Test that conversation memory respects max_messages limit"""
        for i in range(10):
            self.conv_memory.add_message("thread_1", "user", f"Message {i}")
        
        conversation = self.conv_memory.get_conversation("thread_1")
        
        assert len(conversation) == 5  # max_messages
        assert conversation[0]["content"] == "Message 5"  # Oldest kept
        assert conversation[-1]["content"] == "Message 9"  # Most recent
    
    def test_long_term_memory_store_and_search(self):
        """Test storing and searching long-term memories"""
        self.long_memory.store(
            content="LangGraph uses StateGraph for workflows",
            metadata={"source": "documentation"},
            category="research"
        )
        
        results = self.long_memory.search("LangGraph")
        
        assert len(results) > 0
        assert "LangGraph" in results[0]["content"]
        assert results[0]["category"] == "research"
    
    def test_long_term_memory_category_filter(self):
        """Test filtering memories by category"""
        self.long_memory.store("Research fact", {}, "research")
        self.long_memory.store("User preference", {}, "preference")
        
        research_results = self.long_memory.search("fact", category="research")
        
        assert len(research_results) > 0
        assert all(m["category"] == "research" for m in research_results)
    
    def test_memory_manager_integration(self):
        """Test MemoryManager combining both memory types"""
        manager = MemoryManager(self.temp_file.name)
        
        # Add conversation
        manager.conversation_memory.add_message("test", "user", "Remember this")
        
        # Add long-term memory
        manager.remember("test", "Important information", "note")
        
        # Get context
        context = manager.get_context("test", "important")
        
        assert "Important information" in context or "Remember this" in context


class TestAgentFlow:
    """Test agent decision-making and flow"""
    
    def test_should_continue_with_tool_calls(self):
        """Test that should_continue returns 'tools' when there are tool calls"""
        mock_message = Mock()
        mock_message.tool_calls = [{"name": "web_search", "args": {}}]
        
        state = {
            "messages": [mock_message],
            "research_context": "",
            "tasks": [],
            "next_action": ""
        }
        
        result = should_continue(state)
        assert result == "tools"
    
    def test_should_continue_without_tool_calls(self):
        """Test that should_continue returns 'end' when no tool calls"""
        mock_message = Mock()
        mock_message.tool_calls = []
        
        state = {
            "messages": [mock_message],
            "research_context": "",
            "tasks": [],
            "next_action": ""
        }
        
        result = should_continue(state)
        assert result == "end"


class TestIntegration:
    """Integration tests for full workflows"""
    
    @pytest.mark.skipif(
        "ANTHROPIC_API_KEY" not in __import__("os").environ,
        reason="Requires ANTHROPIC_API_KEY"
    )
    def test_full_research_workflow(self):
        """Test complete research workflow (requires API key)"""
        from agent import run_agent
        
        response = run_agent(
            "Search for information about LangGraph",
            thread_id="test_research"
        )
        
        assert isinstance(response, str)
        assert len(response) > 0
    
    @pytest.mark.skipif(
        "ANTHROPIC_API_KEY" not in __import__("os").environ,
        reason="Requires ANTHROPIC_API_KEY"
    )
    def test_task_creation_workflow(self):
        """Test task creation workflow (requires API key)"""
        from agent import run_agent
        
        response = run_agent(
            "Create a high-priority task to review AI papers",
            thread_id="test_tasks"
        )
        
        assert isinstance(response, str)
        # Should mention task creation
        assert any(word in response.lower() for word in ["task", "created", "success"])


# Mock tests that don't require API key
class TestMockedAgent:
    """Test agent with mocked LLM responses"""
    
    @patch('agent.ChatAnthropic')
    def test_agent_with_mock_llm(self, mock_claude):
        """Test agent with mocked LLM"""
        # Mock the LLM response
        mock_response = Mock()
        mock_response.content = "I'll help you with that!"
        mock_response.tool_calls = []
        
        mock_model = Mock()
        mock_model.invoke.return_value = mock_response
        mock_claude.return_value.bind_tools.return_value = mock_model
        
        from agent import call_model
        
        state = {
            "messages": [{"role": "user", "content": "Hello"}],
            "research_context": "",
            "tasks": [],
            "next_action": ""
        }
        
        result = call_model(state)
        
        assert "messages" in result
        assert len(result["messages"]) > 0


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "--tb=short"])
