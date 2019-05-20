# JSON-Configparser
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
    