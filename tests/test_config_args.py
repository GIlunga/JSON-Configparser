import pytest

import json_configparser
from .data import option_defs


valid_bounds_lst = [json_configparser.Bounds("a1", lower_bound=0, upper_bound=10),
                    json_configparser.Bounds("a2", lower_bound=0, upper_bound=10),
                    json_configparser.Bounds("a5", lower_bound=0, upper_bound=10),
                    json_configparser.Bounds("a6", lower_bound=0, upper_bound=10),
                    json_configparser.Bounds("a9", lower_bound=0, upper_bound=10),
                    json_configparser.Bounds("a10", lower_bound=0, upper_bound=10),
                    json_configparser.Bounds("a13", lower_bound=0, upper_bound=10),
                    json_configparser.Bounds("a14", lower_bound=0, upper_bound=10),
                    json_configparser.Bounds("a15", lower_bound=0, upper_bound=10),
                    json_configparser.Bounds("a16", lower_bound=0, upper_bound=10)]

valid_dict = {
    "a1": 5,
    "a2": 5.5,
    "a3": "abc",
    "a4": True,
    "a5": [5, 5],
    "a6": [5.5, 5.5],
    "a7": ["abc", "abc"],
    "a8": [True, False],
    "a9": {"a": 5, "b": 5},
    "a10": {"a": 5.5, "b": 5.5},
    "a11": {"a": "ab", "b": "bc"},
    "a12": {"a": True, "b": False},
    "a13": [[1, 2], [3, 4]],
    "a14": [{"a": 5, "b": 5}, {"a": 5, "b": 5}],
    "a15": {"a": {"a": 5, "b": 5}, "b": {"a": 5, "b": 5}},
    "a16": {"a": [1, 2], "b": [3, 4]}
}


@pytest.mark.parametrize("options_json", [(option_defs.OptionsOnly, "tests/data/valid.json")])
def test_valid_options_only(options_json):
    options_class, json = options_json

    args_object = json_configparser.ConfigArgs(options_class)
    args_dict = args_object.parse_json(json)
    result = options_class(**args_dict)

    assert args_dict == valid_dict
    assert result == option_defs.OptionsOnly(**valid_dict)


@pytest.mark.parametrize("options_json", [(option_defs.OptionsDefaults, "tests/data/empty.json"),
                                          (option_defs.OptionsDefaults, "tests/data/valid.json")])
def test_valid_options_defaults(options_json):
    options_class, json = options_json

    args_object = json_configparser.ConfigArgs(options_class)
    args_dict = args_object.parse_json(json)
    result = options_class(**args_dict)

    assert result == option_defs.OptionsDefaults(**valid_dict)


@pytest.mark.parametrize("options_json", [(option_defs.OptionsOnly, "tests/data/valid.json")])
def test_valid_options_bounds(options_json):
    options_class, json = options_json

    args_object = json_configparser.ConfigArgs(options_class, valid_bounds_lst)
    args_dict = args_object.parse_json(json)
    result = options_class(**args_dict)

    assert args_dict == valid_dict
    assert result == option_defs.OptionsOnly(**valid_dict)


@pytest.mark.parametrize("options_json", [(option_defs.OptionsDefaults, "tests/data/empty.json"),
                                          (option_defs.OptionsDefaults, "tests/data/valid.json")])
def test_valid_options_defaults_bounds(options_json):
    options_class, json = options_json

    args_object = json_configparser.ConfigArgs(options_class, valid_bounds_lst)
    args_dict = args_object.parse_json(json)
    result = options_class(**args_dict)

    assert result == option_defs.OptionsDefaults(**args_dict)


@pytest.mark.parametrize("options_json", [(option_defs.OptionsOnly, "tests/data/invalid.json")])
def test_valid_options_invalid_json(options_json):
    options_class, json = options_json
    args_object = json_configparser.ConfigArgs(options_class)

    with pytest.raises(TypeError):
        args_object.parse_json(json)


def test_unknown_json_args():
    args_object = json_configparser.ConfigArgs(option_defs.OptionsOnly)

    with pytest.raises(ValueError):
        args_object.parse_json("tests/data/unknown_args.json")
