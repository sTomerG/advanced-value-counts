import numpy as np
import pytest
from advanced_value_counts.avc import AdvancedValueCounts as AVC

from .config import COLUMN, DF


@pytest.mark.parametrize("max_groups, expected", [(0, 2), (1, 3),
                                                  (3, 5), (100, 17)])
def test_max_groups_happy(max_groups, expected):
    """Test happy flow for max_groups"""
    avc_df = AVC(df=DF, column=COLUMN, max_groups=max_groups).avc_df
    assert avc_df.index.nunique() == expected


@pytest.mark.parametrize(
    "max_groups, dropna, expected",
    [(0, True, 1), (1, True, 2), (3, True, 4), (100, True, 16)],
)
def test_max_groups_dropna_happy(max_groups, dropna, expected):
    """Test happy flow for max_groups with dropna=True"""
    avc_df = AVC(df=DF, column=COLUMN, max_groups=max_groups,
                 dropna=dropna).avc_df
    assert avc_df.index.nunique() == expected


@pytest.mark.parametrize("min_group_count", [0, 1, 20, 50, 100, 5000])
def test_min_group_count_happy(min_group_count):
    """Test happy flow of min_group_count"""
    avc_df = AVC(df=DF, column=COLUMN, min_group_count=min_group_count).avc_df

    # don't consider _na and _other as they are insensitive to
    # the min_group_count
    if "_na" in avc_df.index:
        avc_df.drop("_na", inplace=True)
    if "_other" in avc_df.index:
        avc_df.drop("_other", inplace=True)

    # if there is a count with more than the min_group_count, the value with
    # the least count should be higher than min_group_count
    if min_group_count <= avc_df["count"].max():
        assert avc_df["count"].min() >= min_group_count
    else:
        # there is no value with a count high enough, thus the result
        # should be nan
        assert np.isnan(avc_df["count"].min())


@pytest.mark.parametrize("min_group_ratio", [0.01, 0.05, 0.1, 0.25, 0.5, 1])
def test_min_group_ratio_happy(min_group_ratio):
    """Test happy flow of min_group_ratio"""
    avc_df = AVC(df=DF, column=COLUMN, min_group_ratio=min_group_ratio).avc_df

    # don't consider _na and _other as they are insensitive to
    # the min_group_ratio
    if "_na" in avc_df.index:
        avc_df.drop("_na", inplace=True)
    if "_other" in avc_df.index:
        avc_df.drop("_other", inplace=True)

    # if there is a ratio with more than the min_group_ratio, the value with
    # the least ratio should be higher than min_group_ratio
    if min_group_ratio <= avc_df["ratio"].max():
        assert avc_df["ratio"].min() >= min_group_ratio
    else:
        # there is no value with a ratio high enough, thus the result should
        # be nan
        assert np.isnan(avc_df["ratio"].min())


@pytest.mark.parametrize("dropna", [True])
def test_dropna_happy_true(dropna):
    """Test that dropna prevents na values"""
    avc_df = AVC(df=DF, column=COLUMN, dropna=dropna).avc_df
    with pytest.raises(KeyError):
        avc_df.loc["_na"]


@pytest.mark.parametrize("dropna", [False])
def test_dropna_happy_false(dropna):
    """Test that dropna=false shows na values as _na"""
    avc_df = AVC(df=DF, column=COLUMN, dropna=dropna).avc_df
    avc_df.loc["_na"]


def test_get_plot_happy():
    """Test whether a plot can be generated without error"""
    avc = AVC(df=DF, column=COLUMN)
    avc.get_plot()
