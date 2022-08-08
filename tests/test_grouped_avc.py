import numpy as np
import pytest
from advanced_value_counts.avc import AdvancedValueCounts as AVC

from .config import COLUMN, DF, GROUPBY_COL
from .helper_functions import remove_from_index


@pytest.mark.parametrize("max_groups, expected", [(0, 3), (1, 4), (3, 6),
                                                  (100, 10)])
def test_max_groups_happy(max_groups, expected):
    """Test happy flow for max_groups with dropna=False (default)"""
    avc_df = AVC(
        df=DF, column=COLUMN, groupby_col=GROUPBY_COL, max_groups=max_groups
    ).avc_df
    assert avc_df.index.get_level_values(level=GROUPBY_COL) \
        .nunique() == expected


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
    assert avc_df.index.get_level_values(level=GROUPBY_COL) \
        .nunique() == expected


@pytest.mark.parametrize("min_group_count", [0, 1, 20, 49, 100, 5000])
def test_min_group_count_happy(min_group_count):
    """Test happy flow of min_group_count"""
    avc = AVC(
        df=DF, column=COLUMN, groupby_col=GROUPBY_COL,
        min_group_count=min_group_count
    ).avc_df

    # don't consider _na and _other as they are
    # insensitive to the min_group_count
    avc = remove_from_index(avc, ("_na", "_other", "_all"))

    try:
        # select the counts from all the _total indices
        avc_counts = avc.loc[(slice(None), "_total"), "count"]

        # assert the minimal subgroup count (of the main group, because _total)
        # is larger than the minimal group count
        assert avc_counts.min() >= min_group_count

    # if _total wasn't found, a keyerror is raised, because no group had
    # enough of the minimal count. Therefore assert the avc is empty.
    except KeyError:
        assert avc.empty


@pytest.mark.parametrize("min_group_ratio", [0.01, 0.05, 0.1, 0.25, 0.5, 1])
def test_min_group_ratio_happy(min_group_ratio):
    """Test happy flow of min_group_ratio"""
    avc = AVC(
        df=DF, column=COLUMN, groupby_col=GROUPBY_COL,
        min_group_ratio=min_group_ratio
    ).avc_df

    # don't consider _na and _other as they are insensitive to
    # the min_group_ratio
    avc = remove_from_index(avc, ("_na", "_other", "_all"))

    try:
        # select the subgroup ratios from all the _total indices
        avc_ratios = avc.loc[(slice(None), "_total"), "subgroup_ratio"]

        # assert the minimal subgroup ratio (of the main group, because _total)
        # is larger than the minimal group ratio
        assert avc_ratios.min() >= min_group_ratio

    # if _total wasn't found, a keyerror is raised, because no group had
    # enough of the minimal count. Therefore assert the avc is empty.
    except KeyError:
        assert avc.empty


@pytest.mark.parametrize("min_subgroup_count", [0, 1, 20, 49, 100, 5000])
def test_min_subgroup_count_happy(min_subgroup_count):
    avc = AVC(
        df=DF,
        column=COLUMN,
        groupby_col=GROUPBY_COL,
        min_subgroup_count=min_subgroup_count,
    ).avc_df

    # remove _other and _na from index as they are insensitive to
    # min_subgroup_count
    avc = remove_from_index(avc, ("_other", "_na", "_total"), level=COLUMN)

    if min_subgroup_count <= avc["count"].max():
        assert avc["count"].min() >= min_subgroup_count
    else:
        # there is no value with a count high enough, thus the result
        # should be nan
        assert np.isnan(avc["count"].min())


@pytest.mark.parametrize("min_subgroup_ratio", [0.01, 0.05, 0.1, 0.25, 0.5, 1])
def test_min_subgroup_ratio_happy(min_subgroup_ratio):
    avc = AVC(
        df=DF,
        column=COLUMN,
        groupby_col=GROUPBY_COL,
        min_subgroup_ratio=min_subgroup_ratio,
    ).avc_df

    # remove _other and _na from index as they are
    # insensitive to min_subgroup_count
    avc = remove_from_index(avc, ("_other", "_na", "_total"), level=COLUMN)

    if min_subgroup_ratio <= avc["subgroup_ratio"].max():
        assert avc["subgroup_ratio"].min() >= min_subgroup_ratio
    else:
        # there is no value with a count high enough, thus the result should
        # be nan
        assert np.isnan(avc["subgroup_ratio"].min())


@pytest.mark.parametrize("min_subgroup_ratio_vs_total", [0.01, 0.05, 0.1,
                                                         0.25, 0.5, 1])
def test_min_subgroup_ratio_vs_total_happy(min_subgroup_ratio_vs_total):
    avc = AVC(
        df=DF,
        column=COLUMN,
        groupby_col=GROUPBY_COL,
        min_subgroup_ratio_vs_total=min_subgroup_ratio_vs_total,
    ).avc_df

    # remove _other and _na from index as they are insensitive to
    # min_subgroup_count
    avc = remove_from_index(avc, ("_other", "_na", "_total"), level=COLUMN)

    if min_subgroup_ratio_vs_total <= avc["r_vs_total"].max():
        assert avc["r_vs_total"].min() >= min_subgroup_ratio_vs_total
    else:
        # there is no value with a count high enough, thus the result should
        # be nan
        assert np.isnan(avc["r_vs_total"].min())


@pytest.mark.parametrize("dropna", [True])
def test_dropna_happy_true(dropna):
    """Test that dropna prevents na values"""
    avc = AVC(df=DF, column=COLUMN, groupby_col=GROUPBY_COL,
              dropna=dropna).avc_df
    with pytest.raises(KeyError):
        avc.loc["_na"]


@pytest.mark.parametrize("dropna", [True])
def test_grouped_dropna_true_happy(dropna):
    """Test that dropna prevents na values"""
    avc = AVC(df=DF, column=COLUMN, groupby_col=GROUPBY_COL,
              dropna=dropna).avc_df
    with pytest.raises(KeyError):
        avc.loc[(slice(None), "_na"), :]


@pytest.mark.parametrize("dropna", [False])
def test_dropna_false_happy(dropna):
    """Test that dropna=false shows na values as _na"""
    avc = AVC(df=DF, column=COLUMN, groupby_col=GROUPBY_COL,
              dropna=dropna).avc_df
    avc.loc["_na"]


@pytest.mark.parametrize("dropna", [False])
def test_grouped_dropna_false_happy(dropna):
    """Test that dropna=false shows na values as _na"""
    avc = AVC(df=DF, column=COLUMN, groupby_col=GROUPBY_COL,
              dropna=dropna).avc_df
    avc.loc[(slice(None), "_na"), :]


def test_grouped_get_plot_happy():
    """Test whether a plot can be generated without error"""
    avc = AVC(df=DF, column=COLUMN, groupby_col=GROUPBY_COL)
    avc.get_plot()


def test_grouped_unsummerized_df_happpy():
    """Test whether a DataFrame without summerized statistics
    is returned"""
    avc = AVC(df=DF, column=COLUMN, groupby_col=GROUPBY_COL)
    df = avc.unsummerized_df
    assert '_all' not in df.index and '_total' not in df.index
