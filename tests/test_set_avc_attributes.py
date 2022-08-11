from typing import Any, Tuple

import numpy as np
import pytest
from advanced_value_counts.avc import AdvancedValueCounts as AVC

from .config import COLUMN, DF


@pytest.mark.parametrize(
    "arguments",
    [
        ({"min_group_count": -1, "min_subgroup_count": -1}),
        ({"min_group_count": np.inf, "min_subgroup_count": np.inf}),
    ],
)
def test_positive_number_at_init_unhappy_value(arguments):
    """Tests unhappy flow for max_groups through negative value"""
    with pytest.raises(ValueError):
        AVC(df=DF, column=COLUMN, **arguments)


@pytest.mark.parametrize(
    "attribute, value",
    [
        ("min_group_count", -1),
        ("min_subgroup_count", -1),
        ("min_group_count", np.inf),
        ("min_subgroup_count", np.inf),
    ],
)
def test_set_positive_number_unhappy_value(attribute: str, value: Any):
    """Test unhappy flow for attributes that only can be a positive number

    Args:
        attribute (str): name of attribute
        value (Any): any value that is not a positive number
    """
    avc = AVC(df=DF, column=COLUMN)
    with pytest.raises(ValueError):
        setattr(avc, attribute, value)


@pytest.mark.parametrize(
    "arguments",
    [
        ({"max_groups": "1"}),
        ({"min_group_ratio": "1"}),
        ({"min_group_count": "1"}),
        ({"max_subgroups": "1"}),
        ({"min_subgroup_ratio": "1"}),
        ({"min_subgroup_count": "1"}),
        ({"min_subgroup_ratio_vs_total": "1"}),
        ({"round_ratio": "1"}),
        ({"max_groups": False}),
        ({"min_group_ratio": False}),
        ({"min_group_count": False}),
        ({"max_subgroups": False}),
        ({"min_subgroup_ratio": False}),
        ({"min_subgroup_count": False}),
        ({"min_subgroup_ratio_vs_total": False}),
        ({"round_ratio": False}),
    ],
)
def test_unhappy_types_at_init(arguments: Tuple[dict]):
    """Test whether unhappy types set at init raises a TypeError

    Args:
        arguments (Tuple[dict]): tuple containing a dict with
        {attribute: value}
    """
    with pytest.raises(TypeError):
        AVC(df=DF, column=COLUMN, **arguments)


@pytest.mark.parametrize(
    "attribute, value",
    [
        ("max_groups", "1"),
        ("min_group_ratio", "1"),
        ("min_group_count", "1"),
        ("max_subgroups", "1"),
        ("min_subgroup_ratio", "1"),
        ("min_subgroup_count", "1"),
        ("min_subgroup_ratio_vs_total", "1"),
        ("round_ratio", "1"),
        ("max_groups", False),
        ("min_group_ratio", False),
        ("min_group_count", False),
        ("max_subgroups", False),
        ("min_subgroup_ratio", False),
        ("min_subgroup_count", False),
        ("min_subgroup_ratio_vs_total", False),
        ("round_ratio", False),
    ],
)
def test_set_unhappy_types(attribute: str, value: Any):
    """Test whether setting unhappy types raises a TypeError

    Args:
        attribute (str): name of an unexisting attribute
        value (Any): any value
    """
    avc = AVC(df=DF, column=COLUMN)
    with pytest.raises(TypeError):
        setattr(avc, attribute, value)


@pytest.mark.parametrize(
    "attribute, value",
    [
        ("new_attribute", "text"),
        ("unexisting", 1),
        ("not_set", False),
    ],
)
def test_set_unexisting_attribute(attribute: str, value: Any):
    """Test whether setting an unexisting attribute rightously raises
    a UserWarning

    Args:
        attribute (str): name of an unexisting attribute
        value (Any): any value
    """
    avc = AVC(df=DF, column=COLUMN)
    with pytest.warns(UserWarning):
        setattr(avc, attribute, value)
