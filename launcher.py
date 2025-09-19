#!/usr/bin/env python3
"""
SuperLua Launcher - Choose between CLI and TUI interface
"""

import sys
import subprocess
from pathlib import Path

def main():
    print("🎯 SuperLua Transpiler")
    print("=" * 40)
    print("1. 🖥️  TUI (Modern Terminal Interface)")
    print("2. 💻 CLI (Command Line Interface)")
    print("3. ❌ Exit")
    print()
    
    while True:
        choice = input("Choose interface (1-3): ").strip()
        
        if choice == "1":
            print("🚀 Starting TUI...")
            try:
                subprocess.run([sys.executable, "superlua_tui.py"])
            except KeyboardInterrupt:
                print("\n👋 TUI closed")
            except Exception as e:
                print(f"❌ Error starting TUI: {e}")
            break
            
        elif choice == "2":
            print("🚀 Starting CLI...")
            try:
                subprocess.run([sys.executable, "transpiler.py"])
            except KeyboardInterrupt:
                print("\n👋 CLI closed")
            except Exception as e:
                print(f"❌ Error starting CLI: {e}")
            break
            
        elif choice == "3":
            print("👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()