import json
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """
    Configuration manager that loads config.json settings.
    
    Provides access to configuration values.
    """
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize the Config manager.
        
        Args:
            config_file: Optional path to config.json. If not provided,
                        uses the default location (src/configuration/config.json)
        """
        self.config_file = config_file or self._default_config_path()
        self._data = self._load()
    
    @staticmethod
    def _default_config_path() -> Path:
        """
        Get the default configuration file path.
        
        Returns:
            Path: Path to config.json in the same directory
        """
        return Path(__file__).parent / "config.json"
    
    def _load(self) -> Dict[str, Any]:
        """
        Load and parse the JSON configuration file.
        
        Returns:
            dict: Parsed configuration data
            
        Raises:
            FileNotFoundError: If config file doesn't exist
            json.JSONDecodeError: If config file is invalid JSON
        """
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        
        with open(self.config_file, "r") as f:
            return json.load(f)
    
    @property
    def base_url(self) -> str:
        """
        Get the base URL from configuration.
        
        Returns:
            str: Base URL for API requests
        """
        return self._data.get("base_url", "")
    
    @property
    def service_fee(self) -> float:
        """
        Get the service fee from configuration.
        
        Returns:
            float: Service fee percentage
        """
        return self._data.get("fees", {}).get("service_fee", 0.0)
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key (supports nested keys with dot notation)
            default: Default value if key not found
            
        Returns:
            Any: Configuration value or default
        """
        if "." in key:
            keys = key.split(".")
            value = self._data
            for k in keys:
                value = value.get(k) if isinstance(value, dict) else None
                if value is None:
                    return default
            return value
        return self._data.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """
        Allow dictionary-style access to configuration.
        
        Args:
            key: Configuration key
            
        Returns:
            Any: Configuration value
            
        Raises:
            KeyError: If key not found
        """
        return self._data[key]
    
    def __contains__(self, key: str) -> bool:
        """Check if a key exists in configuration."""
        return key in self._data
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Get the entire configuration as a dictionary.
        
        Returns:
            dict: Complete configuration data
        """
        return self._data.copy()
    
    def __repr__(self) -> str:
        """String representation of the Config object."""
        return f"Config(file={self.config_file}, keys={list(self._data.keys())})"
