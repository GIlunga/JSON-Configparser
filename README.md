# JSON-Configparser
[![Build status](https://dev.azure.com/guiilunga/JSON-Configparser/_apis/build/status/GIlunga.JSON-Configparser)](https://dev.azure.com/guiilunga/JSON-Configparser/_build?definitionId=-1)
[![PyPI version fury.io](https://badge.fury.io/py/json-configparser.svg)](https://pypi.org/project/json-configparser/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://github.com/GIlunga/JSON-Configparser/blob/master/LICENSE)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/json-configparser.svg)](https://pypi.org/project/json-configparser/)
[![Documentation Status](https://readthedocs.org/projects/json-configparser/badge/?version=latest)](https://json-configparser.readthedocs.io/en/latest/?badge=latest)


This python package enables the usage of JSON files as configuration files that can be properly validated.

The examples folder contains examples of using this package.

## Main Features
- Parse several different datatypes from a JSON configuration file:
    - ints
    - floats
    - strings
    - booleans
    - lists
    - dictionaries
    - lists/dictionaries of all other types
- Define options, including their types, bounds, extra validations, and defaults
- Parse a configuration file, returning an object with attributes or a dictionary
- All types, bounds, and defaults are validated by the package
 
 Check the docs for help getting started: https://json-configparser.readthedocs.io/en/latest/getstarted.html.