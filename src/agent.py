"""
Smart Research & Productivity Assistant
A LangGraph-based agentic AI that combines research capabilities with task management
"""

from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langchain_anthropic import ChatAnthropic
from langchain_core.tools import tool
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from langgraph.checkpoint.memory import MemorySaver
import operator
import json
from datetime import datetime


# Define the agent state
class AgentState(TypedDict):
    """The state of our agent"""
    messages: Annotated[Sequence[BaseMessage], operator.add]
    research_context: str
    tasks: list[dict]
    next_action: str


# Tools for the agent
@tool
def web_search(query: str) -> str:
    """
    Search the web for information. Use this when you need current information
    or facts that you don't already know.
    
    Args:
        query: The search query
    
    Returns:
        Search results as a string
    """
    # In production, integrate with Tavily, SerpAPI, or similar
    # For demo purposes, we'll simulate a search
    return f"""Search results for "{query}":
    
    [Simulated Results]
    1. Recent developments in {query}...
    2. Key facts about {query}...
    3. Expert analysis on {query}...
    
    Note: In production, this would connect to a real search API like Tavily or SerpAPI.
    """


@tool
def create_task(title: str, description: str, priority: str = "medium", due_date: str = None) -> str:
    """
    Create a new task in the task management system.
    
    Args:
        title: The task title
        description: Detailed description of the task
        priority: Priority level (low, medium, high)
        due_date: Due date in YYYY-MM-DD format (optional)
    
    Returns:
        Confirmation message with task ID
    """
    task_id = f"task_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    task = {
        "id": task_id,
        "title": title,
        "description": description,
        "priority": priority,
        "due_date": due_date,
        "status": "pending",
        "created_at": datetime.now().isoformat()
    }
    
    # In production, save to database
    return json.dumps({
        "status": "success",
        "task_id": task_id,
        "message": f"Task '{title}' created successfully with priority {priority}"
    }, indent=2)


@tool
def list_tasks(status: str = "all") -> str:
    """
    List all tasks, optionally filtered by status.
    
    Args:
        status: Filter by status (all, pending, completed, in_progress)
    
    Returns:
        List of tasks as JSON
    """
    # In production, fetch from database
    sample_tasks = [
        {
            "id": "task_001",
            "title": "Review research paper on LLM agents",
            "status": "pending",
            "priority": "high"
        },
        {
            "id": "task_002",
            "title": "Prepare presentation slides",
            "status": "in_progress",
            "priority": "medium"
        }
    ]
    
    return json.dumps(sample_tasks, indent=2)


@tool
def update_task(task_id: str, status: str = None, priority: str = None) -> str:
    """
    Update an existing task's status or priority.
    
    Args:
        task_id: The ID of the task to update
        status: New status (pending, in_progress, completed)
        priority: New priority (low, medium, high)
    
    Returns:
        Confirmation message
    """
    updates = []
    if status:
        updates.append(f"status to '{status}'")
    if priority:
        updates.append(f"priority to '{priority}'")
    
    return json.dumps({
        "status": "success",
        "message": f"Updated task {task_id}: {', '.join(updates)}"
    }, indent=2)


@tool
def summarize_research(topic: str, sources: list[str]) -> str:
    """
    Create a structured summary of research on a topic.
    
    Args:
        topic: The research topic
        sources: List of source URLs or descriptions
    
    Returns:
        Structured research summary
    """
    return f"""Research Summary: {topic}
    
    Key Findings:
    - [Analysis of gathered information]
    - [Important insights]
    - [Conclusions]
    
    Sources Consulted: {len(sources)}
    
    Note: This is a template. In production, this would analyze actual search results.
    """


# Define the tools list
tools = [web_search, create_task, list_tasks, update_task, summarize_research]


# Node functions for the graph
def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Determine if we should continue or end"""
    messages = state["messages"]
    last_message = messages[-1]
    
    # If there are no tool calls, we're done
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return "end"
    return "tools"


def call_model(state: AgentState):
    """Call the LLM with the current state"""
    messages = state["messages"]
    
    # Initialize the model with tools
    model = ChatAnthropic(
        model="claude-sonnet-4-20250514",
        temperature=0
    ).bind_tools(tools)
    
    # Add system message with context
    system_context = f"""You are a smart research and productivity assistant. 

Current Research Context: {state.get('research_context', 'None')}
Active Tasks: {len(state.get('tasks', []))}

Your capabilities:
1. Research: Search the web, analyze information, create summaries
2. Productivity: Create, list, and update tasks
3. Memory: Remember context across the conversation

Always think step-by-step:
- Understand what the user needs
- Determine which tools to use
- Execute actions in logical order
- Provide clear, concise responses

Be proactive in suggesting tasks or research based on user needs."""
    
    response = model.invoke([
        {"role": "system", "content": system_context}
    ] + messages)
    
    return {"messages": [response]}


# Build the graph
def create_agent_graph():
    """Create the LangGraph agent"""
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    
    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Compile with memory
    memory = MemorySaver()
    app = workflow.compile(checkpointer=memory)
    
    return app


def run_agent(user_input: str, thread_id: str = "default"):
    """
    Run the agent with a user input
    
    Args:
        user_input: The user's message
        thread_id: Thread ID for conversation memory
    
    Returns:
        The agent's response
    """
    app = create_agent_graph()
    
    # Initial state
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "research_context": "",
        "tasks": [],
        "next_action": ""
    }
    
    # Run the agent
    config = {"configurable": {"thread_id": thread_id}}
    
    final_state = None
    for chunk in app.stream(initial_state, config):
        if "agent" in chunk:
            final_state = chunk["agent"]
    
    if final_state and "messages" in final_state:
        last_message = final_state["messages"][-1]
        if isinstance(last_message, AIMessage):
            return last_message.content
    
    return "No response generated"


if __name__ == "__main__":
    # Example usage
    print("Smart Research & Productivity Assistant")
    print("=" * 50)
    
    # Test conversation
    response1 = run_agent("Search for recent developments in LangGraph and create a task to review them")
    print(f"\nAssistant: {response1}")
    
    response2 = run_agent("What tasks do I have?")
    print(f"\nAssistant: {response2}")
