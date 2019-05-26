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

explicar melhor algumas coisas, falar do q e validado!

===================
Defining the Bounds
===================
.. code-block:: python

    from json_configparser import Bounds

    bounds = [Bounds("arg1", lower_bound=1),
              Bounds("arg3", upper_bound=2, upper_inclusive=True)]

explicar melhor algumas coisas

==============================
Defining the Extra Validations
==============================
.. code-block:: python

    def extra_validations(args):
        if all(args["arg4"].values()):
            raise ValueError("Not all values in the arg4 argument can be true!")

explicar melhor...

================
Parsing the JSON
================
.. code-block:: python

    from json_configparser import ConfigArgs

    def create_args_object(path_to_json: str):
        args_object = ConfigArgs(Arguments, bounds, extra_validations)
        dict_args = args_object.parse_json(path_to_json)
        return Arguments(**dict_args)

explicar melhor