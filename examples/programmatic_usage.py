"""
Example: Programmatic usage of the agent
Shows how to integrate the agent into your own applications
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from agent import run_agent, create_agent_graph
from memory import MemoryManager


def example_simple_query():
    """Example 1: Simple one-off query"""
    print("Example 1: Simple Query")
    print("=" * 50)
    
    response = run_agent(
        "What are the key components of an AI agent?",
        thread_id="example_1"
    )
    print(f"Response: {response}\n")


def example_multi_turn_conversation():
    """Example 2: Multi-turn conversation with context"""
    print("\nExample 2: Multi-turn Conversation")
    print("=" * 50)
    
    thread_id = "example_2"
    
    # First turn
    response1 = run_agent(
        "Search for recent developments in LangGraph",
        thread_id=thread_id
    )
    print(f"Turn 1: {response1}\n")
    
    # Second turn (context from first turn)
    response2 = run_agent(
        "Create a task to review what you just found",
        thread_id=thread_id
    )
    print(f"Turn 2: {response2}\n")
    
    # Third turn
    response3 = run_agent(
        "What tasks do I have now?",
        thread_id=thread_id
    )
    print(f"Turn 3: {response3}\n")


def example_with_memory():
    """Example 3: Using memory system"""
    print("\nExample 3: Using Memory System")
    print("=" * 50)
    
    memory = MemoryManager()
    
    # Store some preferences
    memory.remember(
        thread_id="user_123",
        content="User prefers Python over JavaScript",
        category="preference"
    )
    
    memory.remember(
        thread_id="user_123",
        content="Working on building an AI agent portfolio project",
        category="context"
    )
    
    # Recall memories
    preferences = memory.recall("Python", category="preference")
    context = memory.recall("portfolio")
    
    print(f"Found {len(preferences)} preference(s)")
    print(f"Found {len(context)} context item(s)")
    
    # Use memory to inform agent
    context_str = memory.get_context("user_123", "portfolio project")
    print(f"\nContext for agent:\n{context_str}\n")


def example_error_handling():
    """Example 4: Error handling"""
    print("\nExample 4: Error Handling")
    print("=" * 50)
    
    try:
        # This will fail if no API key is set
        response = run_agent(
            "Search for AI trends",
            thread_id="example_4"
        )
        print(f"Success: {response}")
    except Exception as e:
        print(f"Error occurred: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print("\nTo fix: Set ANTHROPIC_API_KEY in your .env file")


def example_batch_processing():
    """Example 5: Processing multiple queries"""
    print("\nExample 5: Batch Processing")
    print("=" * 50)
    
    queries = [
        "Create a task to learn LangGraph basics",
        "Create a task to build a simple agent",
        "Create a task to deploy the agent"
    ]
    
    thread_id = "batch_example"
    
    for i, query in enumerate(queries, 1):
        print(f"\nProcessing query {i}/{len(queries)}: {query}")
        try:
            response = run_agent(query, thread_id=thread_id)
            print(f"✓ Completed: {response[:100]}...")
        except Exception as e:
            print(f"✗ Failed: {str(e)}")


def example_custom_workflow():
    """Example 6: Custom workflow orchestration"""
    print("\nExample 6: Custom Workflow")
    print("=" * 50)
    
    # Workflow: Research → Summarize → Create Tasks
    
    thread_id = "workflow_example"
    
    # Step 1: Research
    print("Step 1: Researching...")
    research_query = "Search for tutorials on building AI agents with LangGraph"
    research_response = run_agent(research_query, thread_id)
    print(f"✓ Research complete\n")
    
    # Step 2: Ask for summary
    print("Step 2: Requesting summary...")
    summary_query = "Summarize the key points from your search"
    summary_response = run_agent(summary_query, thread_id)
    print(f"✓ Summary generated\n")
    
    # Step 3: Create learning plan
    print("Step 3: Creating learning plan...")
    plan_query = "Based on this research, create 3 tasks for a learning plan"
    plan_response = run_agent(plan_query, thread_id)
    print(f"✓ Learning plan created\n")
    
    print("Workflow completed successfully!")


if __name__ == "__main__":
    import os
    
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("⚠️  WARNING: ANTHROPIC_API_KEY not set")
        print("Set it in your .env file to run examples with real API calls")
        print("Running demo mode...\n")
    
    # Run examples
    # Uncomment the ones you want to test
    
    # example_simple_query()
    # example_multi_turn_conversation()
    example_with_memory()
    # example_error_handling()
    # example_batch_processing()
    # example_custom_workflow()
    
    print("\n" + "=" * 50)
    print("Examples completed!")
    print("\nTo run with real API:")
    print("1. Set ANTHROPIC_API_KEY in .env")
    print("2. Uncomment desired examples above")
    print("3. Run: python examples/programmatic_usage.py")
