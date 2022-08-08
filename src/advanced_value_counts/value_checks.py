from typing import Any

import numpy as np


def not_inf(value: Any):
    """Makes sure a value is not infinite

    Args:
        value (Any): any value

    Raises:
        ValueError: if value == np.inf
    """
    if value == np.inf:
        raise ValueError("Value cannot be infinite")


def not_below_zero(value: Any):
    """Makes sure a value is not below zero

    Args:
        value (Any): any value

    Raises:
        ValueError: if value below zero
        TypeError: if value not a number
    """
    only_numbers(value)
    if value < 0:
        raise ValueError("Value cannot be below 0")


def only_numbers(value: Any):
    """Makes sure a value is a number

    Args:
        value (Any): any value

    Raises:
        TypeError: if value is not an int or float
    """
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError("Value must be a float or int")


def numbers_or_none(value: Any):
    """Makes sure a value is a number or None

    Args:
        value (Any): any value

    Raises:
        TypeError: if value not a int, float or NoneType
    """
    if value is not None:
        if not isinstance(value, (float, int)) or isinstance(value, bool):
            raise TypeError("Value must be a number or None")


def check_if_ratio(value: Any):
    """
    Checks whether a value is a ratio ( 0 <= value <= 1 )

    Args:
        value (Any): any value

    Raises:
        ValueError: _description_
    """
    only_numbers(value)
    if value < 0 or value > 1:
        raise ValueError("Value cannot be < 0 or > 1.")


class PositiveNumber:
    """Source: https://stackoverflow.com/questions/69570761/check-a-type-
    attribute-with-a-descriptor-and-a-decorator-get-takes-2-po"""

    def __set_name__(self, owner, name):
        self.private_name = "_" + name  # e.g. "_number"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        not_below_zero(value)
        not_inf(value)
        setattr(obj, self.private_name, value)


class PositiveNumberOrNone:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name  # e.g. "_number"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        numbers_or_none(value)
        not_inf(value)
        if value is not None:
            not_below_zero(value)
        setattr(obj, self.private_name, value)


class Ratio:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name  # e.g. "_number"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        check_if_ratio(value)
        setattr(obj, self.private_name, value)


def positive_number_dec(*attributes):
    """ Makes sure attributes can only be set to a positive number
    """
    def decorator(cls):
        attribute_dict = dict()
        for attr in attributes:
            attribute_dict[attr] = PositiveNumber()
        return type(cls.__name__, (cls,), attribute_dict)

    return decorator


def positive_number_or_none_dec(*attributes):
    """ Makes sure attributes can only be set to a positive number or None
    """
    def decorator(cls):
        attribute_dict = dict()
        for attr in attributes:
            attribute_dict[attr] = PositiveNumberOrNone()
        return type(cls.__name__, (cls,), attribute_dict)

    return decorator


def ratio_dec(*attributes):
    """ Makes sure attributes can only be set to a ratio ( >= 0 and <= 1)
    """
    def decorator(cls):
        attribute_dict = dict()
        for attr in attributes:
            attribute_dict[attr] = Ratio()
        return type(cls.__name__, (cls,), attribute_dict)

    return decorator
