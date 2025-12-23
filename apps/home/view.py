"""
Home App View
Displays welcome message
"""

def render(storage):
    """Render the home app content"""
    return """Welcome to Term-X!

A Python terminal application with simple app building blocks.

Keyboard Shortcuts:
  ↑↓ - Navigate apps
  Enter - Open selected app
  : - Focus CLI input
  Esc - Return to home

Try typing a command below or navigate to Notes/Todo apps!
"""
