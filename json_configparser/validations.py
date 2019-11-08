"""
This module implements the type and bound validation of all supported types.
"""

from typing import Any

from . import type_defaults


def validate_argument(arg_value: Any, arg_type_defaults: type_defaults.TypeDefaultBounds) -> Any:
    """
    Given a value and type/bounds, this function checks if the type is supported.
    If so, then check if the value is of the correct type and if it is within the defined bounds.
    For Lists and Dictionaries these checks are applied to all elements.

    :param arg_value: The value of the argument to check.
    :param arg_type_defaults: An instance of TypeDefaultBounds, specifying the type and bounds of the argument to check.
    :raises ValueError: If the argument is an empty string.
    :raises TypeError: If the argument value is not of the expected type.
    """
    if arg_type_defaults.type_ == bool:
        if not isinstance(arg_value, bool):
            raise TypeError("The {name} argument should be a boolean "
                            "({name}: {value})".format(name=arg_type_defaults.arg_name, value=arg_value))

    elif arg_type_defaults.type_ == int or arg_type_defaults.type_ == float:
        if not isinstance(arg_value, arg_type_defaults.type_):
            # Allow 10.0 for integer arguments
            if arg_type_defaults.type_ == int and isinstance(arg_value, float) and float(int(arg_value)) == arg_value:
                return int(arg_value)
            # Allow 10 for float arguments
            elif arg_type_defaults.type_ == float and isinstance(arg_value, int):
                return float(arg_value)

            raise TypeError("The {name} argument should be a {type_} "
                            "({name}: {value})".format(name=arg_type_defaults.arg_name,
                                                       type_=arg_type_defaults.type_,
                                                       value=arg_value))
        if arg_type_defaults.bound_obj is not None:
            arg_type_defaults.bound_obj.validate_value(arg_value)

    elif arg_type_defaults.type_ == str:
        if not isinstance(arg_value, str):
            raise TypeError("The {name} argument should be a string "
                            "({name}: {value})".format(name=arg_type_defaults.arg_name, value=arg_value))
        # TODO: Consider allowing empty strings
        if not len(arg_value.strip()) > 0:
            raise ValueError("The {name} argument should be a non empty string "
                             "({name}: {value})".format(name=arg_type_defaults.arg_name, value=arg_value))

    # All other expected types (List[x] and Dict[x]) must have this attribute
    elif not hasattr(arg_type_defaults.type_, "__orig_bases__"):
        raise TypeError("Unknown type {} for {} argument".format(arg_type_defaults.type_, arg_type_defaults.arg_name))

    elif arg_type_defaults.type_.__orig_bases__[0] == list:
        return _validate_list(arg_value, arg_type_defaults)

    elif arg_type_defaults.type_.__orig_bases__[0] == dict:
        return _validate_dict(arg_value, arg_type_defaults)

    else:
        raise TypeError("Unknown type {} for argument {}".format(arg_type_defaults.type_, arg_type_defaults.arg_name))

    return arg_value


def _validate_list(arg_value: Any, arg_type_defaults: type_defaults.TypeDefaultBounds) -> Any:
    if not isinstance(arg_value, list):
        raise TypeError("The {name} argument should be a list "
                        "({name}: {value})".format(name=arg_type_defaults.arg_name, value=arg_value))

    # Get expected inner type of list
    inner_type = arg_type_defaults.type_.__args__[0]
    if inner_type not in [int, float, str, bool] and \
            (not hasattr(inner_type, "__orig_bases__") or inner_type.__orig_bases__[0] not in [list, dict]):
        raise TypeError("List arguments can only be List[int], List[float], List[str], List[bool], or a combination of "
                        "List of Lists/Dicts with those types "
                        "({}: {})".format(arg_type_defaults.arg_name, arg_type_defaults.type_))

    # Validate each element recursively
    el_name = "element of " + arg_type_defaults.arg_name + " list"

    if len(arg_value) == 0:
        raise TypeError("The {name} argument should be a list of {type_}, but it is an empty "
                        "list.".format(name=arg_type_defaults.arg_name, type_=inner_type))

    new_lst = []
    for el in arg_value:
        el_type_defaults = type_defaults.TypeDefaultBounds(el_name, inner_type, bound_obj=arg_type_defaults.bound_obj)
        new_lst.append(validate_argument(el, el_type_defaults))

    return new_lst


def _validate_dict(arg_value: Any, arg_type_defaults: type_defaults.TypeDefaultBounds) -> Any:
    if not isinstance(arg_value, dict):
        raise TypeError("The {name} argument should be a dict "
                        "({name}: {value})".format(name=arg_type_defaults.arg_name, value=arg_value))

    if not arg_type_defaults.type_.__args__[0] == str:
        raise TypeError("The keys for dictionaries must always be strings "
                        "({}: {})".format(arg_type_defaults.arg_name, arg_type_defaults.type_))

    # Get expected type of dictionary values
    inner_type = arg_type_defaults.type_.__args__[1]

    if inner_type not in [int, float, str, bool] and \
            (not hasattr(inner_type, "__orig_bases__") or inner_type.__orig_bases__[0] not in [list, dict]):
        raise TypeError("Dict arguments can only be Dict[str, int], Dict[str, float], Dict[str, str], Dict[str, bool], "
                        "or a combination of Dict of Lists/Dicts with those types "
                        "({}: {})".format(arg_type_defaults.arg_name, arg_type_defaults.type_))

    # Validate keys and elements recursively
    key_name = "key of " + arg_type_defaults.arg_name + " dictionary"
    el_name = "element of " + arg_type_defaults.arg_name + " dictionary with key "

    if len(arg_value) == 0:
        raise TypeError("The {name} argument should be a dict of {type_}, but it is an empty "
                        "dict.".format(name=arg_type_defaults.arg_name, type_=inner_type))

    new_dict = {}
    for key in arg_value:
        key_type_defaults = type_defaults.TypeDefaultBounds(key_name, str)
        el_type_defaults = type_defaults.TypeDefaultBounds(el_name + key, inner_type,
                                                           bound_obj=arg_type_defaults.bound_obj)
        validate_argument(key, key_type_defaults)
        new_dict[key] = validate_argument(arg_value[key], el_type_defaults)

    return new_dict
