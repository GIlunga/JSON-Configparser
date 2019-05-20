import inspect
import logging
import json
from typing import List, Callable, Union, Dict, Any

from . import bounds
from . import type_defaults
from . import validations


class ConfigArgs(object):
    def __init__(self, options_class: type, bounds_lst: Union[List[bounds.Bounds], None]=None,
                 extra_validations: Union[Callable, None]=None):
        self._validate_init_args(options_class, bounds_lst, extra_validations)

        self.options_class = options_class
        self.bounds_lst = bounds_lst
        self.extra_validations = extra_validations

        self.arg_names, self.type_default_bounds_dict = self._create_type_default_bounds_dict()

    @staticmethod
    def _validate_init_args(options_class: type, bounds_lst: Union[List[bounds.Bounds], None]=None,
                            extra_validations: Union[Callable, None]=None):
        # Cannot check if NamedTuple directly
        if not isinstance(options_class, type):
            raise TypeError("The options_class parameter should be the typing NamedTuple Class itself "
                            "(options_class: {})".format(options_class))
        if not hasattr(options_class, "__annotations__") or not hasattr(options_class, "_field_defaults") or \
                len(options_class.__annotations__) == 0:
            raise TypeError("The options_class parameter should be the typing NamedTuple Class itself "
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
                raise ValueError("The extra_validations parameters should be None or a function of a single parameter "
                                 "(extra_validations parameters: {})".format(sig.parameters))

    def _create_type_default_bounds_dict(self):
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
        for arg, type_ in arg_types_dict.items():
            actual_inner_type = type_
            while hasattr(actual_inner_type, "__orig_bases__"):
                if actual_inner_type.__orig_bases__[0] not in [list, dict]:
                    raise TypeError("The type of the {name} argument is not supported "
                                    "({name}: {type_})".format(name=arg, type_=type_))
                i = 0 if actual_inner_type.__orig_bases__[0] == list else 1
                actual_inner_type = actual_inner_type.__args__[i]

            if actual_inner_type not in [bool, int, float, str]:
                raise TypeError("The type of the {name} argument is not supported "
                                "({name}: {type_})".format(name=arg, type_=type_))

    @staticmethod
    def _validate_can_have_bounds(type_: type):
        actual_inner_type = type_
        while hasattr(actual_inner_type, "__orig_bases__"):
            # Already checked that it is a list or dict
            i = 0 if actual_inner_type.__orig_bases__[0] == list else 1
            actual_inner_type = actual_inner_type.__args__[i]

        return actual_inner_type in [int, float]

    @staticmethod
    def _check_valid_default(arg_defaults_dict: Dict[str, Any], arg_types_dict: Dict[str, type],
                             arg_bounds_dict: Dict[str, bounds.Bounds]):
        for arg_name, default_value in arg_defaults_dict.items():
            # Use the validations module to validate default has if it was the real value
            type_def = type_defaults.TypeDefaultBounds(arg_name, arg_types_dict[arg_name],
                                                       bound_obj=arg_bounds_dict.get(arg_name, None))
            try:
                validations.validate_argument(default_value, type_def)
            except ValueError:
                # Empty strings are ok
                if default_value == "":
                    continue
                else:
                    raise ValueError("Invalid default value for {name} argument with bound {bound} "
                                     "(default: {value})".format(name=arg_name, bound=arg_bounds_dict[arg_name],
                                                                 value=default_value))
            except TypeError:
                # allow none or empty for lists and dicts
                if hasattr(arg_types_dict[arg_name], "__orig_bases__"):
                    if default_value is None:
                        continue
                    elif arg_types_dict[arg_name].__orig_bases__[0] == list and default_value == []:
                        continue
                    elif arg_types_dict[arg_name].__orig_bases__[0] == dict and default_value == {}:
                        continue

                raise TypeError("Invalid type for default of the {} argument "
                                "(default value: {}, expected_type: {})".format(arg_name, default_value,
                                                                                arg_types_dict[arg_name]))

    def parse_json(self, path_to_json: str, encoding: str="utf-8") -> Dict[str, Any]:
        with open(path_to_json, "r", encoding=encoding) as f:
            loaded_args = json.load(f)

        for arg_name in self.arg_names:
            if arg_name not in loaded_args and not self.type_default_bounds_dict[arg_name].has_default:
                raise ValueError("Argument {} was not provided in the JSON file and no default "
                                 "was given".format(arg_name))

            elif arg_name in loaded_args:
                validations.validate_argument(loaded_args[arg_name], self.type_default_bounds_dict[arg_name])

        if len(loaded_args) != len(self.arg_names):
            for arg_name in loaded_args:
                if arg_name not in self.arg_names:
                    logging.warning("Unknown argument {}. Ignoring".format(arg_name))

        # Check extra validations
        if self.extra_validations is not None:
            self.extra_validations(loaded_args)

        return loaded_args
