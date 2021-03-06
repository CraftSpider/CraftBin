
from typing import Dict, Any, Optional
from pathlib import Path
from minecraft.model import Model
from minecraft.blockstate import Blockstate
from minecraft.schematic import Schematic

_DEFAULT_RESOURCE_PATH: Path = ...

class Config:

    resource_path: Path
    block_size: int
    models: Dict[str, Model]
    blockstates: Dict[str, Blockstate]

    schematic: Optional[Schematic]

    def __init__(self, settings: Dict[str, Any] = ...) -> None: ...

    @property
    def ef_size(self) -> int: ...

DEFAULT_CONFIG = Config()
_CUR_CONFIG = DEFAULT_CONFIG

def get_config() -> Config: ...

def set_config(config: Config) -> None: ...
