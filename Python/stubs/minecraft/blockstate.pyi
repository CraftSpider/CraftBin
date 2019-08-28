
from typing import Dict, Any, Optional, Union, List

import numbers
import minecraft.enums as enums

from PIL.Image import Image
from minecraft.model import Model
from minecraft.schematic import Schematic

class Variant:

    __slots__ = ("model", "x", "y", "uv_lock", "weight")

    model: Model
    x: int
    y: int
    uv_lock: bool
    weight: numbers.Real

    def __init__(self, namespace: str, data: Dict[str, Any]) -> None: ...

    def __repr__(self) -> str: ...

    def get_side(self, side: enums.Side) -> Optional[Image]: ...

    def get_side_height(self, side: enums.Side) -> int: ...

    def get_sprite(self) -> Optional[Image]: ...

class Part:

    __slots__ = ("condition", "variant")

    condition: Dict[str, Any]
    variant: Union[Variant, List[Variant]]

    def __init__(self, namespace: str, data: Dict[str, Any]) -> None: ...

    def __repr__(self) -> str: ...

    def check_condition(self, x: int, y: int, z: int) -> bool: ...

    def get_variant(self) -> Variant: ...

class Blockstate:

    __slots__ = ("namespace", "name", "multipart", "variants", "parts")

    namespace: str
    name: str
    multipart: bool
    variants: Dict[str, Union[Variant, List[Variant]]]
    parts: List[Part]

    def __init__(self, namespace: str, name: str, data: Dict[str, Any]) -> None: ...

    def is_variant(self) -> bool: ...

    def is_multipart(self) -> bool: ...

    def has_variable(self, name: str) -> bool: ...

    def get_variant(self, **kwargs: Optional[str]) -> Optional[Variant]: ...

    def get_parts(self) -> List[Part]: ...

    @classmethod
    def get_blockstate(cls, namespace: str, block: str) -> Blockstate: ...
