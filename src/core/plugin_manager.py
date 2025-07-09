from typing import Dict, Type, Any
import importlib
import inspect
from pathlib import Path

class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, Any] = {}
        self._plugin_configs: Dict[str, dict] = {}

    def register_plugin(self, name: str, plugin_class: Type[Any], config: dict = None):
        """Register a new plugin with optional configuration."""
        self._plugins[name] = plugin_class
        self._plugin_configs[name] = config or {}

    def get_plugin(self, name: str) -> Any:
        """Get a registered plugin instance."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' not found")
        return self._plugins[name]

    def load_plugins_from_directory(self, directory: str):
        """Load all plugins from a directory."""
        plugin_dir = Path(directory)
        if not plugin_dir.exists():
            raise FileNotFoundError(f"Plugin directory '{directory}' not found")

        for file in plugin_dir.glob("*.py"):
            if file.name.startswith("__"):
                continue

            module_name = file.stem
            try:
                module = importlib.import_module(f"{directory.replace('/', '.')}.{module_name}")
                for name, obj in inspect.getmembers(module):
                    if inspect.isclass(obj) and hasattr(obj, 'is_plugin') and obj.is_plugin:
                        self.register_plugin(name, obj)
            except Exception as e:
                print(f"Error loading plugin from {file}: {e}")

    def get_all_plugins(self) -> Dict[str, Any]:
        """Get all registered plugins."""
        return self._plugins.copy()

    def get_plugin_config(self, name: str) -> dict:
        """Get configuration for a specific plugin."""
        return self._plugin_configs.get(name, {}) 