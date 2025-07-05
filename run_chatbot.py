#!/usr/bin/env python3
"""
Simple script to run the Gradio chatbot interface
"""

import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

try:
    from gradio_chatbot import demo

    print("🤖 Starting Gradio Chatbot Interface...")
    print("🌐 Interface will be available at: http://localhost:7860")
    print("=" * 50)

    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        quiet=False,
    )

except KeyboardInterrupt:
    print("\n🛑 Chatbot stopped")
except Exception as e:
    print(f"❌ Error starting chatbot: {e}")
    import traceback

    traceback.print_exc()
