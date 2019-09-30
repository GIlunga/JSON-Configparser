from typing import NamedTuple, List, Dict
import json_configparser


class Options(NamedTuple):
    words: List[str]
    max_size: int = 2
    fail: bool = False
    translation: Dict[str, str] = {}


bounds = [json_configparser.Bounds("max_size", lower_bound=1)]


def extra_validations(args_dict):
    for word in args_dict["words"]:
        if word not in args_dict["translation"]:
            raise ValueError("Unknown word: {}".format(word))


def create_options_object(path_to_json):
    args_object = json_configparser.ConfigArgs(Options, bounds, extra_validations)
    dict_args = args_object.parse_json(path_to_json)
    return Options(**dict_args)

