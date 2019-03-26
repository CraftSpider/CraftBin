
from typing import Dict, Tuple, Any, Optional, List
import numbers
import minecraft.enums as enums

from PIL.Image import Image
from utils.vector import Vector

class Rotation:

    __slots__ = ("origin", "axis", "angle", "rescale")

    origin: Vector
    axis: Vector
    angle: numbers.Real
    rescale: bool

    def __init__(self, data: Dict[str, Any]) -> None: ...

class Face:

    __slots__ = ("side", "uv", "texture", "cull_face", "rotation", "tint_index")

    side: enums.Side
    uv: Optional[Tuple[int, int, int, int]]
    texture: str
    cull_face: enums.Side
    rotation: int
    tint_index: Optional[int]

    def __init__(self, side: str, data: Dict[str, Any]) -> None: ...

class Element:

    __slots__ = ("begin", "end", "rotation", "shade", "faces")

    begin: Vector
    end: Vector
    rotation: Rotation
    shade: bool
    faces: List[Face]

    def __init__(self, data: Dict[str, Any]) -> None: ...

    def __repr__(self) -> str: ...

    def get_face(self, side: enums.Side) -> Optional[Face]: ...

class Model:

    __slots__ = ("namespace", "name", "_effective_data", "_raw_data", "parent", "textures", "ambient_occlusion",
                 "elements")

    namespace: str
    name: str
    _effective_data: Dict[str, Any]
    _raw_data: Dict[str, Any]
    parent: Optional[Model]
    textures: Dict[str, str]
    ambient_occlusion: bool
    elements: List[Element]

    def __init__(self, namespace: str, name: str, data: Dict[str, Any]) -> None: ...

    def __repr__(self) -> str: ...

    def _get_effective(self) -> Dict[str, Any]: ...

    def _resolve_texture(self, name: str) -> str: ...

    def _resolve_side_rotation(self, x: int, y: int, z: int) -> Tuple[enums.Side, int]: ...

    def _resolve_uv(self, element: Element, face: Face, axis: str) -> Tuple[int, int, int, int]: ...

    def _resolve_darken(self, element: Element, axis: str) -> float: ...

    def inherits(self, name: str) -> bool: ...

    def get_top(self, x: int = ..., y: int = ..., z: int = ...) -> Optional[Image]: ...

    def get_sprite(self) -> Optional[Image]: ...

    @classmethod
    def get_model(cls, namespace: str, name: str) -> Model: ...
