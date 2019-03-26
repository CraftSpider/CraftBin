
from typing import Dict, Any, Optional, Union, List
import numbers
from minecraft.model import Model

class Variant:

    __slots__ = ("model", "x", "y", "uv_lock", "weight")

    model: Model
    x: int
    y: int
    uv_lock: bool
    weight: numbers.Real

    def __init__(self, namespace: str, data: Dict[str, Any]) -> None: ...

class Part:

    __slots__ = ("condition", "variant")

    condition: Dict[str, Any]
    variant: Union[Variant, List[Variant]]

    def __init__(self, namespace: str, data: Dict[str, Any]) -> None: ...

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

    def get_variant(self, **kwargs: Optional[str]): ...

    @classmethod
    def get_blockstate(cls, namespace: str, block: str) -> Blockstate: ...
