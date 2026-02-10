# 🤖 Smart Research & Productivity Assistant

An intelligent agentic AI system built with LangGraph that combines research capabilities with task management. This project demonstrates modern AI agent architecture with tool use, memory systems, and multi-step reasoning.

## 🌟 Features

### Research Capabilities
- **Web Search Integration**: Search for current information and synthesize findings
- **Research Summarization**: Automatically create structured summaries from multiple sources
- **Context-Aware Analysis**: Maintain research context across conversations

### Productivity Tools
- **Task Management**: Create, list, update, and track tasks
- **Priority System**: Organize tasks by priority and due dates
- **Status Tracking**: Monitor task progress (pending, in-progress, completed)

### Memory Systems
- **Short-term Memory**: Conversation history with context windowing
- **Long-term Memory**: Persistent storage of important information
- **Semantic Search**: Retrieve relevant past interactions (when using vector stores)

### Agent Architecture
- **LangGraph Orchestration**: State-based workflow management
- **Tool Use**: Dynamic tool selection and execution
- **Multi-step Reasoning**: Complex task decomposition and planning

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│                   (CLI / API / Web)                      │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────┐
│                  Agent Orchestrator                      │
│                   (LangGraph + LLM)                      │
│  ┌──────────────────────────────────────────────────┐   │
│  │  State Graph: Entry → Agent → Tools → Agent ...  │   │
│  └──────────────────────────────────────────────────┘   │
└───────┬──────────────────────┬─────────────────────┬────┘
        │                      │                     │
┌───────▼────────┐   ┌────────▼────────┐   ┌────────▼─────────┐
│     Tools      │   │  Memory System   │   │   LLM Provider   │
│  - Web Search  │   │  - Conversation  │   │   - Anthropic    │
│  - Task Mgmt   │   │  - Long-term     │   │   - OpenAI       │
│  - Summarizer  │   │  - Vector Store  │   │   - Local Models │
└────────────────┘   └──────────────────┘   └──────────────────┘
```

### Key Components

1. **Agent Core** (`src/agent.py`)
   - LangGraph-based state machine
   - Tool binding and orchestration
   - Conditional routing logic

2. **Memory System** (`src/memory.py`)
   - Conversation history management
   - Long-term memory persistence
   - Context retrieval and formatting

3. **CLI Interface** (`src/cli.py`)
   - Interactive command-line interface
   - Rich formatting and user experience
   - Command handling and display

## 🚀 Quick Start

### Prerequisites
- Python 3.9 or higher
- Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com/))

### Installation

1. **Clone or download this project**
   ```bash
   cd agentic-assistant
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   ```

### Running the Assistant

**Interactive CLI Mode:**
```bash
python src/cli.py
```

**Programmatic Usage:**
```python
from src.agent import run_agent

response = run_agent("Search for recent AI developments and create a task to review them")
print(response)
```

## 📖 Usage Examples

### Research Task
```
You: Search for recent developments in LangGraph and summarize the key features