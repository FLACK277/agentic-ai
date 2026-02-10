import sys
import os

# Add current directory to path
sys.path.append(os.getcwd())

try:
    from src.agent import run_agent
    print("Agent imported successfully.")
    result = run_agent("hello")
    print(f"Result: {result}")
except Exception:
    import traceback
    traceback.print_exc()
