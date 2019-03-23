
from typing import Dict, Optional, Any, Tuple, Union
from nbt.nbt import NBTFile
from pathlib import Path

class SchematicError(Exception): ...

class Schematic:

    __slots__ = ("nbt", "height", "width", "length", "id_map", "datamap")

    nbt: NBTFile
    height: int
    width: int
    length: int
    id_map: Dict[int, str]
    datamap: Optional[Dict[Any, Any]]

    def __init__(self, file: NBTFile) -> None: ...

    def _apply_datamap(self, namespace: str, block: str, data: int) -> Tuple[str, str, int]: ...

    def load_datamap(self, filename: Union[Path, str, bytes]) -> None: ...

    def get_block(self, x: int, y: int, z: int) -> Tuple[str, str, int]: ...

def load_schematic(path: Union[str, bytes, Path]) -> Optional[Schematic]: ...
