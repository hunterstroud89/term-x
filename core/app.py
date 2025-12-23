"""
Main Terminal Application
Handles layout, navigation, and app switching
"""

from textual.app import App, ComposeResult
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.widgets import Header, Footer, Static, Input, ListView, ListItem, Label
from textual.binding import Binding
from pathlib import Path
import yaml

from core.terminal import Terminal
from core.storage import Storage


class TerminalApp(App):
    """Main TUI Application"""
    
    BINDINGS = [
        Binding("h", "switch_app('home')", "Home", show=False),
        Binding("n", "switch_app('notes')", "Notes", show=False),
        Binding("t", "switch_app('todo')", "Todo", show=False),
        Binding("escape", "clear_cli", "Clear", show=False),
        Binding("q", "quit", "Quit", show=False),
        Binding("ctrl+c", "quit", "Quit", show=False),
    ]
    
    CSS = """
    Screen {
        background: #1e1e2e;
    }
    
    #title-bar {
        height: 1;
        background: #313244;
        color: #cba6f7;
        text-align: center;
    }
    
    #hint-bar {
        height: 1;
        background: #313244;
        color: #a6adc8;
        text-align: center;
    }
    
    #main-container {
        layout: horizontal;
    }
    
    #nav-panel {
        width: 25;
        border: solid #45475a;
        border-title-color: #6c7086;
        border-title-background: #1e1e2e;
        background: #1e1e2e;
        padding: 1;
    }
    
    #right-column {
        layout: vertical;
        width: 1fr;
    }
    
    #app-panel {
        border: solid #45475a;
        border-title-color: #6c7086;
        border-title-background: #1e1e2e;
        background: #1e1e2e;
        height: 1fr;
        padding: 1;
    }
    
    #app-content {
        height: 1fr;
        color: #a6adc8;
    }
    
    #cli-panel {
        border: solid #45475a;
        border-title-color: #6c7086;
        border-title-background: #1e1e2e;
        background: #1e1e2e;
        height: 10;
        padding: 1;
    }
    
    #cli-output {
        height: 1fr;
        color: #a6adc8;
    }
    
    #cli-input {
        background: #1e1e2e;
        border: none;
        color: #cdd6f4;
    }
    
    ListView {
        background: transparent;
    }
    
    ListItem {
        color: #a6adc8;
        background: transparent;
    }
    
    ListItem.--highlight {
        background: #313244;
    }
    
    ListItem.-active {
        color: #cba6f7;
    }
    """
    
    def __init__(self):
        super().__init__()
        self.apps = self.load_apps()
        self.current_app = "home"
        self.terminal = Terminal()
        self.storage = Storage()
        self.command_history = []
        self.history_index = -1
        
    def compose(self) -> ComposeResult:
        """Create layout"""
        yield Static("TERM-X TERMINAL v1.0", id="title-bar")
        
        with Container(id="main-container"):
            # Navigation panel
            with Vertical(id="nav-panel") as nav_panel:
                nav_panel.border_title = "NAVIGATION"
                yield ListView(
                    *[ListItem(Label(app["name"])) for app in self.apps.values()],
                    id="nav-list"
                )
            
            # Right column
            with Vertical(id="right-column"):
                # App panel
                with Vertical(id="app-panel") as app_panel:
                    app_panel.border_title = "HOME"
                    yield Static("Welcome to Term-X", id="app-content")
                
                # CLI panel  
                with Vertical(id="cli-panel") as cli_panel:
                    cli_panel.border_title = "CLI"
                    yield Static("", id="cli-output")
                    yield Input(placeholder="type command...", id="cli-input")
        
        yield Static("←→: navigate | H: home | N: notes | T: todo | ↑↓: history | Q: quit | Tab: focus", id="hint-bar")
    
    def on_mount(self) -> None:
        """Initialize app on startup"""
        self.load_app("home")
        
    def action_switch_app(self, app_id: str) -> None:
        """Switch to a specific app via keyboard shortcut"""
        if app_id in self.apps:
            self.load_app(app_id)
    
    def action_clear_cli(self) -> None:
        """Clear CLI output"""
        cli_output = self.query_one("#cli-output", Static)
        cli_output.update("")
        cli_input = self.query_one("#cli-input", Input)
        cli_input.value = ""
    
    def load_apps(self) -> dict:
        """Load all apps from apps directory"""
        apps = {}
        apps_dir = Path("apps")
        
        for app_dir in apps_dir.iterdir():
            if app_dir.is_dir():
                config_file = app_dir / "config.yaml"
                if config_file.exists():
                    with open(config_file) as f:
                        config = yaml.safe_load(f)
                        apps[config["id"]] = config
        
        return apps
    
    def load_app(self, app_id: str) -> None:
        """Load and display an app"""
        if app_id not in self.apps:
            return
            
        app_config = self.apps[app_id]
        self.current_app = app_id
        
        # Update panel border title
        app_panel = self.query_one("#app-panel")
        app_panel.border_title = app_config["name"].upper()
        
        # Load app view
        app_module = f"apps.{app_id}.view"
        try:
            module = __import__(app_module, fromlist=["render"])
            content = module.render(self.storage)
            
            app_content = self.query_one("#app-content", Static)
            app_content.update(content)
        except Exception as e:
            app_content = self.query_one("#app-content", Static)
            app_content.update(f"Error loading app: {e}")
        
        # Update CLI panel title with hints
        cli_panel = self.query_one("#cli-panel")
        hints = app_config.get("hints", "")
        cli_panel.border_title = f"CLI - {hints}" if hints else "CLI"
        
        # Update navigation highlight
        self.update_nav_highlight()
    
    def update_nav_highlight(self) -> None:
        """Update active app in navigation"""
        nav_list = self.query_one("#nav-list", ListView)
        app_ids = list(self.apps.keys())
        
        for idx, app_id in enumerate(app_ids):
            item = nav_list.children[idx]
            if app_id == self.current_app:
                item.add_class("-active")
            else:
                item.remove_class("-active")
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle app selection from navigation"""
        app_ids = list(self.apps.keys())
        selected_idx = event.list_view.index
        if 0 <= selected_idx < len(app_ids):
            self.load_app(app_ids[selected_idx])
    
    def on_key(self, event) -> None:
        """Handle key presses for history navigation"""
        cli_input = self.query_one("#cli-input", Input)
        nav_list = self.query_one("#nav-list", ListView)
        
        # Handle 'q' to quit only when input is NOT focused
        if event.key == "q" and not cli_input.has_focus:
            self.exit()
            event.prevent_default()
            return
        
        # Handle left/right arrow keys for focus switching when CLI is NOT focused
        if not cli_input.has_focus:
            if event.key == "right":
                cli_input.focus()
                event.prevent_default()
                return
            elif event.key == "left":
                nav_list.focus()
                event.prevent_default()
                return
        
        # When CLI input is focused, handle arrows differently
        if cli_input.has_focus:
            # Left arrow goes back to navigation
            if event.key == "left" and len(cli_input.value) == 0:
                nav_list.focus()
                event.prevent_default()
                return
            
            # Up/down for command history
            if event.key == "up":
                if self.command_history and self.history_index > 0:
                    self.history_index -= 1
                    cli_input.value = self.command_history[self.history_index]
                    cli_input.cursor_position = len(cli_input.value)
                    event.prevent_default()
            elif event.key == "down":
                if self.command_history:
                    if self.history_index < len(self.command_history) - 1:
                        self.history_index += 1
                        cli_input.value = self.command_history[self.history_index]
                    else:
                        self.history_index = len(self.command_history)
                        cli_input.value = ""
                    cli_input.cursor_position = len(cli_input.value)
                    event.prevent_default()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle CLI command submission"""
        if event.input.id != "cli-input":
            return
            
        command = event.value.strip()
        if not command:
            return
        
        # Add to history
        self.command_history.append(command)
        self.history_index = len(self.command_history)
        
        # Execute command
        result = self.terminal.execute(command, self.current_app, self.storage)
        
        # Show output
        output = self.query_one("#cli-output", Static)
        current_output = str(output.renderable) if output.renderable else ""
        output_text = result.get('output', str(result))
        new_output = f"{current_output}\n> {command}\n{output_text}" if current_output else f"> {command}\n{output_text}"
        if result.get("reload"):
            self.load_app(self.current_app)
        
        # Clear input
        event.input.value = ""
    
    def action_home(self) -> None:
        """Go to home app"""
        self.load_app("home")
    
    def action_focus_cli(self) -> None:
        """Focus the CLI input"""
        cli_input = self.query_one("#cli-input", Input)
        cli_input.focus()
