#!/usr/bin/env python3
"""
SuperLua TUI - A Gemini-style command interface for the SuperLua transpiler
Clean splash screen with command-based interaction and autocompletion
"""

import os
import sys
from pathlib import Path
from typing import Optional, List, Tuple

from textual import on
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical, ScrollableContainer
from textual.widgets import (
    Header, Footer, Button, Static, Input, TextArea, Tree, 
    DirectoryTree, Label, ProgressBar, Log, Tabs, TabPane
)
from textual.screen import Screen
from textual.binding import Binding
from textual.reactive import reactive
from rich.console import Console
from rich.syntax import Syntax
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
import fnmatch

# Import our transpiler
from transpiler import transpile_superlua


class SuperLuaTUI(App):
    """SuperLua TUI Application - Gemini-style Command Interface"""
    
    CSS = """
    .splash-container {
        height: 1fr;
        align: center middle;
        content-align: center middle;
        margin: 2;
    }
    
    .command-container {
        height: 7;
        dock: bottom;
        border: solid $primary;
        margin: 1;
        padding: 1;
    }
    
    .logo-text {
        text-align: center;
        color: $accent;
        text-style: bold;
        margin: 1;
    }
    
    .subtitle-text {
        text-align: center;
        color: $text-muted;
        text-style: italic;
        margin-bottom: 2;
    }
    
    .command-prompt {
        color: $primary;
        text-style: bold;
        margin-bottom: 1;
    }
    
    .completion-text {
        color: $text-muted;
        text-style: italic;
        margin-top: 1;
        height: 1;
    }
    
    #command_input {
        margin-top: 1;
        border: solid $accent;
        background: $surface;
        color: $text;
        height: 3;
        padding: 1;
    }
    
    #command_input:focus {
        border: solid $warning;
        background: $panel;
        color: $primary;
    }
    
    .help-text {
        text-align: center;
        color: $text-muted;
        margin: 1;
    }
    
    .version-text {
        text-align: center;
        color: $text-disabled;
        text-style: dim;
        margin-top: 1;
    }
    """
    
    TITLE = "SuperLua"
    SUB_TITLE = "Command Interface"
    
    BINDINGS = [
        Binding("ctrl+c", "quit", "Quit"),
        Binding("ctrl+q", "quit", "Quit"),
        Binding("tab", "autocomplete", "Complete"),
        Binding("escape", "clear", "Clear"),
        Binding("f1", "help", "Help"),
    ]
    
    def __init__(self):
        super().__init__()
        self.commands = ["compile", "help", "list", "clear", "quit", "exit"]
        self.all_files = []
        self.update_file_list()
    
    def compose(self) -> ComposeResult:
        yield Header()
        
        # Splash screen
        with Container(classes="splash-container"):
            yield Static("""
   ███████╗██╗   ██╗██████╗ ███████╗██████╗ ██╗     ██╗   ██╗ █████╗ 
   ██╔════╝██║   ██║██╔══██╗██╔════╝██╔══██╗██║     ██║   ██║██╔══██╗
   ███████╗██║   ██║██████╔╝█████╗  ██████╔╝██║     ██║   ██║███████║
   ╚════██║██║   ██║██╔═══╝ ██╔══╝  ██╔══██╗██║     ██║   ██║██╔══██║
   ███████║╚██████╔╝██║     ███████╗██║  ██║███████╗╚██████╔╝██║  ██║
   ╚══════╝ ╚═════╝ ╚═╝     ╚══════╝╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝
            """, classes="logo-text")
            
            yield Static("✨ Object-Oriented Programming for Lua ✨", classes="subtitle-text")
            
            yield Static("Available commands: compile, help, list, clear, quit", classes="help-text")
            yield Static("Type a command and press Tab for autocompletion", classes="help-text")
            yield Static("v1.0.0", classes="version-text")
        
        # Command input area
        with Container(classes="command-container"):
            yield Static("SuperLua > ", classes="command-prompt", id="prompt")
            yield Input(
                placeholder="Type 'compile <filename>' or 'help'...",
                id="command_input"
            )
            yield Static("💡 Tip: Press Tab to autocomplete commands and filenames", 
                        id="completion_hint", classes="completion-text")
        
        yield Footer()
    
    def on_mount(self):
        """Called when the app starts"""
        self.update_file_list()
        # Focus the command input
        command_input = self.query_one("#command_input", Input)
        command_input.focus()
    
    def update_file_list(self):
        """Update the list of all .slua files"""
        current_dir = Path('.')
        self.all_files = []
        
        # Find all .slua files recursively
        for slua_file in current_dir.rglob('*.slua'):
            self.all_files.append(str(slua_file))
        
        self.all_files.sort()
    
    def get_command_completions(self, partial: str) -> List[str]:
        """Get command completions for partial input"""
        if not partial:
            return self.commands
        
        return [cmd for cmd in self.commands if cmd.startswith(partial.lower())]
    
    def get_filename_completions(self, partial: str) -> List[str]:
        """Get filename completions for partial input"""
        if not partial:
            return [os.path.basename(f) for f in self.all_files]
        
        partial_lower = partial.lower()
        completions = []
        
        for file_path in self.all_files:
            filename = os.path.basename(file_path)
            if filename.lower().startswith(partial_lower):
                completions.append(filename)
        
        return completions
    
    def update_completion_hint(self, text: str):
        """Update the completion hint display"""
        hint_widget = self.query_one("#completion_hint", Static)
        
        if not text.strip():
            hint_widget.update("💡 Tip: Press Tab to autocomplete commands and filenames")
            return
        
        parts = text.split()
        
        if len(parts) == 1:
            # Command completion
            partial = parts[0]
            completions = self.get_command_completions(partial)
            
            if completions and partial:
                best_match = completions[0]
                if best_match.startswith(partial.lower()):
                    # Show greyed out completion
                    remaining = best_match[len(partial):]
                    hint_widget.update(f"📝 Press Tab: {partial}[dim]{remaining}[/dim] | Available: {', '.join(completions[:3])}")
                else:
                    hint_widget.update(f"📋 Available commands: {', '.join(completions[:3])}")
            elif completions:
                hint_widget.update(f"📋 Available commands: {', '.join(completions[:3])}")
            else:
                hint_widget.update("❌ No matching commands found")
                
        elif len(parts) == 2 and parts[0].lower() == "compile":
            # Filename completion
            partial = parts[1]
            completions = self.get_filename_completions(partial)
            
            if completions and partial:
                best_match = completions[0]
                if best_match.lower().startswith(partial.lower()):
                    # Show greyed out completion
                    remaining = best_match[len(partial):]
                    hint_widget.update(f"📁 Press Tab: {partial}[dim]{remaining}[/dim] | Files: {', '.join(completions[:3])}")
                else:
                    hint_widget.update(f"📁 Available files: {', '.join(completions[:3])}")
            elif completions:
                hint_widget.update(f"📁 Available files: {', '.join(completions[:3])}")
            else:
                hint_widget.update("❌ No matching .slua files found")
        else:
            hint_widget.update("💡 Tip: Type 'help' for available commands")
    
    @on(Input.Changed, "#command_input")
    def handle_input_change(self, event: Input.Changed):
        """Handle changes to command input"""
        self.update_completion_hint(event.value)
    
    @on(Input.Submitted, "#command_input")
    def handle_command_submit(self, event: Input.Submitted):
        """Handle command submission"""
        command = event.value.strip()
        if not command:
            return
        
        self.execute_command(command)
        
        # Clear the input
        command_input = self.query_one("#command_input", Input)
        command_input.value = ""
        self.update_completion_hint("")
    
    def action_autocomplete(self):
        """Handle Tab key for autocompletion"""
        command_input = self.query_one("#command_input", Input)
        current_text = command_input.value
        
        if not current_text.strip():
            return
        
        parts = current_text.split()
        
        if len(parts) == 1:
            # Command completion
            partial = parts[0]
            completions = self.get_command_completions(partial)
            
            if completions:
                # Use the first matching completion
                command_input.value = completions[0] + " "
                
        elif len(parts) == 2 and parts[0].lower() == "compile":
            # Filename completion
            partial = parts[1]
            completions = self.get_filename_completions(partial)
            
            if completions:
                # Use the first matching completion
                command_input.value = f"compile {completions[0]}"
        
        self.update_completion_hint(command_input.value)
    
    def action_clear(self):
        """Clear the command input"""
        command_input = self.query_one("#command_input", Input)
        command_input.value = ""
        self.update_completion_hint("")
    
    def execute_command(self, command: str):
        """Execute a command"""
        parts = command.split()
        if not parts:
            return
        
        cmd = parts[0].lower()
        
        if cmd in ["quit", "exit"]:
            self.exit()
        elif cmd == "help":
            self.show_help()
        elif cmd == "list":
            self.list_files()
        elif cmd == "clear":
            self.action_clear()
        elif cmd == "compile":
            if len(parts) < 2:
                self.notify("❌ Usage: compile <filename>", severity="error")
                return
            
            filename = parts[1]
            self.compile_file(filename)
        else:
            self.notify(f"❌ Unknown command: {cmd}", severity="error")
    
    def compile_file(self, filename: str):
        """Compile a SuperLua file"""
        # Find the full path
        file_path = None
        
        # Try exact match first
        for f in self.all_files:
            if os.path.basename(f) == filename:
                file_path = f
                break
        
        # Try adding .slua extension
        if not file_path and not filename.endswith('.slua'):
            filename_with_ext = filename + '.slua'
            for f in self.all_files:
                if os.path.basename(f) == filename_with_ext:
                    file_path = f
                    break
        
        if not file_path:
            self.notify(f"❌ File not found: {filename}", severity="error")
            return
        
        try:
            # Read the .slua file
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Transpile it
            transpiled = transpile_superlua(content)
            
            # Write the .lua file
            output_path = file_path.replace('.slua', '.lua')
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(transpiled)
            
            self.notify(f"✅ Compiled {os.path.basename(file_path)} → {os.path.basename(output_path)}", 
                       severity="information")
            
        except Exception as e:
            self.notify(f"❌ Compilation error: {e}", severity="error")
    
    def list_files(self):
        """List all .slua files"""
        if not self.all_files:
            self.notify("📁 No .slua files found", severity="information")
            return
        
        files_list = []
        for file_path in self.all_files:
            filename = os.path.basename(file_path)
            # Check if corresponding .lua file exists
            lua_path = file_path.replace('.slua', '.lua')
            status = "✅ Compiled" if os.path.exists(lua_path) else "⏳ Not compiled"
            files_list.append(f"{filename} - {status}")
        
        files_text = "\n".join(files_list)
        self.notify(f"📁 SuperLua Files:\n{files_text}", severity="information")
    
    def show_help(self):
        """Show help information"""
        help_text = """SuperLua Command Interface

Available Commands:
  • compile <filename>  - Compile a .slua file to .lua
  • list               - List all .slua files in project
  • help               - Show this help message
  • clear              - Clear command input
  • quit/exit          - Exit the application

Autocompletion:
  • Type 'comp' and press Tab → 'compile '
  • Type 'compile my' and press Tab → complete filename
  • Greyed text shows what Tab will complete

Examples:
  • compile calculator.slua
  • compile calc (auto-adds .slua)
  • list
  • help

Tips:
  • Use Tab for autocompletion
  • File names are case-sensitive
  • .slua extension is optional for compile command"""
        
        self.notify(help_text, severity="information")


def main():
    """Entry point for the TUI application"""
    app = SuperLuaTUI()
    app.run()


if __name__ == "__main__":
    main()