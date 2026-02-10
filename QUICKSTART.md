# Quick Start Guide

Get your agentic AI running in 5 minutes!

## Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
python setup.py

# Follow the prompts - it will:
# ✓ Check Python version
# ✓ Create virtual environment
# ✓ Install all dependencies
# ✓ Set up configuration files
```

## Option 2: Manual Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment
cp .env.example .env
# Edit .env and add your ANTHROPIC_API_KEY
```

## Get Your API Key

1. Go to https://console.anthropic.com/
2. Sign up or log in
3. Navigate to API Keys
4. Create a new key
5. Copy it to your `.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-api03-...
   ```

## Run the Agent

### Interactive Mode (Recommended for First Time)

```bash
python src/cli.py
```

You'll see:
```
Smart Research & Productivity Assistant
I can help you with:
- 🔍 Research: Search the web and synthesize information
- ✅ Tasks: Create, list, and manage your tasks
- 🧠 Memory: Remember context across our conversations

You: _
```

### Try These Commands

```
You: Search for recent developments in AI agents

You: Create a high-priority task to review those developments

You: /tasks

You: /help
```

## Demo Mode (No API Key Required)

Want to see how it works without setting up an API key?

```bash
python demo.py
```

This runs through pre-scripted scenarios showing the agent's capabilities.

## Programmatic Usage

```python
from src.agent import run_agent

# Simple query
response = run_agent("What is LangGraph?")
print(response)

# Multi-turn with context
thread_id = "my_session"
run_agent("Search for Python tutorials", thread_id)
run_agent("Create a task to practice", thread_id)  # Remembers context!
```

## Project Structure

```
agentic-assistant/
├── src/
│   ├── agent.py      # 🧠 Core agent logic
│   ├── memory.py     # 💾 Memory system
│   └── cli.py        # 💬 Interactive interface
├── examples/         # 📚 Usage examples
├── tests/            # ✅ Test suite
├── docs/             # 📖 Documentation
├── demo.py           # 🎬 Demo script
└── setup.py          # ⚙️ Setup automation
```

## Common Issues

### "ANTHROPIC_API_KEY not set"
- Make sure you created `.env` file
- Verify your API key is correct
- Check there are no extra spaces

### "Module not found"
- Activate virtual environment first
- Run `pip install -r requirements.txt`

### "Connection error"
- Check your internet connection
- Verify API key is valid
- Try again (may be temporary API issue)

## Next Steps

1. **Explore Examples:**
   ```bash
   python examples/programmatic_usage.py
   ```

2. **Read the Docs:**
   - `README.md` - Full documentation
   - `PORTFOLIO.md` - Technical deep dive
   - `docs/agent_flow.py` - Architecture visualization

3. **Customize:**
   - Add your own tools in `src/agent.py`
   - Modify the system prompt
   - Integrate different LLM providers

4. **Deploy:**
   - Build a web interface
   - Create a Slack bot
   - Deploy as an API service

## Get Help

- **Issues?** Check `README.md` troubleshooting section
- **Questions?** See `examples/` for common patterns
- **Contributions?** Pull requests welcome!

---

**Ready to build something amazing? Let's go! 🚀**
