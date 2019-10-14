"""
Implements the TypeDefaultBounds NamedTuple, which holds information about an argument.
"""

from typing import NamedTuple, Any
from . import bounds


class TypeDefaultBounds(NamedTuple):
    """
    NamedTuple representing the name, type, default value, and bounds of an argument.
    """
    #: the name of the argument
    arg_name: str
    #: the type of the argument
    type_: type = None
    #: flag to indicate if there is a default value for the argument
    has_default: bool = False
    #: the value of the default argument
    default_value: Any = None
    #: an instance of the Bound class, representing the bounds of the argument
    bound_obj: bounds.Bounds = None
