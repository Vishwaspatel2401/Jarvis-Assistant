import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv

class ConfigManager:
    def __init__(self, config_file: str = "config.json", env_file: str = ".env"):
        self.config_file = config_file
        self.env_file = env_file
        self.config: Dict[str, Any] = {}
        self._load_config()

    def _load_config(self) -> None:
        """Load configuration from file and environment variables."""
        # Load environment variables
        load_dotenv(self.env_file)

        # Load JSON config
        config_path = Path(self.config_file)
        if config_path.exists():
            with open(config_path, 'r') as f:
                self.config = json.load(f)

        # Override with environment variables
        for key in self.config:
            env_value = os.getenv(key.upper())
            if env_value is not None:
                self.config[key] = env_value

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value."""
        self.config[key] = value
        self._save_config()

    def _save_config(self) -> None:
        """Save configuration to file."""
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f, indent=4)

    def get_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        """Get configuration for a specific plugin."""
        return self.config.get(f"plugins.{plugin_name}", {})

    def update_plugin_config(self, plugin_name: str, config: Dict[str, Any]) -> None:
        """Update configuration for a specific plugin."""
        if "plugins" not in self.config:
            self.config["plugins"] = {}
        self.config["plugins"][plugin_name] = config
        self._save_config() 