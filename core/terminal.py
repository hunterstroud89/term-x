"""
Terminal Command Handler
Processes CLI commands and routes to apps
"""

class Terminal:
    """Command processor for the CLI"""
    
    def execute(self, command: str, current_app: str, storage) -> dict:
        """
        Execute a command and return result
        
        Returns dict with:
            - output: str (text to display)
            - redirect: str|None (app to switch to)
            - reload: bool (reload current app)
        """
        parts = command.split()
        cmd = parts[0] if parts else ""
        args = parts[1:]
        
        # Global commands
        if cmd == "open":
            if args:
                app_name = " ".join(args).lower()
                return {
                    "output": f"Opening {app_name}...",
                    "redirect": app_name,
                    "reload": False
                }
            return {"output": "Usage: open [app]", "redirect": None, "reload": False}
        
        if cmd == "home":
            return {
                "output": "Returning home...",
                "redirect": "home",
                "reload": False
            }
        
        if cmd == "ls":
            apps = ["home", "notes", "todo"]  # TODO: load dynamically
            output = "Available apps:\\n" + "\\n".join(f"  {app}" for app in apps)
            return {"output": output, "redirect": None, "reload": False}
        
        if cmd == "clear":
            return {"output": "", "redirect": None, "reload": False}
        
        if cmd == "help":
            output = """Global Commands:
  open [app] - Open an app
  home - Return to home
  ls - List apps
  clear - Clear terminal
  help - Show this message"""
            return {"output": output, "redirect": None, "reload": False}
        
        # App-specific commands
        if current_app == "notes":
            return self.handle_notes_command(cmd, args, storage)
        elif current_app == "todo":
            return self.handle_todo_command(cmd, args, storage)
        
        return {
            "output": f"Unknown command: {cmd}. Type 'help' for commands.",
            "redirect": None,
            "reload": False
        }
    
    def handle_notes_command(self, cmd: str, args: list, storage) -> dict:
        """Handle notes app commands"""
        notes = storage.load("notes", [])
        
        if cmd == "new":
            if args:
                title = " ".join(args)
                note = {"title": title, "content": ""}
                notes.append(note)
                storage.save("notes", notes)
                return {"output": f"Created note: {title}", "redirect": None, "reload": True}
            return {"output": "Usage: new [title]", "redirect": None, "reload": False}
        
        if cmd == "list":
            if not notes:
                return {"output": "No notes yet.", "redirect": None, "reload": False}
            output = "\\n".join(f"  {i}: {note['title']}" for i, note in enumerate(notes))
            return {"output": output, "redirect": None, "reload": False}
        
        return {"output": f"Unknown notes command: {cmd}", "redirect": None, "reload": False}
    
    def handle_todo_command(self, cmd: str, args: list, storage) -> dict:
        """Handle todo app commands"""
        todos = storage.load("todos", [])
        
        if cmd == "add":
            if args:
                task = " ".join(args)
                todos.append({"task": task, "done": False})
                storage.save("todos", todos)
                return {"output": f"Added task: {task}", "redirect": None, "reload": True}
            return {"output": "Usage: add [task]", "redirect": None, "reload": False}
        
        if cmd == "done":
            if args and args[0].isdigit():
                idx = int(args[0])
                if 0 <= idx < len(todos):
                    todos[idx]["done"] = True
                    storage.save("todos", todos)
                    return {"output": f"Marked task {idx} as done", "redirect": None, "reload": True}
            return {"output": "Usage: done [id]", "redirect": None, "reload": False}
        
        if cmd == "list":
            if not todos:
                return {"output": "No tasks yet.", "redirect": None, "reload": False}
            output = "\\n".join(
                f"  {i}: {'✓' if t['done'] else ' '} {t['task']}" 
                for i, t in enumerate(todos)
            )
            return {"output": output, "redirect": None, "reload": False}
        
        return {"output": f"Unknown todo command: {cmd}", "redirect": None, "reload": False}
