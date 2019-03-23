
from typing import Dict, Any
from pathlib import Path
from minecraft.model import Model
from minecraft.blockstate import Blockstate

_DEFAULT_RESOURCE_PATH: Path = ...

class Config:

    resource_path: Path
    models: Dict[str, Model]
    blockstates: Dict[str, Blockstate]

    def __init__(self, settings: Dict[str, Any] = ...) -> None: ...

DEFAULT_CONFIG = Config()
_CUR_CONFIG = DEFAULT_CONFIG

def get_config() -> Config: ...

def set_config(config: Config) -> None: ...
