"""
Demo script showcasing the Smart Research & Productivity Assistant
Run this to see the agent in action without API keys (using mock responses)
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def demo_without_api():
    """Demonstration mode without requiring API keys"""
    print("=" * 70)
    print(" Smart Research & Productivity Assistant - DEMO MODE")
    print("=" * 70)
    print()
    
    scenarios = [
        {
            "title": "Scenario 1: Research Request",
            "user_input": "Search for recent developments in agentic AI systems",
            "agent_response": """I'll search for that information.

[Using web_search tool with query: "recent developments agentic AI"]

Based on the search results, here are the key recent developments:

**Key Developments:**
1. **Multi-Agent Systems**: Frameworks like AutoGEN and CrewAI enable multiple
   specialized agents to collaborate on complex tasks

2. **LangGraph & StateGraph**: New orchestration tools providing better control
   over agent workflows with state management and checkpointing

3. **Tool Use Improvements**: Enhanced function calling capabilities across
   major LLM providers (OpenAI, Anthropic, Google)

4. **Memory Systems**: Integration of vector databases for long-term context
   and retrieval-augmented generation (RAG)

Would you like me to create a task to review these developments in detail?"""
        },
        {
            "title": "Scenario 2: Task Creation",
            "user_input": "Yes, create a high-priority task to review these AI developments",
            "agent_response": """[Using create_task tool]

Task created successfully:
- Task ID: task_20250209_001
- Title: Review recent agentic AI developments
- Priority: High
- Status: Pending
- Description: Review multi-agent systems, LangGraph, tool use improvements,
  and memory systems

The task has been added to your task list. Use `/tasks` to view all tasks."""
        },
        {
            "title": "Scenario 3: Multi-Tool Usage",
            "user_input": "What are my current tasks and what should I prioritize?",
            "agent_response": """[Using list_tasks tool]

You currently have 3 tasks:

**High Priority:**
1. Review recent agentic AI developments (Status: Pending)
   - This is time-sensitive for staying current with the field

**Medium Priority:**
2. Prepare portfolio presentation (Status: In Progress)
   - Good progress, continue working on this

**Low Priority:**
3. Read LangChain documentation (Status: Pending)
   - Can be done after completing the AI developments review

**Recommendation:** Focus on the high-priority AI developments review first,
as it's marked as time-sensitive. The presentation is already in progress,
so you can alternate between these two tasks."""
        }
    ]
    
    for scenario in scenarios:
        print(f"\n📍 {scenario['title']}")
        print("-" * 70)
        print(f"\n👤 You: {scenario['user_input']}")
        print(f"\n🤖 Assistant:\n{scenario['agent_response']}")
        print("\n" + "=" * 70)
        input("\nPress Enter to continue to next scenario...")
    
    print("\n✅ Demo completed!")
    print("\nTo use the full agent with real API calls:")
    print("1. Set up your ANTHROPIC_API_KEY in .env")
    print("2. Run: python src/cli.py")
    print("\nFor production use, integrate real search APIs:")
    print("- Tavily (recommended for AI agents)")
    print("- SerpAPI (Google search results)")
    print("- Bing Search API")


def show_architecture():
    """Display the agent architecture"""
    print("\n" + "=" * 70)
    print(" AGENT ARCHITECTURE")
    print("=" * 70)
    print("""
    ┌─────────────────────────────────────────────┐
    │           User Input / CLI                   │
    └──────────────────┬──────────────────────────┘
                       │
                       ▼
    ┌─────────────────────────────────────────────┐
    │         LangGraph State Machine              │
    │                                              │
    │  ┌────────────────────────────────────┐     │
    │  │  1. Receive user input             │     │
    │  │  2. Analyze intent                 │     │
    │  │  3. Select appropriate tools       │     │
    │  │  4. Execute tools sequentially     │     │
    │  │  5. Synthesize response            │     │
    │  │  6. Update memory                  │     │
    │  └────────────────────────────────────┘     │
    └──────┬─────────────────────┬─────────────────┘
           │                     │
           ▼                     ▼
    ┌─────────────┐      ┌──────────────────┐
    │   Tools     │      │  Memory System   │
    │             │      │                  │
    │ • Search    │      │ • Conversation   │
    │ • Tasks     │      │ • Long-term      │
    │ • Summarize │      │ • Vector DB      │
    └─────────────┘      └──────────────────┘
    
    Key Features:
    • Stateful: Maintains conversation context
    • Multi-step: Can chain multiple tool calls
    • Adaptive: Chooses tools based on context
    • Memory: Remembers past interactions
    """)


def show_tool_details():
    """Display available tools and their capabilities"""
    print("\n" + "=" * 70)
    print(" AVAILABLE TOOLS")
    print("=" * 70)
    
    tools = [
        {
            "name": "web_search",
            "description": "Search the web for current information",
            "parameters": "query: str",
            "example": 'web_search("latest AI research papers")'
        },
        {
            "name": "create_task",
            "description": "Create a new task with priority and due date",
            "parameters": "title: str, description: str, priority: str, due_date: str",
            "example": 'create_task("Review papers", "Read 3 AI papers", "high", "2025-02-15")'
        },
        {
            "name": "list_tasks",
            "description": "List all tasks or filter by status",
            "parameters": "status: str = 'all'",
            "example": 'list_tasks("pending")'
        },
        {
            "name": "update_task",
            "description": "Update task status or priority",
            "parameters": "task_id: str, status: str, priority: str",
            "example": 'update_task("task_001", status="completed")'
        },
        {
            "name": "summarize_research",
            "description": "Create structured summary from research",
            "parameters": "topic: str, sources: list[str]",
            "example": 'summarize_research("AI agents", ["url1", "url2"])'
        }
    ]
    
    for tool in tools:
        print(f"\n📦 {tool['name']}")
        print(f"   {tool['description']}")
        print(f"   Parameters: {tool['parameters']}")
        print(f"   Example: {tool['example']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Demo the Smart Assistant")
    parser.add_argument("--architecture", action="store_true", help="Show architecture diagram")
    parser.add_argument("--tools", action="store_true", help="Show available tools")
    
    args = parser.parse_args()
    
    if args.architecture:
        show_architecture()
    elif args.tools:
        show_tool_details()
    else:
        demo_without_api()
