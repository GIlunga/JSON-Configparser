Welcome to JSON-Configparser's documentation!
=============================================

JSON-Configparser is a Python package which enables the usage of JSON files as configuration files which are validated.
The main goals of the package are avoiding having to write validation code several times and enabling the usage of JSON
files as configuration files.

The package allows parsing several different datatypes from a JSON file:

- integers
- floats
- strings
- booleans
- lists
- dictionaries (with string keys)
- lists/dictionaries of the other types

Besides validating datatypes, it also validates bounds and extra user-defined constraints.

For understanding how to use the package, please check the :doc:`getstarted` and :doc:`examples` pages.
The full API (both public and private) is in the :doc:`api` page.

The package is available on `PyPI <https://pypi.org/project/json-configparser/>`_ (currently supports Python 3.6 only).
To install the latest version, run the following command: :code:`pip install json-configparser`

.. toctree::
   :maxdepth: 2
   :hidden:

   getstarted
   examples
   api

