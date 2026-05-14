"""
In this file, the CV template proprties can be configured.
"""

__all__ = [
    "bcv_config"
]

import yaml
from pathlib import Path
from addict import Dict
from BeyondCV.utils import merge_dicts_recursively


def _load_yaml(file_path: str | Path) -> dict[str, str]:
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        return {}


default_config_dir = Path(__file__).resolve().parent / "default_config.yaml"
current_config_dir = "current_config.yaml"

# ORDER MATTERS! Ensure current_config exists AFTER default_config
bcv_config: Dict = Dict(merge_dicts_recursively(
    _load_yaml(default_config_dir),
    _load_yaml(current_config_dir)
))
