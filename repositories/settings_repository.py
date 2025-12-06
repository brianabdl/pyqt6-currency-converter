"""
Repository for managing application settings
"""
import json
import os
from typing import Dict, Any

class SettingsRepository:
    """Handles storage and retrieval of application settings"""
    
    DEFAULT_SETTINGS = {
        "default_from_currency": "USD",
        "default_to_currency": "EUR",
        "theme": "light"
    }
    
    def __init__(self, storage_file: str = "settings.json"):
        self._storage_file = storage_file
        self._settings: Dict[str, Any] = self.DEFAULT_SETTINGS.copy()
        self._load()
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a setting value"""
        return self._settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a setting value and save"""
        self._settings[key] = value
        self._save()
    
    def get_all(self) -> Dict[str, Any]:
        """Get all settings"""
        return self._settings.copy()
    
    def _save(self):
        """Save settings to file"""
        try:
            with open(self._storage_file, 'w') as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    def _load(self):
        """Load settings from file"""
        if not os.path.exists(self._storage_file):
            self._save() # Create default file
            return
            
        try:
            with open(self._storage_file, 'r') as f:
                data = json.load(f)
                self._settings.update(data)
        except Exception as e:
            print(f"Error loading settings: {e}")
