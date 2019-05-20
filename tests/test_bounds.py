import json_configparser
import pytest

# Known valid values
valid_arg_name = "valid"
valid_lower_bound = 5
valid_lower_inclusive = True
valid_upper_bound = 15
valid_upper_inclusive = True


# Valid tests
@pytest.mark.parametrize("lbound", [None, valid_lower_bound])
@pytest.mark.parametrize("ubound", [None, valid_upper_bound])
def test_valid_cases_creation(lbound, ubound):
    bound = json_configparser.Bounds(valid_arg_name, lbound, valid_lower_inclusive, ubound,
                                     valid_upper_inclusive)
    bound.validate_value(10)


@pytest.mark.parametrize("bound_inclusive", [(5, 15, True, True), (6, 14, False, False)])
def test_valid_edge_cases(bound_inclusive):
    lbound, ubound, l_inclusive, u_inclusive = bound_inclusive

    bound = json_configparser.Bounds(valid_arg_name, lbound, l_inclusive, ubound,
                                     u_inclusive)
    bound.validate_value(10)


# Invalid tests
@pytest.mark.parametrize("value_bound_inclusive", [(5, 5, 15, False, False),
                                                   (15, 5, 15, False, False),
                                                   (4, 5, 15, True, True),
                                                   (16, 5, 15, True, True)])
def test_wrong_edge_cases(value_bound_inclusive):
    value, lbound, ubound, l_inclusive, u_inclusive = value_bound_inclusive

    bound = json_configparser.Bounds(valid_arg_name, lbound, l_inclusive, ubound,
                                     u_inclusive)
    with pytest.raises(ValueError):
        bound.validate_value(value)


@pytest.mark.parametrize("arg_name", [None, int, valid_arg_name])
@pytest.mark.parametrize("lower_bound", ["bad", True, valid_lower_bound])
@pytest.mark.parametrize("lower_inclusive", [None, int, valid_lower_inclusive])
@pytest.mark.parametrize("upper_bound", ["bad", True, valid_upper_bound])
@pytest.mark.parametrize("upper_inclusive", [None, int, valid_upper_inclusive])
def test_wrong_types(arg_name, lower_bound, lower_inclusive, upper_bound, upper_inclusive):
    # Avoid valid case
    if arg_name == valid_arg_name and lower_bound == valid_lower_bound and lower_inclusive and \
            upper_bound == valid_upper_bound and upper_inclusive:
        pass
    else:
        with pytest.raises(TypeError):
            json_configparser.Bounds(arg_name, lower_bound, lower_inclusive, upper_bound, upper_inclusive)


def test_whitespace_arg_name():
    with pytest.raises(ValueError):
        json_configparser.Bounds("   ", valid_lower_bound, valid_lower_inclusive, valid_upper_bound,
                                 valid_upper_inclusive)


def test_invalid_bound():
    with pytest.raises(ValueError):
        json_configparser.Bounds(valid_arg_name, 15, valid_lower_inclusive, 5, valid_upper_inclusive)


def test_equal_bound():
    with pytest.raises(ValueError):
        json_configparser.Bounds(valid_arg_name, 5, valid_lower_inclusive, 5, valid_upper_inclusive)
