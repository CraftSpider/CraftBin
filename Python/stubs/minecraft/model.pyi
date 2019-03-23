
from typing import Dict, Tuple, Any, Optional, List, Union
from pathlib import Path
from PIL.Image import Image

class Model:

    __slots__ = ("namespace", "name", "_effective_data", "_raw_data", "parent", "textures", "ambient_occlusion",
                 "elements")

    UP_IDS: Dict[str, Tuple[int, int]] = ...

    namespace: str
    name: str
    _effective_data: Dict[str, Any]
    _raw_data: Dict[str, Any]
    parent: Optional[Model]
    textures: Dict[str, str]
    ambient_occlusion: bool
    elements: List[Dict[Any, Any]]

    def __init__(self, namespace: str, name: str, data: Dict[str, Any]) -> None: ...

    def __repr__(self) -> str: ...

    def _get_effective(self) -> Dict[str, Any]: ...

    def _resolve_texture(self, name: str) -> str: ...

    def inherits(self, name: str) -> bool: ...

    def _resolve_side_rotation(self, x: int, y: int, z: int):

    def get_top(self, x: int = ..., y: int = ..., z: int = ...) -> Optional[Image]: ...

    def get_sprite(self) -> Optional[Image]: ...

    @classmethod
    def get_model(cls, namespace: str, name: str) -> Model: ...
