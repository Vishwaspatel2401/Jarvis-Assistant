from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

class BasePlugin(ABC):
    is_plugin = True

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or {}
        self.initialized = False

    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the plugin with its configuration."""
        pass

    @abstractmethod
    async def execute(self, *args, **kwargs) -> Any:
        """Execute the plugin's main functionality."""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Clean up resources used by the plugin."""
        pass

    def get_config(self, key: str, default: Any = None) -> Any:
        """Get a configuration value with an optional default."""
        return self.config.get(key, default)

    def is_ready(self) -> bool:
        """Check if the plugin is properly initialized."""
        return self.initialized 