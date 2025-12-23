"""
Todo App View
Displays task list
"""

def render(storage):
    """Render the todo app content"""
    todos = storage.load("todos", [])
    
    if not todos:
        return "No tasks yet.\\n\\nType 'add [task]' to create your first task!"
    
    pending = [t for t in todos if not t["done"]]
    completed = [t for t in todos if t["done"]]
    
    output = ""
    
    if pending:
        output += "Pending Tasks:\\n\\n"
        for i, todo in enumerate(todos):
            if not todo["done"]:
                output += f"  {i}: {todo['task']}\\n"
    
    if completed:
        output += "\\nCompleted Tasks:\\n\\n"
        for i, todo in enumerate(todos):
            if todo["done"]:
                output += f"  {i}: ✓ {todo['task']}\\n"
    
    return output
