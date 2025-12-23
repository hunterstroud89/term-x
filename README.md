# Term-X - Python Terminal UI

A real terminal application built with Python and Textual.

## Quick Install

```bash
# Clone the repo
git clone https://github.com/hunterstroud89/term-x.git
cd term-x

# Run it (auto-installs dependencies first time)
./run.sh
```

## Install Globally (so you can run `term-x` from anywhere)

```bash
cd term-x

# Create launcher
echo '#!/bin/bash
cd "$(dirname "$0")"
python3 main.py' > term-x
chmod +x term-x

# Add to PATH
sudo ln -s "$(pwd)/term-x" /usr/local/bin/term-x
```

Now just type `term-x` anywhere!

## Update to Latest Version

```bash
cd term-x
git pull
```

## Requirements
- Python 3.7+
- Textual library (auto-installed by run.sh)

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
