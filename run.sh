#!/bin/bash

# Term-X Auto-Setup and Run Script

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "First time setup - creating virtual environment..."
    python3 -m venv venv
    
    # Activate and install dependencies
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
    echo "Setup complete!"
else
    # Just activate existing venv
    source venv/bin/activate
fi

# Run the app
python main.py
