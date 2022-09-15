import numpy as np
import pandas as pd


def get_avc_df(
    df: pd.DataFrame,
    column: str,
    groupby_col: str = None,
    dropna: bool = False,
    max_groups: int = None,
    min_group_ratio: float = 0,
    min_group_count: int = 1,
    max_subgroups: int = None,
    min_subgroup_ratio: float = 0,
    min_subgroup_count: int = 1,
    min_subgroup_ratio_vs_total: float = 0,
    round_ratio: int = None,
) -> pd.DataFrame:

    """
        Args:
        df (pd.DataFrame): the DataFrame to get advanced value counts from

        column (str): the name of the column where the values to count are in

        groupby_col (str, optional): the name of the column to apply the
        pd.DataFrame.groupby method to. Defaults to None

        dropna (bool, optional): if true, won't add counts for NA values.
        Defaults to False

        max_groups (int, optional): the maximum amount of groups of the
        groupby_col. The remaining groups will be grouped into one group
        called '_other'. Defaults to None.

        min_group_ratio (float, optional): the minimum ratio of the count a
        group of the groupby_col must have. Groups below the threshold will be
        grouped into one group called '_other'. Defaults to 0.

        min_group_count (int, optional): the minimum count a group of the
        groupby_col must have. Groups below the threshold will be grouped into
        one group called '_other'. Defaults to 1.

        max_subgroups (int, optional): the maximum amount of subgroups
        (based on column) per group (based on groupby_col). Remaining
        subgroups will be grouped into one subgroup called '_other'.
        Defaults to None.

        min_subgroup_ratio (float, optional): the minimum ratio of the count
        of a subgroup per group. Subgroups below the threshold will be grouped
        into one subgroup called '_other'. Defaults to 0.

        min_subgroup_count (int, optional): the minimum count of a subgroup
        per group. Subgroups below the threshold will be grouped into one
        subgroup called '_other'. Defaults to 0.

        min_subgroup_vs_total_ratio (float, optional): the minium ratio of a
        subgroup compared to the total count. Subgroups below the threshold
        will be grouped into one subgroup called '_other'. Defaults to 0.

        round_ratio (int, optional): the amount of decimals to round a ratio
        to. Defaults to None

    Returns:
        pd.DataFrame: a DataFrame with relative and absolute counts, plus
        extra summary statistics.
    """

    dfc = df.copy()

    # change the values of the main groups to '_other' if their ratio or
    # minimal count is too small
    if groupby_col:
        dfc[groupby_col] = group_uncommon_values(
            df=dfc,
            column=groupby_col,
            max_groups=max_groups,
            min_ratio=min_group_ratio,
            min_count=min_group_count,
            dropna=dropna,
        )
        dfc[column] = group_uncommon_values(
            df=dfc,
            column=column,
            min_ratio=min_subgroup_ratio_vs_total,
            min_count=min_subgroup_count,
            dropna=dropna,
        )
    else:
        dfc[column] = group_uncommon_values(
            df=dfc,
            column=column,
            max_groups=max_groups,
            min_ratio=min_group_ratio,
            min_count=min_group_count,
            dropna=dropna,
        )

    # replace na's with _na as a string
    if not dropna:
        dfc.loc[:, column] = dfc[column].fillna("_na")
        if groupby_col:
            dfc.loc[:, groupby_col] = dfc[groupby_col].fillna("_na")

    # get summary statistics, which means:
    # add a group '_all' for overall statistics, and
    # add '_total' as subgroup for subgroup statistics
    value_counts_df = add_summary_statistics(dfc, column, groupby_col)

    if groupby_col:
        # change the subgroups which are too small to '_other'
        value_counts_df[column] = group_uncommon_subgroups(
            value_counts_df=value_counts_df,
            column=column,
            max_subgroups=max_subgroups,
            min_subgroup_ratio=min_subgroup_ratio,
            min_subgroup_count=min_subgroup_count,
            min_subgroup_ratio_vs_total=min_subgroup_ratio_vs_total,
        )

    # if not groupby change the index name to the column for extra readability
    else:
        value_counts_df.index.name = column

    # change the count column to integers
    value_counts_df["count"] = value_counts_df["count"].astype(int)

    # round the ratio for visability if a number is set for round_ratio
    if round_ratio:
        value_counts_df["subgroup_ratio"] = value_counts_df[
            "subgroup_ratio"
        ].round(round_ratio)
        if groupby_col:
            value_counts_df["r_vs_total"] = value_counts_df[
                "r_vs_total"
            ].round(round_ratio)

    # groupby the two columns again to get the final DataFrame
    if groupby_col:
        value_counts_df = (
            value_counts_df.groupby([value_counts_df.index, column])
            .sum()
            .sort_index()
        )
        # return value_counts_df
        value_counts_df = add_subgroup_diff_vs_total(
            value_counts_df,
            col="subgroup_ratio",
            new_col="subgr_r_diff_subgr_all",
        )

        return value_counts_df.loc[
            :,
            [
                "count",
                "subgroup_ratio",
                "subgr_r_diff_subgr_all",
                "r_vs_total",
            ],
        ]

    else:
        return value_counts_df.sort_values("count", ascending=False)


def add_summary_statistics(
    df: pd.DataFrame, column: str, groupby_col: str
) -> pd.DataFrame:
    """Adds summary statistic of each subgroup and main group of a
    grouped-by DataFrame

    Args:
        df (pd.DataFrame): DataFrame to add the summary statistics to
        column (str): the column which will be turned into subgroups
        groupby_col (str): the column by which the DataFrame will be grouped by

    Returns:
        pd.DataFrame: DataFrame with summary statistics added
    """

    # perform two ungrouped value_counts
    rel_series = df[column].value_counts(normalize=True)
    count_series = df[column].value_counts()

    # perform  a value_counts on a groupby if a groupby column is specified
    if groupby_col:
        rel_series_grouped = df.groupby(groupby_col)[column].value_counts(
            normalize=True
        )
        count_series_grouped = df.groupby(groupby_col)[column].value_counts()

        # select the grouped value counts series to be concatenatd to a
        # single dataframe
        series_to_concat = [rel_series_grouped, count_series_grouped]
        keys = ("subgroup_ratio", "count")
    else:
        # select the ungrouped value counts series to be conconatenated to a
        # single dataframe
        series_to_concat = [rel_series, count_series]
        keys = ("ratio", "count")

    # concatenate the relative and the absolute series to
    # get a dataframe with both
    value_counts_df = pd.concat(
        series_to_concat, axis=1, keys=keys  # names of the columns
    )
    if groupby_col:

        # add the statistics of the ungrouped value counts, and add them to a
        # new group called '_all'
        for index in set(value_counts_df.index.get_level_values(column)):
            value_counts_df.loc[
                ("_all", index), "subgroup_ratio"
            ] = rel_series[index]
            value_counts_df.loc[("_all", index), "count"] = count_series[index]

        # add the statistics of the whole dataframe
        value_counts_df.loc[
            ("_all", "_total"), "subgroup_ratio"
        ] = 1  # ratio of all data = 1
        value_counts_df.loc[
            ("_all", "_total"), "count"
        ] = count_series.sum()  # total count

        # loop through the zero-level index, which defines the groups of the
        # groupby column
        for groupby_index in set(
            value_counts_df.index.get_level_values(groupby_col)
        ):

            # make sure the '_all' index, created above, isn't used
            if groupby_index != "_all":

                # total of a subgroup is always 1
                value_counts_df.loc[
                    (groupby_index, "_total"), "subgroup_ratio"
                ] = 1

                # add the absolute count for each group
                value_counts_df.loc[
                    (groupby_index, "_total"), "count"
                ] = value_counts_df.loc[groupby_index, "count"].sum()

    return value_counts_df


def group_uncommon_values(
    df: pd.DataFrame,
    column: str,
    max_groups: int = None,
    min_ratio: float = 0,
    min_count: int = 1,
    dropna: bool = False,
    uncommon_group_name: str = "_other",
):

    """Changes column values to a specified string (from uncommon_group_name)
    based on minimal conditions of its counts and maxium condition of amount
    of unique values

    Args:
        df (pd.DataFrame): the relevant pandas DataFrame

        column (str): the column name where the values are in

        max_groups (int, optional): the maximum amount of different values
        that are allowed. Defaults to None.

        min_ratio (float, optional): the minimal ratio a value must have.
        Defaults to 0.

        min_count (int, optional): the minimal count a value must have.
        Defaults to 1.

        uncommon_group_name (str, optional): value to change the uncommon
        group names to. Defaults to '_other'

    Returns:
        pd.Series: the pd.Series of the column of the df, with possibly some
        values changed to the value of uncommon_group_name
    """

    # get the value counts of the column
    value_counts = df[column].value_counts(dropna=dropna)
    value_counts.index = value_counts.index.fillna("_na")

    # make sure _na won't be dropped if dropna == False
    groups = [] if dropna else ["_na"]

    # make sure max_groups is not affected by _na, by increasing
    # max_groups by 1 if _na is in the n biggest groups with
    # n = max_groups
    if max_groups:
        max_groups = (
            max_groups
            if "_na" not in value_counts.head(max_groups).index
            else max_groups + 1
        )
    # determine the names of the groups that are allowed, based on if
    # max_groups is set or not
    groups += (
        value_counts.head(max_groups).index.tolist()
        if max_groups is not None
        else value_counts.index.tolist()
    )
    # get a truth value for when a value count is less than the minimal ratio
    # or less than the minimal count
    conditions = (
        (value_counts / value_counts.sum()).lt(min_ratio)
        | value_counts.lt(min_count)
        | ~value_counts.index.isin(groups)
    )

    # replace labels with uncommon_group_name if the count (ratio) is les
    # than the minimal count (ratio)
    return np.where(
        df[column].isin(value_counts[conditions].index),
        uncommon_group_name,
        df[column],
    )


def group_uncommon_subgroups(
    value_counts_df: pd.DataFrame,
    column: str,
    max_subgroups: int = None,
    min_subgroup_ratio: float = 0,
    min_subgroup_count: int = 1,
    min_subgroup_ratio_vs_total: float = 0,
):
    """Changes column values of uncommon subgroups of a grouped-by DataFrame
    based on the parameters to '_other'

    Args:
        value_counts_df (pd.DataFrame): a pd.DataFrame with columns
        'subgroup_ratio' and 'count'

        column (str): the column name with the subgroups of a
        grouped-by dataframe

        max_subgroups (int, optional): maximal amount of subgroups within a
        group. Defaults to None.

        min_subgroup_ratio (float, optional): minimal amount of ratio of a
        subgroup within a group. Defaults to 0.

        min_subgroup_count (int, optional): minimal amount of counts for a
        subgroup within a group. Defaults to 1.

        min_subgroup_ratio_vs_total (float, optional): minimal ratio for a
        subgroup compared to the entire DataFrame. Defaults to 0.

    Returns:
        pd.Series: the pd.Series of the column of the df, with possibly some
        values changed to '_other'
    """

    # get the total count
    total_count = np.max(value_counts_df["count"])

    # get the ratio vs total
    value_counts_df["r_vs_total"] = value_counts_df["count"] / total_count

    # reset the subgroup index column to easier change values
    value_counts_df.reset_index(level=column, inplace=True)

    # select allowed subgroups based on max_subgroups
    if max_subgroups:
        subgroups = (
            value_counts_df.loc[
                "_all", [column, "count"]
            ]  # select the column and count column of the _all group
            .sort_values(
                by="count", ascending=False
            )  # sort by count, descending
            .iloc[1 : max_subgroups + 1][column]
            .values
        )  # select the top columns, [1:max_subgroups+1] is due to the
        # _total subgroup

    # if max_subgroups is not set, all subgroups are allowed based
    # on max_subgroups
    else:
        subgroups = value_counts_df[column].unique()

    # set conditions for which the value should not be changed to '_other'
    min_subgroup_count_condition = (
        value_counts_df["count"] < min_subgroup_count
    ) | (value_counts_df["subgroup_ratio"] < min_subgroup_ratio)
    total_ratio_condition = (
        value_counts_df["r_vs_total"] < min_subgroup_ratio_vs_total
    )
    special_column_condition = ~value_counts_df[column].isin(["_na", "_total"])
    max_subgroup_condition = ~value_counts_df[column].isin(subgroups)
    not_index_all_condition = (
        value_counts_df.index.get_level_values(0) != "_all"
    )

    # change values to'_other' if the conditions following conditions are met:
    # if (the subgroup count OR the witihin group ratio are below thresholds
    # OR the ratio vs total is smaller than the threshold
    # OR the column is not allowed according to the max amount of subgroups)
    # AND if the column is not a special column
    # AND the column is not in the _all main group
    value_counts_df[column] = np.where(
        (
            min_subgroup_count_condition
            | total_ratio_condition
            | max_subgroup_condition
        )
        & special_column_condition
        & not_index_all_condition,
        "_other",
        value_counts_df[column],
    )

    # select all the subgroups names which are in the main groups
    # because those need to be retained in the _all main group
    subgroups_in_groups = set(value_counts_df.drop("_all")[column])

    # convert subgroups which are not in the main groups in the
    # _all group to _other
    return np.where(
        (value_counts_df.index == "_all")
        & (~value_counts_df[column].isin(subgroups_in_groups)),
        "_other",
        value_counts_df[column],
    )


def add_subgroup_diff_vs_total(
    df: pd.DataFrame, col: str, new_col: str
) -> pd.DataFrame:
    """Adds column with the difference between a column statistic of a subgroup
    in a group vs that subgroup overall.

    Args:
        df (pd.DataFrame): a pd.DataFrame to
        col (str): the column name to calculate the difference on
        new_col (str): name of the new column with the calculated differences

    Returns:
        pd.DataFrame: a modified copy of the inputted pd.DataFrame
    """
    dfc = df.copy()
    for index, _ in dfc.drop("_all").iterrows():
        dfc.loc[index, new_col] = (
            df.loc[index, col] - df.loc[("_all", index[1]), col]
        )
    return dfc
