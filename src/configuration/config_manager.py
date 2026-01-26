import json
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    """
    Configuration manager that loads config.json settings and supports CLI overrides.
    """
    
    def __init__(self, config_file: Optional[Path] = None, overrides: Optional[Dict[str, Any]] = None):
        """
        Initialize the Config manager with optional CLI overrides.
        
        Args:
            config_file: Optional path to config.json.
            overrides: Optional dictionary of CLI parameters (e.g., from conftest.py).
        """
        self.config_file = config_file or self._default_config_path()
        self._data = self._load()
        self._overrides = overrides or {}
    
    @staticmethod
    def _default_config_path() -> Path:
        return Path(__file__).parent / "config.json"
    
    def _load(self) -> Dict[str, Any]:
        if not self.config_file.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_file}")
        
        with open(self.config_file, "r") as f:
            return json.load(f)
    
    @property
    def base_url(self) -> str:
        """Priority: 1. CLI Override -> 2. JSON Config -> 3. Default Empty String"""
        return self._overrides.get("base_url") or self._data.get("base_url", "")
    
    @property
    def api_version(self) -> str:
        return self._data.get("api_version", "v1")
    
    @property
    def quote_expiry_time_sec(self) -> float:
        return float(self._data.get("quote_expiry_time_sec", 20))
    
    @property
    def service_fee(self) -> float:
        """Priority: 1. CLI Override -> 2. JSON Config -> 3. Default 0.0"""
        fee = self._overrides.get("fee")
        if fee is not None:
            return float(fee)
        return float(self._data.get("fees", {}).get("service_fee", 0.0))
    
    @property
    def decimal_precision(self) -> int:
        """Priority: 1. CLI Override -> 2. JSON Config -> 3. Default 2"""
        precision = self._overrides.get("precision")
        if precision is not None:
            return int(precision)
        return int(self._data.get("decimal_precision", 2))

    def get(self, key: str, default: Any = None) -> Any:
        if key in self._overrides and self._overrides[key] is not None:
            return self._overrides[key]
            
        if "." in key:
            keys = key.split(".")
            value = self._data
            for k in keys:
                value = value.get(k) if isinstance(value, dict) else None
                if value is None:
                    return default
            return value
        return self._data.get(key, default)
    
    def to_dict(self) -> Dict[str, Any]:
        """Returns a merged view of the config for logging purposes."""
        merged = self._data.copy()
        # Update with non-None overrides
        for k, v in self._overrides.items():
            if v is not None:
                if k == "fee": # Map CLI 'fee' to the 'fees' nested structure if needed
                    merged.setdefault("fees", {})["service_fee"] = v
                elif k == "precision":
                    merged["decimal_precision"] = v
                else:
                    merged[k] = v
        return merged

    def __repr__(self) -> str:
        return f"Config(base_url={self.base_url}, fee={self.service_fee}, precision={self.decimal_precision})"