import time
import json
import random

def run_agent(user_input: str, thread_id: str = "default"):
    """
    Simulated agent that returns mock responses based on keywords.
    """
    user_input_lower = user_input.lower()
    time.sleep(1.0) # Simulate thinking

    if "news" in user_input_lower or "search" in user_input_lower:
        return """I'll search for that information.

[Using web_search tool]

Based on the search results, here are some recent developments:

1. **AI Agents**: Multi-agent frameworks like LangGraph are gaining popularity.
2. **Models**: New models from Anthropic and Google are showing improved reasoning.
3. **Tools**: Better function calling capabilities are enabling more autonomous workflows.

Would you like me to create a task to track these topics?"""

    elif "task" in user_input_lower:
         return """[Using list_tasks tool]

You have the following tasks:

1. **Review AI News** (Priority: High, Status: Pending)
2. **Setup Environment** (Priority: Medium, Status: In Progress)

I can help you create a new task or update existing ones."""

    elif "help" in user_input_lower:
        return """I can help you with:

- **Research**: Search the web for information
- **Tasks**: Create and manage your to-do list
- **Summaries**: Summarize long documents or topics

Just ask me anything!"""

    else:
        return f"""I understand you said: "{user_input}"

I'm a demo agent running without an API key, so I have limited responses. 
Try asking me to "search for AI news" or "check my tasks" to see my capabilities!"""
