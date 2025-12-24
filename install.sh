#!/bin/bash
set -e

echo "📦 Installing Term-X..."

# Get the script directory
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$INSTALL_DIR"

# Check for Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment
if [ ! -d "venv" ]; then
    echo "🔧 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install dependencies
echo "📥 Installing dependencies..."
source venv/bin/activate
pip install -q --upgrade pip
pip install -q -r requirements.txt

# Create symlink to PATH
SYMLINK_PATH="/usr/local/bin/term-x"

if [ -L "$SYMLINK_PATH" ] || [ -f "$SYMLINK_PATH" ]; then
    echo "🔄 Updating existing installation..."
    sudo rm -f "$SYMLINK_PATH"
fi

# Create launcher script
cat > term-x << 'EOF'
#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "$(readlink -f "$0" 2>/dev/null || realpath "$0")")" && pwd)"
cd "$SCRIPT_DIR"
source venv/bin/activate
python main.py "$@"
EOF

chmod +x term-x

# Create symlink
echo "🔗 Creating system-wide command..."
sudo ln -sf "$INSTALL_DIR/term-x" "$SYMLINK_PATH"

echo ""
echo "✅ Installation complete!"
echo ""
echo "Run 'term-x' from anywhere to start the app."
echo ""
