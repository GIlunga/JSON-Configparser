from typing import Any

from . import type_defaults


def validate_argument(arg_value: Any, arg_type_defaults: type_defaults.TypeDefaultBounds):
    if arg_type_defaults.type_ == bool:
        if not isinstance(arg_value, bool):
            raise TypeError("The {name} argument should be a boolean "
                            "({name}: {value})".format(name=arg_type_defaults.arg_name, value=arg_value))

    elif arg_type_defaults.type_ == int or arg_type_defaults.type_ == float:
        if not isinstance(arg_value, arg_type_defaults.type_):
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
        if not len(arg_value.strip()) > 0:
            raise ValueError("The {name} argument should be a non empty string "
                             "({name}: {value})".format(name=arg_type_defaults.arg_name, value=arg_value))

    # All other expected types (List[x] and Dict[x]) must have this attribute
    elif not hasattr(arg_type_defaults.type_, "__orig_bases__"):
        raise TypeError("Unknown type {} for {} argument".format(arg_type_defaults.type_, arg_type_defaults.arg_name))

    elif arg_type_defaults.type_.__orig_bases__[0] == list:
        _validate_list(arg_value, arg_type_defaults)

    elif arg_type_defaults.type_.__orig_bases__[0] == dict:
        _validate_dict(arg_value, arg_type_defaults)

    else:
        raise TypeError("Unknown type {} for argument {}".format(arg_type_defaults.type_, arg_type_defaults.arg_name))


def _validate_list(arg_value: Any, arg_type_defaults: type_defaults.TypeDefaultBounds):
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

    for el in arg_value:
        el_type_defaults = type_defaults.TypeDefaultBounds(el_name, inner_type, bound_obj=arg_type_defaults.bound_obj)
        validate_argument(el, el_type_defaults)


def _validate_dict(arg_value: Any, arg_type_defaults: type_defaults.TypeDefaultBounds):
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

    for key in arg_value:
        key_type_defaults = type_defaults.TypeDefaultBounds(key_name, str)
        el_type_defaults = type_defaults.TypeDefaultBounds(el_name + key, inner_type, bound_obj=arg_type_defaults.bound_obj)
        validate_argument(key, key_type_defaults)
        validate_argument(arg_value[key], el_type_defaults)