"""
Simple JSON Storage
Saves and loads data from JSON files
"""

import json
from pathlib import Path


class Storage:
    """Handle JSON file storage"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
    
    def load(self, key: str, default=None):
        """Load data from JSON file"""
        file_path = self.data_dir / f"{key}.json"
        
        if not file_path.exists():
            return default
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception:
            return default
    
    def save(self, key: str, data) -> bool:
        """Save data to JSON file"""
        file_path = self.data_dir / f"{key}.json"
        
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception:
            return False
