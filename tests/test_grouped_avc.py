from itertools import groupby
from typing import Any

import numpy as np
import pytest
from advanced_value_counts.avc import AdvancedValueCounts as AVC

from .config import COLUMN, DF, GROUPBY_COL


@pytest.mark.parametrize(
    "max_groups, expected", [(0, 3), (1, 4), (3, 6), (100, 10)]
)
def test_max_groups_happy(max_groups, expected):
    """Test happy flow for max_groups with dropna=False (default)"""
    avc_df = AVC(
        df=DF, column=COLUMN, groupby_col=GROUPBY_COL, max_groups=max_groups
    ).avc_df
    assert (
        avc_df.index.get_level_values(level=GROUPBY_COL).nunique() == expected
    )


@pytest.mark.parametrize(
    "max_groups, dropna, expected",
    [(0, True, 2), (1, True, 3), (3, True, 5), (100, True, 9)],
)
def test_max_groups_dropna_happy(max_groups, dropna, expected):
    """Test happy flow for max_groups with dropna=True"""
    avc_df = AVC(
        df=DF,
        column=COLUMN,
        groupby_col=GROUPBY_COL,
        max_groups=max_groups,
        dropna=dropna,
    ).avc_df
    assert (
        avc_df.index.get_level_values(level=GROUPBY_COL).nunique() == expected
    )


@pytest.mark.parametrize("min_group_count", [0, 1, 20, 49, 100, 5000])
def test_min_group_count_happy(min_group_count):
    """Test happy flow of min_group_count"""
    avc_df = AVC(
        df=DF,
        column=COLUMN,
        groupby_col=GROUPBY_COL,
        min_group_count=min_group_count,
    ).avc_df

    # don't consider _na and _other as they are
    # insensitive to the min_group_count
    avc_df = (
        avc_df
        .drop(["_other", "_na", "_all"], errors='ignore')
    )

    try:
        # select the counts from all the _total indices
        avc_counts = avc_df.loc[(slice(None), "_total"), "count"]

        # assert the minimal subgroup count (of the main group, because _total)
        # is larger than the minimal group count
        assert avc_counts.min() >= min_group_count

    # if _total wasn't found, a keyerror is raised, because no group had
    # enough of the minimal count. Therefore assert the avc_df is empty.
    except KeyError:
        assert avc_df.empty


@pytest.mark.parametrize("min_group_ratio", [0.01, 0.05, 0.1, 0.25, 0.5, 1])
def test_min_group_ratio_happy(min_group_ratio):
    """Test happy flow of min_group_ratio"""
    avc_df = AVC(
        df=DF,
        column=COLUMN,
        groupby_col=GROUPBY_COL,
        min_group_ratio=min_group_ratio,
    ).avc_df

    # don't consider _na and _other as they are insensitive to
    # the min_group_ratio
    avc_df = (
        avc_df
        .drop(["_na", "_other", "_all"], errors='ignore')
    )

    try:
        # select the subgroup ratios from all the _total indices
        avc_ratios = avc_df.loc[(slice(None), "_total"), "r_vs_total"]

        # assert the minimal subgroup ratio (of the main group, because _total)
        # is larger than the minimal group ratio
        assert avc_ratios.min() >= min_group_ratio

    # if _total wasn't found, a keyerror is raised, because no group had
    # enough of the minimal count. Therefore assert the avc_df is empty.
    except KeyError:
        assert avc_df.empty


@pytest.mark.parametrize("min_subgroup_count", [0, 1, 20, 49, 100, 5000])
def test_min_subgroup_count_happy(min_subgroup_count):
    avc_df = AVC(
        df=DF,
        column=COLUMN,
        groupby_col=GROUPBY_COL,
        min_subgroup_count=min_subgroup_count,
    ).avc_df

    # remove _other and _na from index as they are insensitive to
    # min_subgroup_count
    avc_df = (
        avc_df
        .drop(["_other", "_na", "_total"], level=COLUMN, errors='ignore')
    )

    if min_subgroup_count <= avc_df["count"].max():
        assert avc_df["count"].min() >= min_subgroup_count
    else:
        # there is no value with a count high enough, thus the result
        # should be nan
        assert np.isnan(avc_df["count"].min())


@pytest.mark.parametrize("min_subgroup_ratio", [0.01, 0.05, 0.1, 0.25, 0.5, 1])
def test_min_subgroup_ratio_happy(min_subgroup_ratio):
    avc_df = AVC(
        df=DF,
        column=COLUMN,
        groupby_col=GROUPBY_COL,
        min_subgroup_ratio=min_subgroup_ratio,
    ).avc_df

    # remove _other and _na from index as they are
    # insensitive to min_subgroup_count
    avc_df = (
        avc_df
        .drop(['_other', "_na", "_total"], level=COLUMN, errors='ignore')
        .drop(['_all'], level=GROUPBY_COL, errors='ignore')
    )

    if min_subgroup_ratio <= avc_df["subgroup_ratio"].max():
        assert avc_df["subgroup_ratio"].min() >= min_subgroup_ratio
    else:
        # there is no value with a count high enough, thus the result should
        # be nan
        assert np.isnan(avc_df["subgroup_ratio"].min())


@pytest.mark.parametrize(
    "min_subgroup_ratio_vs_total", [0.01, 0.05, 0.1, 0.25, 0.5, 1]
)
def test_min_subgroup_ratio_vs_total_happy(min_subgroup_ratio_vs_total):
    avc_df = AVC(
        df=DF,
        column=COLUMN,
        groupby_col=GROUPBY_COL,
        min_subgroup_ratio_vs_total=min_subgroup_ratio_vs_total,
    ).avc_df

    # remove _other and _na from index as they are insensitive to
    # min_subgroup_count
    avc_df = (
        avc_df
        .drop(["_other", "_na", "_total"], level=COLUMN, errors='ignore')
    )

    if min_subgroup_ratio_vs_total <= avc_df["r_vs_total"].max():
        assert avc_df["r_vs_total"].min() >= min_subgroup_ratio_vs_total
    else:
        # there is no value with a count high enough, thus the result should
        # be nan
        assert np.isnan(avc_df["r_vs_total"].min())


@pytest.mark.parametrize("dropna", [True])
def test_dropna_happy_true(dropna):
    """Test that dropna prevents na values"""
    avc_df = AVC(
        df=DF, column=COLUMN, groupby_col=GROUPBY_COL, dropna=dropna
    ).avc_df
    with pytest.raises(KeyError):
        avc_df.loc["_na"]


@pytest.mark.parametrize("dropna", [True])
def test_grouped_dropna_true_happy(dropna):
    """Test that dropna prevents na values"""
    avc_df = AVC(
        df=DF, column=COLUMN, groupby_col=GROUPBY_COL, dropna=dropna
    ).avc_df
    with pytest.raises(KeyError):
        avc_df.loc[(slice(None), "_na"), :]


@pytest.mark.parametrize("dropna", [False])
def test_dropna_false_happy(dropna):
    """Test that dropna=false shows na values as _na"""
    avc_df = AVC(
        df=DF, column=COLUMN, groupby_col=GROUPBY_COL, dropna=dropna
    ).avc_df
    avc_df.loc["_na"]


@pytest.mark.parametrize("dropna", [False])
def test_grouped_dropna_false_happy(dropna):
    """Test that dropna=false shows na values as _na"""
    avc_df = AVC(
        df=DF, column=COLUMN, groupby_col=GROUPBY_COL, dropna=dropna
    ).avc_df
    avc_df.loc[(slice(None), "_na"), :]
    
@pytest.mark.parametrize(
    "attribute, value",
    [
        ("max_groups", 3),
        ("min_group_ratio", 0.1),
        ("min_group_count", 5),
        ("max_subgroups", 5),
        ("min_subgroup_ratio", 0.2),
        ("min_subgroup_count", 3),
        ("min_subgroup_ratio_vs_total", 0.02),
    ],
)
def test_all_subgroups_in_all(attribute: str, value: Any):
    """Test whether all subgroups in main groups are in
    the subgroups of _all"""
    avc = AVC(df=DF, column=COLUMN, groupby_col=GROUPBY_COL)
    setattr(avc, attribute, value)
    avc_df = avc.avc_df
    subgroups = set(
        avc_df
        .drop('_all', level=0)
        .index
        .get_level_values(1)
    )
    subgroups_in_all = set(
        avc_df
        .loc['_all']
        .index
        .values
    )
    assert subgroups == subgroups_in_all

def test_grouped_get_plot_happy():
    """Test whether a plot can be generated without error"""
    avc = AVC(df=DF, column=COLUMN, groupby_col=GROUPBY_COL)
    avc.get_plot()


def test_grouped_unsummerized_df_happpy():
    """Test whether a DataFrame without summerized statistics
    is returned"""
    avc = AVC(df=DF, column=COLUMN, groupby_col=GROUPBY_COL)
    df = avc.unsummerized_df
    assert "_all" not in df.index and "_total" not in df.index

