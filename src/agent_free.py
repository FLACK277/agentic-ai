"""
Smart Research & Productivity Assistant - FREE VERSION
Uses Ollama (local LLM) - completely free, no API keys needed!
"""

from typing import TypedDict, Annotated, Sequence, Literal
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
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


# Tools for the agent (same as before)
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
    # Simulated search results for demo
    return f"""Search results for "{query}":
    
    [Simulated Results - In production, integrate with Tavily or SerpAPI]
    1. Recent developments in {query} include new frameworks and tools...
    2. Key researchers are focusing on multi-agent systems and reasoning...
    3. Industry applications show 40% improvement in task completion...
    
    Note: This is a simulation. For real search, integrate a search API.
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
    sample_tasks = [
        {
            "id": "task_001",
            "title": "Review AI agent frameworks",
            "status": "pending",
            "priority": "high"
        },
        {
            "id": "task_002",
            "title": "Build portfolio project",
            "status": "in_progress",
            "priority": "high"
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
    - Modern approaches focus on autonomous decision-making
    - Tool use and function calling are essential components
    - Memory systems enable context retention across sessions
    
    Sources Consulted: {len(sources)}
    
    Recommendations:
    - Explore LangGraph for state-based workflows
    - Implement vector databases for semantic search
    - Use local models for cost-effective development
    """


# Define the tools list
tools = [web_search, create_task, list_tasks, update_task, summarize_research]


# Node functions for the graph
def should_continue(state: AgentState) -> Literal["tools", "end"]:
    """Determine if we should continue or end"""
    messages = state["messages"]
    last_message = messages[-1]
    
    if not hasattr(last_message, "tool_calls") or not last_message.tool_calls:
        return "end"
    return "tools"


def call_model(state: AgentState):
    """Call the LLM with the current state"""
    messages = state["messages"]
    
    # Import here to make it optional
    try:
        from langchain_community.llms import Ollama
        
        # Initialize Ollama model (FREE - runs locally!)
        # Default model: llama3.2 (lightweight and fast)
        # Other options: llama3.2, mistral, phi, gemma
        model = Ollama(
            model="llama3.2",
            temperature=0
        )
        
        # Note: Ollama doesn't support tool calling natively like Claude/GPT
        # So we use a simpler approach with structured prompts
        
    except ImportError:
        print("ERROR: Ollama not installed!")
        print("Install with: pip install langchain-community")
        print("Then install Ollama from: https://ollama.ai/")
        raise
    
    # System context
    system_context = f"""You are a helpful research and productivity assistant.

Current Research Context: {state.get('research_context', 'None')}
Active Tasks: {len(state.get('tasks', []))}

Available tools:
1. web_search(query) - Search for information
2. create_task(title, description, priority) - Create a new task
3. list_tasks(status) - List all tasks
4. update_task(task_id, status, priority) - Update a task
5. summarize_research(topic, sources) - Summarize research

When the user asks for something that requires a tool, respond with:
TOOL: tool_name
ARGS: {{"arg1": "value1", "arg2": "value2"}}

Otherwise, respond naturally to help the user.
"""
    
    # Format messages for Ollama
    prompt = system_context + "\n\n"
    for msg in messages:
        if isinstance(msg, HumanMessage):
            prompt += f"User: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            prompt += f"Assistant: {msg.content}\n"
    
    prompt += "Assistant: "
    
    # Get response
    response_text = model.invoke(prompt)
    
    # Parse if it's a tool call
    tool_calls = []
    if "TOOL:" in response_text and "ARGS:" in response_text:
        # Extract tool call (simple parsing)
        lines = response_text.split('\n')
        tool_name = None
        args = {}
        
        for line in lines:
            if line.startswith("TOOL:"):
                tool_name = line.replace("TOOL:", "").strip()
            elif line.startswith("ARGS:"):
                args_str = line.replace("ARGS:", "").strip()
                try:
                    args = json.loads(args_str)
                except:
                    pass
        
        if tool_name:
            tool_calls = [{
                "name": tool_name,
                "args": args,
                "id": "call_1"
            }]
            response_text = f"I'll use the {tool_name} tool to help with that."
    
    # Create response message
    response = AIMessage(content=response_text)
    if tool_calls:
        response.tool_calls = tool_calls
    
    return {"messages": [response]}


# Build the graph
def create_agent_graph():
    """Create the LangGraph agent"""
    workflow = StateGraph(AgentState)
    
    workflow.add_node("agent", call_model)
    workflow.add_node("tools", ToolNode(tools))
    
    workflow.set_entry_point("agent")
    
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    
    workflow.add_edge("tools", "agent")
    
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
    
    initial_state = {
        "messages": [HumanMessage(content=user_input)],
        "research_context": "",
        "tasks": [],
        "next_action": ""
    }
    
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
    print("Smart Research & Productivity Assistant - FREE VERSION")
    print("Using Ollama (local LLM)")
    print("=" * 60)
    
    # Check if Ollama is available
    try:
        from langchain_community.llms import Ollama
        test = Ollama(model="llama3.2")
        test.invoke("Hi")
        print("✓ Ollama is running!")
    except Exception as e:
        print(f"✗ Ollama not available: {e}")
        print("\nTo install Ollama:")
        print("1. Visit: https://ollama.ai/")
        print("2. Download and install")
        print("3. Run: ollama pull llama3.2")
        print("4. Then run this script again")
        exit(1)
    
    # Test conversation
    response = run_agent("What can you help me with?")
    print(f"\nAssistant: {response}")
