"""
Visualize Agent Decision Flow
Creates a flowchart showing how the agent processes requests
"""

def generate_mermaid_diagram():
    """Generate Mermaid flowchart of agent decision flow"""
    diagram = """
```mermaid
graph TD
    Start([User Input]) --> Parse[Parse Intent]
    Parse --> Context[Load Context & Memory]
    Context --> Analyze{Analyze Request Type}
    
    Analyze -->|Research Query| Research[Select web_search Tool]
    Analyze -->|Task Request| TaskOps[Select Task Tool]
    Analyze -->|General Question| Direct[Direct Response]
    
    Research --> Execute1[Execute Search]
    Execute1 --> Process1[Process Results]
    Process1 --> Summary[Generate Summary]
    Summary --> DecideNext{Need More Info?}
    
    TaskOps --> CreateTask[create_task]
    TaskOps --> ListTask[list_tasks]
    TaskOps --> UpdateTask[update_task]
    
    CreateTask --> Execute2[Execute Tool]
    ListTask --> Execute2
    UpdateTask --> Execute2
    Execute2 --> Process2[Process Results]
    Process2 --> DecideNext
    
    Direct --> Format[Format Response]
    
    DecideNext -->|Yes| Research
    DecideNext -->|No| Format
    
    Format --> Memory[Update Memory]
    Memory --> Response([Return to User])
    
    style Start fill:#e1f5ff
    style Response fill:#e1f5ff
    style Analyze fill:#fff4e1
    style DecideNext fill:#fff4e1
```
"""
    return diagram


def print_decision_tree():
    """Print ASCII decision tree"""
    tree = """
Agent Decision Flow
═══════════════════

User Input
    │
    ├─→ Parse Intent
    │      │
    │      ├─→ Is this a research query?
    │      │   YES → Use web_search tool
    │      │          │
    │      │          ├─→ Execute search
    │      │          ├─→ Analyze results
    │      │          ├─→ Need more info?
    │      │          │   YES → Search again
    │      │          │   NO  → Summarize
    │      │          └─→ Generate response
    │      │
    │      ├─→ Is this about tasks?
    │      │   YES → Select task operation
    │      │          │
    │      │          ├─→ Create? → create_task()
    │      │          ├─→ List?   → list_tasks()
    │      │          ├─→ Update? → update_task()
    │      │          └─→ Generate response
    │      │
    │      └─→ General question?
    │          YES → Use existing knowledge
    │                 └─→ Generate response
    │
    └─→ Update memory & return to user

Key Decision Points:
• Intent Classification (research vs tasks vs general)
• Tool Selection (which tool to use)
• Iteration Decision (need more information?)
• Response Formatting (how to present results)
"""
    return tree


def explain_tool_selection():
    """Explain how the agent selects tools"""
    explanation = """
Tool Selection Logic
════════════════════

The agent uses the LLM's reasoning to decide which tools to call.

Example 1: Research Query
─────────────────────────
User: "What are recent developments in AI?"

Agent thinks:
1. This requires current information ✓
2. I don't have real-time data ✓
3. I should use web_search ✓
4. Query: "recent AI developments 2025"

Tool selected: web_search(query="recent AI developments 2025")


Example 2: Task Creation
────────────────────────
User: "Remind me to review those AI papers tomorrow"

Agent thinks:
1. This is a task creation request ✓
2. Extract: title="Review AI papers", due="tomorrow" ✓
3. I should use create_task ✓

Tool selected: create_task(
    title="Review AI papers",
    description="Review papers on AI developments",
    priority="medium",
    due_date="2025-02-11"
)


Example 3: Multi-Tool Usage
───────────────────────────
User: "Search for Python tutorials and create a task to practice"

Agent thinks:
1. Two operations needed ✓
2. First: web_search for tutorials ✓
3. Then: create_task based on findings ✓

Tools selected (in sequence):
1. web_search(query="Python tutorials")
2. create_task(
       title="Practice Python",
       description="Based on tutorial findings...",
       priority="medium"
   )


Why This Approach Works:
────────────────────────
✓ Flexible: Can handle varied user requests
✓ Autonomous: Decides tool usage without hardcoded rules
✓ Contextual: Uses conversation history for decisions
✓ Extensible: Adding new tools doesn't require rewriting logic
"""
    return explanation


def show_state_transitions():
    """Show how agent state changes"""
    states = """
State Transitions Example
═════════════════════════

Initial State:
─────────────
{
    "messages": [],
    "research_context": "",
    "tasks": [],
    "next_action": ""
}

After User Input: "Search for LangGraph tutorials"
───────────────────────────────────────────────────
{
    "messages": [
        {"role": "user", "content": "Search for LangGraph tutorials"}
    ],
    "research_context": "",
    "tasks": [],
    "next_action": "web_search"
}

After Tool Execution:
────────────────────
{
    "messages": [
        {"role": "user", "content": "Search for LangGraph tutorials"},
        {"role": "assistant", "content": "I'll search for that..."},
        {"role": "tool", "tool_name": "web_search", "content": "Search results..."}
    ],
    "research_context": "Found tutorials on LangGraph basics, state management...",
    "tasks": [],
    "next_action": "summarize"
}

After Response Generation:
──────────────────────────
{
    "messages": [
        {"role": "user", "content": "Search for LangGraph tutorials"},
        {"role": "assistant", "content": "I'll search for that..."},
        {"role": "tool", "tool_name": "web_search", "content": "Search results..."},
        {"role": "assistant", "content": "I found several great tutorials..."}
    ],
    "research_context": "LangGraph tutorials cover...",
    "tasks": [],
    "next_action": "complete"
}

State preserved across conversation for context!
"""
    return states


if __name__ == "__main__":
    print("=" * 70)
    print(" AGENT VISUALIZATION")
    print("=" * 70)
    
    print("\n" + print_decision_tree())
    
    print("\n" + "=" * 70)
    print(explain_tool_selection())
    
    print("\n" + "=" * 70)
    print(show_state_transitions())
    
    print("\n" + "=" * 70)
    print("\nMermaid Diagram (paste into https://mermaid.live):")
    print(generate_mermaid_diagram())
    
    print("\n" + "=" * 70)
    print("\nFor more details, see:")
    print("• README.md - Overview and setup")
    print("• PORTFOLIO.md - Technical deep dive")
    print("• examples/ - Usage examples")
