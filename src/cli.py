"""
Interactive CLI Interface for the Smart Assistant
Provides a user-friendly command-line interface with rich formatting
"""

import sys
from datetime import datetime
from typing import Optional
import json

try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.markdown import Markdown
    from rich.prompt import Prompt
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better formatting: pip install rich")

from agent import run_agent, create_agent_graph
from memory import MemoryManager


class AssistantCLI:
    """Interactive CLI for the assistant"""
    
    def __init__(self):
        self.console = Console() if RICH_AVAILABLE else None
        self.memory = MemoryManager()
        self.thread_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.running = True
    
    def print(self, text: str, style: Optional[str] = None):
        """Print with or without rich formatting"""
        if self.console:
            self.console.print(text, style=style)
        else:
            print(text)
    
    def print_panel(self, text: str, title: str = "Assistant"):
        """Print a panel"""
        if self.console:
            self.console.print(Panel(text, title=title, border_style="blue"))
        else:
            print(f"\n=== {title} ===")
            print(text)
            print("=" * (len(title) + 8))
    
    def print_welcome(self):
        """Print welcome message"""
        welcome = """
# Smart Research & Productivity Assistant

I can help you with:
- 🔍 Research: Search the web and synthesize information
- ✅ Tasks: Create, list, and manage your tasks
- 🧠 Memory: Remember context across our conversations

**Commands:**
- Type your request naturally
- `/tasks` - List all tasks
- `/memory` - View recent memories
- `/clear` - Clear conversation
- `/help` - Show this help
- `/quit` - Exit

Let's get started! What would you like help with?
        """
        
        if self.console:
            self.console.print(Markdown(welcome))
        else:
            print(welcome)
    
    def handle_command(self, user_input: str) -> bool:
        """
        Handle special commands
        
        Returns:
            True if command was handled, False otherwise
        """
        if user_input == "/quit":
            self.print("\n👋 Goodbye!", style="bold green")
            self.running = False
            return True
        
        elif user_input == "/help":
            self.print_welcome()
            return True
        
        elif user_input == "/clear":
            self.memory.conversation_memory.clear_conversation(self.thread_id)
            self.print("\n✨ Conversation cleared!", style="bold green")
            return True
        
        elif user_input == "/tasks":
            self.show_tasks()
            return True
        
        elif user_input == "/memory":
            self.show_memory()
            return True
        
        return False
    
    def show_tasks(self):
        """Display tasks in a formatted table"""
        # In production, fetch from database
        tasks = [
            {"id": "001", "title": "Review LangGraph docs", "priority": "high", "status": "pending"},
            {"id": "002", "title": "Build demo app", "priority": "medium", "status": "in_progress"}
        ]
        
        if self.console:
            table = Table(title="Your Tasks")
            table.add_column("ID", style="cyan")
            table.add_column("Title", style="white")
            table.add_column("Priority", style="yellow")
            table.add_column("Status", style="green")
            
            for task in tasks:
                table.add_row(
                    task["id"],
                    task["title"],
                    task["priority"],
                    task["status"]
                )
            
            self.console.print(table)
        else:
            print("\n=== Your Tasks ===")
            for task in tasks:
                print(f"{task['id']}: {task['title']} [{task['priority']}] - {task['status']}")
    
    def show_memory(self):
        """Display recent memories"""
        memories = self.memory.long_term_memory.get_recent(limit=5)
        
        if not memories:
            self.print("\nNo memories stored yet.", style="italic")
            return
        
        self.print("\n📚 Recent Memories:", style="bold")
        for mem in memories:
            self.print(f"\n[{mem['category']}] {mem['content'][:100]}...")
    
    def run(self):
        """Main interaction loop"""
        self.print_welcome()
        
        while self.running:
            try:
                # Get user input
                if self.console:
                    user_input = Prompt.ask("\n[bold cyan]You[/bold cyan]")
                else:
                    user_input = input("\nYou: ").strip()
                
                if not user_input:
                    continue
                
                # Handle commands
                if user_input.startswith("/"):
                    if self.handle_command(user_input):
                        continue
                
                # Store in conversation memory
                self.memory.conversation_memory.add_message(
                    self.thread_id, "user", user_input
                )
                
                # Process with agent
                self.print("\n[italic]Thinking...[/italic]", style="dim")
                
                try:
                    response = run_agent(user_input, self.thread_id)
                    
                    # Store response in conversation memory
                    self.memory.conversation_memory.add_message(
                        self.thread_id, "assistant", response
                    )
                    
                    # Display response
                    self.print_panel(response, "Assistant")
                    
                    # Store important information in long-term memory
                    if any(keyword in user_input.lower() for keyword in ["remember", "important", "note"]):
                        self.memory.remember(
                            thread_id=self.thread_id,
                            content=user_input,
                            category="user_note"
                        )
                
                except Exception as e:
                    self.print(f"\n❌ Error: {str(e)}", style="bold red")
                    self.print("This might be due to missing API keys. See README for setup.", style="italic")
            
            except KeyboardInterrupt:
                self.print("\n\n👋 Goodbye!", style="bold green")
                break
            except Exception as e:
                self.print(f"\n❌ Unexpected error: {str(e)}", style="bold red")


def main():
    """Entry point for the CLI"""
    cli = AssistantCLI()
    cli.run()


if __name__ == "__main__":
    main()
