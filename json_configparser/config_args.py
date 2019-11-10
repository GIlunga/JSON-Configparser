"""
Implements the ConfigArgs class which is the main class for parsing options classes, validating arguments, and parsing
a JSON file.
"""

import copy
import inspect
import json
from typing import List, Callable, Union, Dict, Any, Set

from . import bounds
from . import type_defaults
from . import validations


class ConfigArgs(object):
    """
    Parses the Arguments NamedTuple class to extract information about argument names, types, and defaults.
    Also holds information about Bounds and extra validations.

    The parse_json method can be used to parse a JSON file and validate it against the known information.
    """
    # TODO: Improve names
    def __init__(self, options_class: type, bounds_lst: Union[List[bounds.Bounds], None] = None,
                 extra_validations: Union[Callable, None] = None):
        """
        :param options_class: The NamedTuple class which defines all arguments, types, and defaults.
        :param bounds_lst: A list of Bounds objects, which defines bounds for arguments.
        :param extra_validations: A function which contains extra validations. Should receive a dictionary mapping from
                                  argument name to value and should return a dictionary of the same type.
        """
        self._validate_init_args(options_class, bounds_lst, extra_validations)

        self.options_class = options_class
        self.bounds_lst = bounds_lst
        self.extra_validations = extra_validations

        self.arg_names, self.type_default_bounds_dict = self._create_type_default_bounds_dict()

    @staticmethod
    def _validate_init_args(options_class: type, bounds_lst: Union[List[bounds.Bounds], None] = None,
                            extra_validations: Union[Callable, None] = None):
        # Cannot check if NamedTuple directly
        if not isinstance(options_class, type):
            raise TypeError("The options_class parameter should be the typing NamedTuple Class itself "
                            "(options_class: {})".format(options_class))
        if not hasattr(options_class, "__annotations__") or not hasattr(options_class, "_field_defaults") or \
                len(options_class.__annotations__) == 0:
            raise TypeError("The options_class parameter should be a subclass of the typing NamedTuple Class itself "
                            "(options_class: {})".format(options_class))

        if bounds_lst is not None:
            if not isinstance(bounds_lst, list):
                raise TypeError("The bounds_lst parameter should be None or a list of Bounds objects "
                                "(bounds_lst: {})".format(bounds_lst))
            if len(bounds_lst) > 0 and not all(isinstance(el, bounds.Bounds) for el in bounds_lst):
                raise TypeError("The bounds_lst parameter should be None or a list of Bounds objects "
                                "(bounds_lst: {})".format(bounds_lst))

        if extra_validations is not None:
            if not isinstance(extra_validations, Callable):
                raise TypeError("The extra_validations parameters should be None or a function of a single parameter "
                                "(extra_validations: {})".format(extra_validations))

            sig = inspect.signature(extra_validations)

            if not len(sig.parameters) == 1:
                raise ValueError("The extra_validations parameters should be a function of a single parameter "
                                 "(extra_validations parameters: {})".format(sig.parameters))

    def _create_type_default_bounds_dict(self) -> (Set[str], Dict[str, type_defaults.TypeDefaultBounds]):
        """
        Parses the provided Arguments class and creates a set of argument names and a dictionary holding information
        about the type, default, and bounds of all arguments.

        :return: The set of all argument names and a dictionary mapping from argument name to TypeDefaultBounds
                 instance.
        :raises ValueError: If a bound is specified for an unknown argument. Or if a default value is out of bounds.
        :raises TypeError: If a bound is specified for an invalid type. Or if an argument has an invalid type.
                           Or if the default value is of the wrong type.
        """
        arg_types_dict = self.options_class.__annotations__
        arg_names = set(arg_types_dict.keys())
        arg_bounds_dict = {}

        # Check if the Options have supported types
        self._check_supported_types(arg_types_dict)

        # Check bound names match with actual names in the class
        if self.bounds_lst is not None:
            for bound in self.bounds_lst:
                if bound.arg_name not in arg_names:
                    raise ValueError("Bound specified for unknown argument {}".format(bound.arg_name))
                elif not self._validate_can_have_bounds(arg_types_dict[bound.arg_name]):
                    raise TypeError("Bounds can only be defined for ints, floats, or Lists/Dicts of ints or floats "
                                    "({}: {})".format(bound.arg_name, arg_types_dict[bound.arg_name]))
                else:
                    arg_bounds_dict[bound.arg_name] = bound

        # Get the default values from the class and validate them
        arg_defaults_dict = self.options_class._field_defaults
        self._check_valid_default(arg_defaults_dict, arg_types_dict, arg_bounds_dict)

        arg_type_defaults_dict = {}
        for arg_name in arg_names:
            type_ = arg_types_dict[arg_name]
            if arg_name in arg_defaults_dict:
                default_value = arg_defaults_dict[arg_name]

                arg_type_defaults_dict[arg_name] = \
                    type_defaults.TypeDefaultBounds(arg_name, type_, has_default=True,
                                                    default_value=default_value,
                                                    bound_obj=arg_bounds_dict.get(arg_name, None))
            else:
                arg_type_defaults_dict[arg_name] = \
                    type_defaults.TypeDefaultBounds(arg_name, type_, bound_obj=arg_bounds_dict.get(arg_name, None))

        return arg_names, arg_type_defaults_dict

    @staticmethod
    def _check_supported_types(arg_types_dict: Dict[str, type]):
        """
        Check if the provided argument type is valid.
        Valid types are ints, floats, strs, bools, and lists/dicts of those types.

        :param arg_types_dict: Dictionary mapping from argument name to type.
        :raises TypeError: If the provided argument type is not supported.
        """
        for arg, type_ in arg_types_dict.items():
            actual_inner_type = type_
            while hasattr(actual_inner_type, "__origin__"):
                # Check list (v3.7) and typing.List (3.6)
                if actual_inner_type.__origin__ not in [list, dict, List, Dict]:
                    raise TypeError("The type of the {name} argument is not supported "
                                    "({name}: {type_})".format(name=arg, type_=type_))
                if actual_inner_type.__origin__ in [list, List]:
                    actual_inner_type = actual_inner_type.__args__[0]
                else:
                    # Check dictionary keys are strings
                    if actual_inner_type.__args__[0] != str:
                        raise TypeError("The type of the {name} argument is not supported "
                                        "({name}: {type_})".format(name=arg, type_=type_))

                    actual_inner_type = actual_inner_type.__args__[1]

            if actual_inner_type not in [bool, int, float, str]:
                raise TypeError("The type of the {name} argument is not supported "
                                "({name}: {type_})".format(name=arg, type_=type_))

    @staticmethod
    def _validate_can_have_bounds(type_: type) -> bool:
        """
        Validate if a specific type can have bounds.
        Valid types are integers, floats, and lists/dicts of those types.

        :param type_: The type to validate.
        :return: Boolean value indicating if the type can have bounds.
        """
        actual_inner_type = type_
        while hasattr(actual_inner_type, "__origin__"):
            # Already checked that it is a list or dict
            i = 0 if actual_inner_type.__origin__ in [list, List] else 1
            actual_inner_type = actual_inner_type.__args__[i]

        return actual_inner_type in [int, float]

    @staticmethod
    def _check_valid_default(arg_defaults_dict: Dict[str, Any], arg_types_dict: Dict[str, type],
                             arg_bounds_dict: Dict[str, bounds.Bounds]):
        """
        Checks if the provided default arguments are valid, considering the types and bounds.

        :param arg_defaults_dict: Dictionary mapping from argument name to default value.
        :param arg_types_dict: Dictionary mapping from argument name to type.
        :param arg_bounds_dict: Dictionary mapping from argument name to Bounds object.
        :raises ValueError: If the default value is out of bounds.
        :raises TypeError: If the default argument is of the wrong type (None is accepted for lists and dicts).
        """
        for arg_name, default_value in arg_defaults_dict.items():
            # Use the validations module to validate default has if it was the real value
            type_def = type_defaults.TypeDefaultBounds(arg_name, arg_types_dict[arg_name],
                                                       bound_obj=arg_bounds_dict.get(arg_name, None))
            try:
                validations.validate_argument(default_value, type_def)
            except ValueError:
                raise ValueError("Invalid default value for {name} argument with bound {bound} "
                                 "(default: {value})".format(name=arg_name, bound=arg_bounds_dict[arg_name],
                                                             value=default_value))
            except TypeError:
                # allow none or empty for lists and dicts
                if hasattr(arg_types_dict[arg_name], "__origin__"):
                    if default_value is None:
                        continue
                    elif arg_types_dict[arg_name].__origin__ in [list, List] and default_value == []:
                        continue
                    elif arg_types_dict[arg_name].__origin__ in [dict, Dict] and default_value == {}:
                        continue

                raise TypeError("Invalid type for default of the {} argument "
                                "(default value: {}, expected_type: {})".format(arg_name, default_value,
                                                                                arg_types_dict[arg_name]))

    # TODO: Implement 3.6+ version
    def parse_json(self, path_to_json: str, encoding: str = "utf-8") -> Dict[str, Any]:
        """
        Parses a JSON file, reads the arguments, validates them, and returns a dictionary with them.

        :param path_to_json: Path to JSON configuration file.
        :param encoding: The encoding to use when loading the JSON file.
        :return: A Dictionary mapping argument name to value.
        :raises ValueError: If an argument is an empty string, if an argument with no default is missing from the JSON,
                            or if the JSON contains an unknown argument.
        :raises TypeError: If an argument is of the wrong type.
        """
        with open(path_to_json, "r", encoding=encoding) as f:
            loaded_args = json.load(f)

        json_arg_names = set(loaded_args.keys())

        for arg_name in self.arg_names:
            if arg_name not in json_arg_names and not self.type_default_bounds_dict[arg_name].has_default:
                raise ValueError("Argument {} was not provided in the JSON file and no default "
                                 "was given".format(arg_name))

            elif arg_name in json_arg_names:
                json_arg_names.remove(arg_name)
                loaded_args[arg_name] = validations.validate_argument(loaded_args[arg_name],
                                                                      self.type_default_bounds_dict[arg_name])

        if len(json_arg_names) > 0:
            raise ValueError("Unknown arguments provided in the JSON file: {}".format(json_arg_names))

        # Check extra validations
        if self.extra_validations is not None:
            returned_args = self.extra_validations(copy.deepcopy(loaded_args))
            if returned_args is not None and isinstance(returned_args, dict):
                loaded_args = returned_args

        return loaded_args
