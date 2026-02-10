# 🎉 100% FREE Setup Guide - No API Keys Required!

This version uses **Ollama** - a completely free, local AI that runs on your computer. Perfect for portfolio projects!

## ✅ What You Get (100% FREE)

- ✅ **No API keys** needed
- ✅ **No credit card** required
- ✅ **No usage limits** or costs
- ✅ **Works offline** after initial download
- ✅ **Privacy**: All data stays on your computer
- ✅ **Unlimited usage** for your portfolio

## 🚀 Quick Start (3 Steps)

### Step 1: Install Ollama

**Windows:**
1. Go to: https://ollama.ai/
2. Click "Download for Windows"
3. Run the installer
4. That's it!

**Mac:**
1. Go to: https://ollama.ai/
2. Click "Download for Mac"
3. Drag to Applications folder
4. Open Ollama

**Linux:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
```

### Step 2: Download a Model

Open your terminal and run:

```bash
# Download Llama 3.2 (recommended - lightweight and fast)
ollama pull llama3.2
```

**Other options:**
```bash
ollama pull mistral        # Mistral 7B - good for reasoning
ollama pull phi            # Microsoft Phi - super lightweight
ollama pull gemma          # Google Gemma - balanced performance
```

**Note:** First download takes 2-5 minutes (downloads the AI model to your computer)

### Step 3: Install Python Dependencies

```bash
cd agentic-assistant

# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # Mac/Linux
# OR
venv\Scripts\activate     # Windows

# Install dependencies (FREE VERSION)
pip install -r requirements-free.txt
```

## 🎯 Run Your Agent

### Interactive Mode:

```bash
python src/cli_free.py
```

### Test It Works:

```bash
python src/agent_free.py
```

You should see:
```
✓ Ollama is running!
Assistant: I can help you with research and task management...
```

## 💡 How Ollama Works

```
┌─────────────────────────────────┐
│   Your Computer                 │
│                                 │
│  ┌──────────────────────────┐  │
│  │  Ollama Server           │  │
│  │  (Runs in background)    │  │
│  │                          │  │
│  │  Models:                 │  │
│  │  • llama3.2 (4GB)        │  │
│  │  • mistral (4GB)         │  │
│  │  • phi (2GB)             │  │
│  └──────────────────────────┘  │
│           ↑                     │
│           │ (Free, Local API)   │
│           ↓                     │
│  ┌──────────────────────────┐  │
│  │  Your Agent Project      │  │
│  │  (Python Code)           │  │
│  └──────────────────────────┘  │
│                                 │
└─────────────────────────────────┘

No internet needed after download!
All processing happens on your computer!
```

## 📊 Model Comparison

| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| **llama3.2** | 2GB | ⚡⚡⚡ | ⭐⭐⭐ | **Recommended** - Balanced |
| mistral | 4GB | ⚡⚡ | ⭐⭐⭐⭐ | Complex reasoning |
| phi | 1.5GB | ⚡⚡⚡⚡ | ⭐⭐ | Lightweight, fast |
| gemma | 3GB | ⚡⚡⚡ | ⭐⭐⭐ | Good all-rounder |

**Recommendation**: Start with **llama3.2** - it's fast, small, and good quality!

## 🔧 Configuration

### Change Models

Edit `src/agent_free.py`, line ~135:

```python
model = Ollama(
    model="llama3.2",  # Change to: mistral, phi, gemma, etc.
    temperature=0
)
```

### Adjust Temperature

```python
model = Ollama(
    model="llama3.2",
    temperature=0.7  # Higher = more creative, Lower = more focused
)
```

## 🆚 Ollama vs Cloud APIs

### Ollama (FREE) ✅
- ✅ 100% free forever
- ✅ No API keys
- ✅ Works offline
- ✅ Private (data stays local)
- ✅ No usage limits
- ❌ Requires decent computer
- ❌ Slightly slower than cloud

### Cloud APIs (Anthropic, OpenAI) 💳
- ✅ Very powerful models
- ✅ No local compute needed
- ✅ Faster responses
- ❌ Costs money (after free credits)
- ❌ Requires internet
- ❌ Data sent to cloud
- ❌ Usage limits

**For a portfolio project?** → **Ollama is perfect!** ✅

## 💻 System Requirements

### Minimum:
- **RAM**: 8GB
- **Storage**: 5GB free
- **OS**: Windows 10+, macOS 11+, Linux
- **CPU**: Any modern processor

### Recommended:
- **RAM**: 16GB
- **Storage**: 10GB free
- **GPU**: Not required (but helps with speed)

**Don't have these specs?**
- Use `phi` model (only 1.5GB, runs on 4GB RAM)
- Or use the demo mode (no AI needed)

## 🚨 Troubleshooting

### "Ollama not found" Error

**Check if Ollama is running:**
```bash
ollama list
```

Should show your downloaded models.

**If not running:**
- **Windows**: Search for "Ollama" in Start menu and click it
- **Mac**: Click the Ollama icon in menu bar
- **Linux**: Run `ollama serve` in terminal

### "Model not found" Error

Download the model:
```bash
ollama pull llama3.2
```

### "Connection refused" Error

Restart Ollama:
```bash
# Stop
killall ollama  # Mac/Linux
# OR Task Manager > End Ollama  # Windows

# Start again
ollama serve
```

### Slow Responses

1. **Try a smaller model**:
   ```bash
   ollama pull phi
   ```
   Change model in code to "phi"

2. **Close other applications** to free up RAM

3. **Lower temperature** for faster responses

## 🎓 Ollama Commands Cheat Sheet

```bash
# List downloaded models
ollama list

# Download a model
ollama pull llama3.2

# Remove a model
ollama rm llama3.2

# Test a model
ollama run llama3.2 "Hello!"

# Check version
ollama --version

# Start server manually
ollama serve
```

## 📚 Learn More

**Official Ollama Docs:**
- Website: https://ollama.ai/
- Models: https://ollama.ai/library
- GitHub: https://github.com/ollama/ollama

**Available Models:**
- See all: https://ollama.ai/library
- 50+ open-source models
- All completely free!

## 🎯 For Your Portfolio

### Talking Points:

**Interviewer**: "How did you handle costs during development?"

**You**: "I used Ollama, which runs open-source LLMs locally. This gave me unlimited testing without API costs, and I designed the architecture to easily switch between local models and cloud APIs. For production, we could use Claude or GPT-4, but Ollama was perfect for development."

**Highlights**:
- ✅ Cost-effective development
- ✅ Understanding of deployment tradeoffs
- ✅ Flexible architecture design
- ✅ Knowledge of both local and cloud solutions

## ✨ Advantages for Portfolio

1. **Demonstrate Cost Awareness**
   - You understand infrastructure costs
   - You made smart tradeoff decisions
   - You can optimize for different scenarios

2. **Show Technical Breadth**
   - You know cloud APIs AND local models
   - You understand deployment options
   - You can adapt to constraints

3. **Unlimited Development**
   - Test as much as you want
   - No budget concerns
   - Perfect for learning and experimentation

## 🚀 You're Ready!

Now you can build and demo your AI agent with:
- ✅ **Zero cost**
- ✅ **No API keys**
- ✅ **Unlimited usage**
- ✅ **Complete privacy**

Perfect for a portfolio project! 🎉

---

## Quick Start Checklist

- [ ] Install Ollama from ollama.ai
- [ ] Run: `ollama pull llama3.2`
- [ ] Install Python dependencies: `pip install -r requirements-free.txt`
- [ ] Test: `python src/agent_free.py`
- [ ] Start building: `python src/cli_free.py`

**Questions?** Check the troubleshooting section above!
