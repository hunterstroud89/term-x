"""
Notes App View
Displays list of notes
"""

def render(storage):
    """Render the notes app content"""
    notes = storage.load("notes", [])
    
    if not notes:
        return "No notes yet.\\n\\nType 'new [title]' to create your first note!"
    
    output = "Your Notes:\\n\\n"
    for i, note in enumerate(notes):
        output += f"  {i}: {note['title']}\\n"
    
    return output
