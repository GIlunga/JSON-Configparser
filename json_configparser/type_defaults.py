from typing import NamedTuple, Any
from . import bounds


class TypeDefaultBounds(NamedTuple):
    arg_name: str
    type_: type
    has_default: bool = False
    default_value: Any = None
    bound_obj: bounds.Bounds = None
