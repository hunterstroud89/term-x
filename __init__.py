"""Term-X package initialization"""
from core.app import TerminalApp

__version__ = "1.0.0"

def main():
    """Main entry point"""
    app = TerminalApp()
    app.run()
