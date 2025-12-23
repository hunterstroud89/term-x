# Term-X - Python Terminal UI

A real terminal application built with Python and Textual.

## Requirements
- Python 3.11+
- Textual library

## Installation

```bash
cd term-x
pip install textual pyyaml
```

## Running the App

```bash
python main.py
```

## Keyboard Shortcuts
- `↑↓` - Navigate apps
- `Enter` - Open selected app
- `:` - Focus CLI input
- `Esc` - Return to home
- `Ctrl+C` - Quit

## Project Structure

```
term-x/
  main.py           ← Entry point - run this
  core/
    app.py          ← Main application class
    terminal.py     ← CLI command handler
    storage.py      ← JSON data storage
  apps/
    home/
      config.yaml   ← App metadata
      view.py       ← Display logic
    notes/
    todo/
  data/             ← JSON storage files
```

## Building New Apps

1. Create folder in `apps/`
2. Add `config.yaml` with app info
3. Create `view.py` with your UI
4. Optional: Add command handlers

See existing apps for examples!
