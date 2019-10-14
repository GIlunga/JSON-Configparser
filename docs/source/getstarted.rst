Get Started
===========
The JSON-Configparser package reads information from a NamedTuple class, which enumerates all arguments, their types,
and possibly their defaults too. Besides this the user can define bounds for each argument or other extra validations.

As a result, when reading a JSON file, the package returns a dictionary mapping argument name to value. Then, this
dictionary can be used to create an instance of the NamedTuple with the argument values. This instance is immutable
(since it is a tuple) and if the user has an IDE, then autocompletion and type checking work when using the object.

The following sections describe the steps of using the package.

======================
Defining the Arguments
======================
First, the arguments must be defined using the NamedTuple class:

.. code-block:: python

   from typing import NamedTuple

   class Arguments(NamedTuple):
       arg1: int
       arg2: str
       arg3: List[float]
       arg4: Dict[str, bool]
       arg5: bool = True

The *Arguments* class defines all arguments and is also a typed NamedTuple.
Each argument must have a type. Valid types are:

* :code:`bool`
* :code:`int`
* :code:`float`
* :code:`str`
* :code:`List[x]` where x is any other valid type, including lists and dictionaries
* :code:`Dict[str, x]` where x is any other valid type, including lists and dictionaries

There are certain exceptions during validation: 10.0 is an accepted value for integer arguments and 10 is accepted for
float arguments.

Besides types, defaults can also be defined (arg5 in the example is given a default value of True).
Every argument defined in the NamedTuple must be given a value in the JSON file, unless it is given a default value.
Default values are also type checked by the library. If a default value is given and a value is also found in the JSON,
then the value in the JSON is used.

===================
Defining the Bounds
===================
After defining the arguments class, the user can define bounds. Bounds can be defined for arguments of type
int, float, or Lists/Dicts of ints or floats.

.. code-block:: python

    from json_configparser import Bounds

    bounds = [Bounds("arg1", lower_bound=1),
              Bounds("arg3", upper_bound=2, upper_inclusive=True)]

Bound objects are created by defining the name of the argument (must match the class attribute name), the
lower_bound and/or upper_bound, and flags (lower_inclusive and upper_inclusive) indicating if the bound is inclusive or
exclusive (default is False, i.e., exclusive).

==============================
Defining the Extra Validations
==============================
Finally, besides checking types and defaults, additional user defined validations can be done.
The user can define a function which receives a dictionary object, mapping argument name to value.
Then, this function can perform checks and raise Errors if an argument is invalid.

.. code-block:: python

    def extra_validations(args):
        if all(args["arg4"].values()):
            raise ValueError("Not all values in the arg4 argument can be true!")

In this case arg4 is a dictionary of booleans which cannot be all True. When parsing the JSON, if all True values are given,
the ValueError will be thrown by the library.

This function should not change the values in the dictionary, only check them and raise Errors.

================
Parsing the JSON
================
The last step is to actually parse a JSON file.
To do this, you must first create a *ConfigArgs* object and pass it the *Arguments* class, the bounds list, and the
extra validations function defined earlier.
You can now directly invoke the *parse_json* method of the *ConfigArgs* instance and pass the path to a valid JSON.
If all goes well, this should return a dictionary mapping argument names to values.

Finally, you can instantiate the *Arguments* NamedTuple directly by passing the dictionary. Below is the recommended way of doing these steps.

.. code-block:: python

    from json_configparser import ConfigArgs

    def create_args_object(path_to_json: str):
        args_object = ConfigArgs(Arguments, bounds, extra_validations)
        dict_args = args_object.parse_json(path_to_json)
        return Arguments(**dict_args)

For further help, please see the Examples section, or open an issue on Github.