from types import NoneType

import numpy as np


def not_inf(value):
    if value == np.inf:
        raise ValueError("Value cannot be infinite")


def not_below_zero(value):
    if value < 0:
        raise ValueError("Value cannot be below 0")


def only_numbers(value):
    if not isinstance(value, (int, float)) or isinstance(value, bool):
        raise TypeError("Value must be a number")


def numbers_or_none(value):
    if not isinstance(value, (int, float, NoneType)) or isinstance(value, bool):
        raise TypeError("Value must be a number or None")


def check_if_ratio(value):
    if value < 0 or value > 1:
        raise ValueError("Value cannot be < 0 or > 1.")


class PositiveNumber:
    """Source: https://stackoverflow.com/questions/69570761/check-a-type-attribute-with-a-descriptor-and-a-decorator-get-takes-2-po"""

    def __set_name__(self, owner, name):
        self.private_name = "_" + name  # e.g. "_number"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        only_numbers(value)
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
        if not isinstance(value, NoneType):
            not_below_zero(value)
        setattr(obj, self.private_name, value)


class Ratio:
    def __set_name__(self, owner, name):
        self.private_name = "_" + name  # e.g. "_number"

    def __get__(self, obj, objtype=None):
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        only_numbers(value)
        check_if_ratio(value)
        setattr(obj, self.private_name, value)


def positive_number_dec(*attributes):
    def decorator(cls):
        attribute_dict = dict()
        for attr in attributes:
            attribute_dict[attr] = PositiveNumber()
        return type(cls.__name__, (cls,), attribute_dict)

    return decorator


def positive_number_or_none_dec(*attributes):
    def decorator(cls):
        attribute_dict = dict()
        for attr in attributes:
            attribute_dict[attr] = PositiveNumberOrNone()
        return type(cls.__name__, (cls,), attribute_dict)

    return decorator


def ratio_dec(*attributes):
    def decorator(cls):
        attribute_dict = dict()
        for attr in attributes:
            attribute_dict[attr] = Ratio()
        return type(cls.__name__, (cls,), attribute_dict)

    return decorator
