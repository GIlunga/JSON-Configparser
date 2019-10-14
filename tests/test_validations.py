from typing import List, Dict, Tuple

import pytest

from json_configparser import validations
from json_configparser import type_defaults
from json_configparser import bounds


default_bool = type_defaults.TypeDefaultBounds("a", bool)
default_int = type_defaults.TypeDefaultBounds("a", int)
default_float = type_defaults.TypeDefaultBounds("a", float)
default_str = type_defaults.TypeDefaultBounds("a", str)
default_list_int = type_defaults.TypeDefaultBounds("a", List[int])
default_list_float = type_defaults.TypeDefaultBounds("a", List[float])
default_list_str = type_defaults.TypeDefaultBounds("a", List[str])
default_list_bool = type_defaults.TypeDefaultBounds("a", List[bool])
default_list_list_int = type_defaults.TypeDefaultBounds("a", List[List[int]])
default_list_dict = type_defaults.TypeDefaultBounds("a", List[Dict[str, int]])
default_dict_int = type_defaults.TypeDefaultBounds("a", Dict[str, int])
default_dict_float = type_defaults.TypeDefaultBounds("a", Dict[str, float])
default_dict_str = type_defaults.TypeDefaultBounds("a", Dict[str, str])
default_dict_bool = type_defaults.TypeDefaultBounds("a", Dict[str, bool])
default_dict_dict_int = type_defaults.TypeDefaultBounds("a", Dict[str, Dict[str, int]])
default_dict_list_int = type_defaults.TypeDefaultBounds("a", Dict[str, List[int]])
valid_bounds_obj = bounds.Bounds("a", lower_bound=0, upper_bound=10)
invalid_bounds_obj = bounds.Bounds("a", lower_bound=0, upper_bound=1)


@pytest.mark.parametrize("value_typedef", [(True, default_bool),
                                           (10, default_int),
                                           (10.5, default_float),
                                           ("abc", default_str),
                                           ([1, 2], default_list_int),
                                           ([1.5, 2.5], default_list_float),
                                           (["ab", "cd"], default_list_str),
                                           ([True, False], default_list_bool),
                                           ([[1, 2], [3, 4]], default_list_list_int),
                                           ([{"a": 1, "b": 2}, {"a": 5, "b": 4}], default_list_dict),
                                           ({"a": 1, "b": 2}, default_dict_int),
                                           ({"a": 1.5, "b": 2.5}, default_dict_float),
                                           ({"a": "a", "b": "b"}, default_dict_str),
                                           ({"a": True, "b": False}, default_dict_bool),
                                           ({"a": {"a": 1}, "b": {"b": 2}}, default_dict_dict_int),
                                           ({"a": [1, 2], "b": [3, 4]}, default_dict_list_int)])
def test_simple_valid_cases(value_typedef):
    value, typedef = value_typedef
    validations.validate_argument(value, typedef)


@pytest.mark.parametrize("value_typedef", [(5, type_defaults.TypeDefaultBounds("a", int, bound_obj=valid_bounds_obj)),
                                           (5.5, type_defaults.TypeDefaultBounds("a", float, bound_obj=valid_bounds_obj)),
                                           ([5, 5], type_defaults.TypeDefaultBounds("a", List[int], bound_obj=valid_bounds_obj)),
                                           ([[5, 5], [5, 5]], type_defaults.TypeDefaultBounds("a", List[List[int]], bound_obj=valid_bounds_obj)),
                                           ([5.5, 5.5], type_defaults.TypeDefaultBounds("a", List[float], bound_obj=valid_bounds_obj)),
                                           ([[5.5, 5.5], [5.5, 5.5]], type_defaults.TypeDefaultBounds("a", List[List[float]], bound_obj=valid_bounds_obj)),
                                           ({"a": 5, "b": 5}, type_defaults.TypeDefaultBounds("a", Dict[str, int], bound_obj=valid_bounds_obj)),
                                           ({"a": 5.5, "b": 5.5}, type_defaults.TypeDefaultBounds("a", Dict[str, float], bound_obj=valid_bounds_obj)),
                                           ([{"a": 5, "b": 5}, {"a": 5, "b": 5}], type_defaults.TypeDefaultBounds("a", List[Dict[str, int]], bound_obj=valid_bounds_obj)),
                                           ({"a": {"a": 5}, "b": {"b": 5}}, type_defaults.TypeDefaultBounds("a", Dict[str, Dict[str, int]], bound_obj=valid_bounds_obj)),
                                           ({"a": [5, 5], "b": [5, 5]}, type_defaults.TypeDefaultBounds("a", Dict[str, List[int]], bound_obj=valid_bounds_obj))])
def test_valid_with_bounds(value_typedef):
    value, typedef = value_typedef
    validations.validate_argument(value, typedef)


@pytest.mark.parametrize("value_typedef", [(True, type_defaults.TypeDefaultBounds("a", bool, has_default=True, default_value=True)),
                                           (10, type_defaults.TypeDefaultBounds("a", int, has_default=True, default_value=10)),
                                           (10.5, type_defaults.TypeDefaultBounds("a", float, has_default=True, default_value=10.5)),
                                           ("abc", type_defaults.TypeDefaultBounds("a", str, has_default=True, default_value="abc")),
                                           ([1, 2], type_defaults.TypeDefaultBounds("a", List[int], has_default=True, default_value=[1, 2])),
                                           ([1.5, 2.5], type_defaults.TypeDefaultBounds("a", List[float], has_default=True, default_value=[1.5, 2.5])),
                                           ([[1, 2], [1, 2]], type_defaults.TypeDefaultBounds("a", List[List[int]], has_default=True, default_value=[[1, 2], [1, 2]])),
                                           ([True, False], type_defaults.TypeDefaultBounds("a", List[bool], has_default=True, default_value=[True, False])),
                                           (["ab", "cd"], type_defaults.TypeDefaultBounds("a", List[str], has_default=True, default_value=["a", "b"])),
                                           ({"a": 1, "b": 2}, type_defaults.TypeDefaultBounds("a", Dict[str, int], has_default=True, default_value={"a": 1, "b": 2})),
                                           ({"a": 1.5, "b": 2.5}, type_defaults.TypeDefaultBounds("a", Dict[str, float], has_default=True, default_value={"a": 1.5, "b": 2.5})),
                                           ({"a": "a", "b": "b"}, type_defaults.TypeDefaultBounds("a", Dict[str, str], has_default=True, default_value={"a": "a", "b": "b"})),
                                           ({"a": True, "b": False}, type_defaults.TypeDefaultBounds("a", Dict[str, bool], has_default=True, default_value={"a": True, "b": False}))])
def test_valid_with_defaults(value_typedef):
    value, typedef = value_typedef
    validations.validate_argument(value, typedef)


@pytest.mark.parametrize("value_typedef", [(True, default_str),
                                           (10, default_float),
                                           (10.5, default_int),
                                           ("abc", default_bool),
                                           (5, default_list_int),
                                           ([1, 2], default_list_float),
                                           ([1.5, 2.5], default_list_int),
                                           (["ab", "cd"], default_list_bool),
                                           ([True, False], default_list_str),
                                           (5, default_dict_int),
                                           ({"a": 1, "b": 2}, default_dict_float),
                                           ({"a": 1.5, "b": 2.5}, default_dict_int),
                                           ({"a": "a", "b": "b"}, default_dict_bool),
                                           ({"a": True, "b": False}, default_dict_str)])
def test_simple_invalid_cases(value_typedef):
    value, typedef = value_typedef
    with pytest.raises(TypeError):
        validations.validate_argument(value, typedef)


@pytest.mark.parametrize("value_typedef", [(5, type_defaults.TypeDefaultBounds("a", int, bound_obj=invalid_bounds_obj)),
                                           (5.5, type_defaults.TypeDefaultBounds("a", float, bound_obj=invalid_bounds_obj)),
                                           ([5, 5], type_defaults.TypeDefaultBounds("a", List[int], bound_obj=invalid_bounds_obj)),
                                           ([[5, 5], [5, 5]], type_defaults.TypeDefaultBounds("a", List[List[int]], bound_obj=invalid_bounds_obj)),
                                           ([5.5, 5.5], type_defaults.TypeDefaultBounds("a", List[float], bound_obj=invalid_bounds_obj)),
                                           ({"a": 5, "b": 5}, type_defaults.TypeDefaultBounds("a", Dict[str, int], bound_obj=invalid_bounds_obj)),
                                           ([{"a": 5, "b": 5}, {"a": 5, "b": 5}], type_defaults.TypeDefaultBounds("a", List[Dict[str, int]], bound_obj=invalid_bounds_obj)),
                                           ({"a": 5.5, "b": 5.5}, type_defaults.TypeDefaultBounds("a", Dict[str, float], bound_obj=invalid_bounds_obj))])
def test_invalid_bounds(value_typedef):
    value, typedef = value_typedef
    with pytest.raises(ValueError):
        validations.validate_argument(value, typedef)


@pytest.mark.parametrize("value_typedef", [([], default_list_int),
                                           ([], default_list_float),
                                           ([], default_list_str),
                                           ([], default_list_bool),
                                           ([[]], default_list_list_int),
                                           ({}, default_dict_int),
                                           ({}, default_dict_float),
                                           ({}, default_dict_str),
                                           ({}, default_dict_bool),
                                           ([{}], default_list_dict),
                                           ("", default_str)])
def test_empty_values(value_typedef):
    value, typedef = value_typedef
    error = TypeError if value != "" else ValueError
    with pytest.raises(error):
        validations.validate_argument(value, typedef)


@pytest.mark.parametrize("value_typedef", [([1, 2.5], default_list_int),
                                           ([1, 2.5], default_list_float),
                                           ([[1, 2], [1.5, 2.5]], default_list_list_int),
                                           (["a", 2], default_str),
                                           ({"a": 1, "b": 2.5}, default_dict_int),
                                           ({"a": 1, "b": 2.5}, default_dict_float),
                                           ({"a": "1", "b": 2.5}, default_dict_str)])
def test_mixed_types(value_typedef):
    value, typedef = value_typedef
    with pytest.raises(TypeError):
        validations.validate_argument(value, typedef)


@pytest.mark.parametrize("value_typedef", [([1, 2], type_defaults.TypeDefaultBounds("a", list)),
                                           ([1, 2], type_defaults.TypeDefaultBounds("a", List)),
                                           ((1, 2), type_defaults.TypeDefaultBounds("a", tuple)),
                                           ((1, 2), type_defaults.TypeDefaultBounds("a", Tuple[int])),
                                           ({"a": 1}, type_defaults.TypeDefaultBounds("a", dict)),
                                           ({"a": 1}, type_defaults.TypeDefaultBounds("a", Dict)),
                                           ({1: 1}, type_defaults.TypeDefaultBounds("a", Dict[int, int])),
                                           (None, type_defaults.TypeDefaultBounds("a", None)),
                                           (default_int, type_defaults.TypeDefaultBounds("a", type_defaults.TypeDefaultBounds))])
def test_unknown_types(value_typedef):
    value, typedef = value_typedef
    with pytest.raises(TypeError):
        validations.validate_argument(value, typedef)


def test_float_value_int_arg():
    typedef = type_defaults.TypeDefaultBounds("a", int)

    validations.validate_argument(1.0, typedef)
