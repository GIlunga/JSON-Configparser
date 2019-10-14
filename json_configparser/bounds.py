"""
The Bounds module implements the Bounds class, which can be used to represent bounds for certain arguments.
"""

from typing import Union


class Bounds(object):
    """
    Represents the Bounds of an argument.
    A Bounds instance is defined by lower and upper bounds, and flags indicating if the bounds are inclusive or
    exclusive.
    The supported argument types are integer, float, or lists/dictionaries of those types.
    """
    # TODO: The validation that the argument type supports Bounds should be done in the __init__
    def __init__(self, arg_name: str, lower_bound: Union[int, float, None]=None, lower_inclusive: bool=True,
                 upper_bound: Union[int, float, None]=None, upper_inclusive: bool=True):
        """
        At least one bound must be provided.

        :param arg_name: The name of the argument.
        :param lower_bound: The lower bound value.
        :param lower_inclusive: Flag indicating if the lower bound is inclusive.
        :param upper_bound: The upper bound value.
        :param upper_inclusive: Flag indicating if the lower bound is inclusive.
        """
        self._validate_init_args(arg_name, lower_bound, lower_inclusive, upper_bound, upper_inclusive)

        self.arg_name = arg_name
        self.lower_bound = lower_bound
        self.lower_inclusive = lower_inclusive
        self.upper_bound = upper_bound
        self.upper_inclusive = upper_inclusive

    @staticmethod
    def _validate_init_args(arg_name: str, lower_bound: Union[int, float, None], lower_inclusive: bool,
                            upper_bound: Union[int, float, None], upper_inclusive: bool):

        if not isinstance(arg_name, str):
            raise TypeError("The arg_name parameter should be a string "
                            "(arg_name: {})".format(arg_name))
        if len(arg_name.strip()) == 0:
            raise ValueError("The arg_name parameter should be a non-empty string "
                             "(arg_name: {})".format(arg_name))

        if lower_bound is not None and type(lower_bound) not in [int, float]:
            raise TypeError("The lower_bound parameter should be an integer, float, or None "
                            "(lower_bound: {}".format(lower_bound))
        if upper_bound is not None and type(upper_bound) not in [int, float]:
            raise TypeError("The upper_bound parameter should be an integer, float, or None "
                            "(upper_bound: {}".format(upper_bound))

        if not isinstance(lower_inclusive, bool):
            raise TypeError("The lower_inclusive parameter should be a boolean value "
                            "(lower_inclusive: {})".format(lower_inclusive))

        if not isinstance(upper_inclusive, bool):
            raise TypeError("The upper_inclusive parameter should be a boolean value "
                            "(upper_inclusive: {})".format(upper_inclusive))

        if lower_bound is not None and upper_bound is not None and lower_bound >= upper_bound:
            raise ValueError("The lower_bound parameter should be less than the upper_bound parameter "
                             "(lower_bound: {}, upper_bound: {})".format(lower_bound, upper_bound))

    def validate_value(self, arg_value: Union[int, float]):
        """
        Validates a value against the provided bounds.

        :param arg_value: The value of the argument to validate.
        :raises ValueError: If the value is out of bounds.
        """
        if self.lower_bound is not None:
            if self.lower_inclusive and arg_value < self.lower_bound:
                raise ValueError("The {name} argument should be greater than or "
                                 "equal to {lbound} ({name}: {value})".format(name=self.arg_name,
                                                                              lbound=self.lower_bound,
                                                                              value=arg_value))
            if not self.lower_inclusive and arg_value <= self.lower_bound:
                raise ValueError("The {name} argument should be greater than "
                                 "{lbound} ({name}: {value})".format(name=self.arg_name,
                                                                     lbound=self.lower_bound,
                                                                     value=arg_value))

        if self.upper_bound is not None:
            if self.upper_inclusive and arg_value > self.upper_bound:
                raise ValueError("The {name} argument should be less than or "
                                 "equal to {ubound} ({name}: {value})".format(name=self.arg_name,
                                                                              ubound=self.upper_bound,
                                                                              value=arg_value))
            if not self.upper_inclusive and arg_value >= self.upper_bound:
                raise ValueError("The {name} argument should be less than "
                                 "{ubound} ({name}: {value})".format(name=self.arg_name,
                                                                     ubound=self.upper_bound,
                                                                     value=arg_value))

    def __str__(self):
        start = "[" if self.lower_inclusive else "]"
        end = "]" if self.upper_inclusive else "["
        return start + str(self.lower_bound) + ", " + str(self.upper_bound) + end
