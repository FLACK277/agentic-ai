"""
Interactive CLI Interface - FREE VERSION
Uses Ollama (no API keys needed!)
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
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Note: Install 'rich' for better formatting: pip install rich")

from agent_free import run_agent, create_agent_graph
from memory import MemoryManager


class AssistantCLI:
    """Interactive CLI for the assistant - FREE VERSION"""
    
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
## 🎉 FREE VERSION - Powered by Ollama

I can help you with:
- 🔍 Research: Search and synthesize information
- ✅ Tasks: Create, list, and manage your tasks
- 🧠 Memory: Remember context across conversations

**This version is 100% FREE:**
- ✅ No API keys required
- ✅ Runs completely on your computer
- ✅ Unlimited usage
- ✅ Works offline (after initial setup)

**Commands:**
- Type your request naturally
- `/tasks` - List all tasks
- `/memory` - View recent memories
- `/clear` - Clear conversation
- `/help` - Show this help
- `/quit` - Exit

**Powered by:** Ollama + Llama 3.2 (running locally)

Let's get started! What would you like help with?
        """
        
        if self.console:
            self.console.print(Markdown(welcome))
        else:
            print(welcome)
    
    def handle_command(self, user_input: str) -> bool:
        """Handle special commands"""
        if user_input == "/quit":
            self.print("\n👋 Goodbye! Thanks for using the FREE assistant!", style="bold green")
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
        """Display tasks"""
        tasks = [
            {"id": "001", "title": "Set up Ollama", "priority": "high", "status": "completed"},
            {"id": "002", "title": "Build AI portfolio project", "priority": "high", "status": "in_progress"}
        ]
        
        self.print("\n📋 Your Tasks:", style="bold")
        for task in tasks:
            status_emoji = "✅" if task["status"] == "completed" else "🔄"
            self.print(f"  {status_emoji} [{task['priority']}] {task['title']}")
    
    def show_memory(self):
        """Display recent memories"""
        memories = self.memory.long_term_memory.get_recent(limit=5)
        
        if not memories:
            self.print("\nNo memories stored yet.", style="italic")
            return
        
        self.print("\n📚 Recent Memories:", style="bold")
        for mem in memories:
            self.print(f"  • [{mem['category']}] {mem['content'][:80]}...")
    
    def check_ollama(self):
        """Check if Ollama is available"""
        try:
            from langchain_community.llms import Ollama
            test_model = Ollama(model="llama3.2", temperature=0)
            test_model.invoke("Hi", max_tokens=5)
            return True
        except Exception as e:
            self.print("\n❌ Ollama is not running or not installed!", style="bold red")
            self.print("\nTo get started:", style="bold yellow")
            self.print("1. Install Ollama from: https://ollama.ai/")
            self.print("2. Run: ollama pull llama3.2")
            self.print("3. Make sure Ollama is running")
            self.print("\nSee FREE_SETUP.md for detailed instructions")
            return False
    
    def run(self):
        """Main interaction loop"""
        # Check Ollama first
        if not self.check_ollama():
            return
        
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
                    
                    # Store response
                    self.memory.conversation_memory.add_message(
                        self.thread_id, "assistant", response
                    )
                    
                    # Display response
                    self.print_panel(response, "Assistant (FREE)")
                    
                    # Store important info
                    if any(kw in user_input.lower() for kw in ["remember", "important", "note"]):
                        self.memory.remember(
                            thread_id=self.thread_id,
                            content=user_input,
                            category="user_note"
                        )
                
                except Exception as e:
                    self.print(f"\n❌ Error: {str(e)}", style="bold red")
                    self.print("\nMake sure Ollama is running:", style="italic")
                    self.print("  Run: ollama serve")
            
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
