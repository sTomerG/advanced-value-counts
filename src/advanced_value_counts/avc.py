from .helper_functions import (
    positive_number_dec,
    positive_number_or_none_dec,
    ratio_dec,
)
from .df_mutations import get_avc_df

from warnings import warn

import seaborn as sns
import pandas as pd
import numpy as np


@positive_number_dec("min_group_count", "min_subgroup_count")
@positive_number_or_none_dec("max_groups", "max_subgroups", "round_ratio")
@ratio_dec("min_group_ratio", "min_subgroup_ratio", "min_subgroup_ratio_vs_total")
class AdvancedValueCounts:
    def __init__(
        self,
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
    ):
        """
        Creates an AdvancedValueCounts class of a DataFrame based on different conditions, to be set through the parameters

         Args:
            df (pd.DataFrame): the DataFrame to apply AdvancedValueCounts to.
            column (str): the name of the column where the values to count are in.
            groupby_col (str, optional): the name of the column to apply the pd.DataFrame.groupby method to. Defaults to None.
            dropna (bool, optional): if true, won't add counts for NA values. Defaults to False.
            max_groups (int, optional): the maximum amount of groups of the groupby_col. The remaining groups will be grouped into one group called '_other'. Defaults to None.
            min_group_ratio (float, optional): the minimum ratio of the count a group of the groupby_col must have. Groups below the threshold will be grouped into one group called '_other'. Defaults to 0.
            min_group_count (int, optional): the minimum count a group of the groupby_col must have. Groups below the threshold will be grouped into one group called '_other'. Defaults to 1.
            max_subgroups (int, optional): the maximum amount of subgroups (based on column) per group (based on groupby_col). Remaining subgroups will be grouped into one subgroup called '_other'. Defaults to None.
            min_subgroup_ratio (float, optional): the minimum ratio of the count of a subgroup per group. Subgroups below the threshold will be grouped into one subgroup called '_other'. Defaults to 0.
            min_subgroup_count (int, optional): the minimum count of a subgroup per group. Subgroups below the threshold will be grouped into one subgroup called '_other'. Defaults to 0.
            min_subgroup_vs_total_ratio (float, optional): the minium ratio of a subgroup compared to the total count. Subgroups below the threshold will be grouped into one subgroup called '_other'. Defaults to 0.
            round_ratio (int, optional): the amount of decimals to round a ratio to. Defaults to None.

        Returns:
            pd.DataFrame: a DataFrame with relative and absolute counts, plus extra summary statistics.
        """
        self.df = df.copy()
        self.column = column
        self.groupby_col = groupby_col
        self.dropna = dropna
        self.max_groups = max_groups
        self.min_group_ratio = min_group_ratio
        self.min_group_count = min_group_count
        self.max_subgroups = max_subgroups
        self.min_subgroup_ratio = min_subgroup_ratio
        self.min_subgroup_count = min_subgroup_count
        self.min_subgroup_ratio_vs_total = min_subgroup_ratio_vs_total
        self.round_ratio = round_ratio

    @property
    def avc_df(self) -> pd.DataFrame:
        """Calls the function to do the actual calculations to get an AdvancedValueCounts DataFrame

        Returns:
            pd.DataFrame: a DataFrame with advanced value count statistics.
        """

        return get_avc_df(
            self.df,
            self.column,
            self.groupby_col,
            self.dropna,
            self.max_groups,
            self.min_group_ratio,
            self.min_group_count,
            self.max_subgroups,
            self.min_subgroup_ratio,
            self.min_subgroup_count,
            self.min_subgroup_ratio_vs_total,
            self.round_ratio,
        )

    @property
    def unsummerized_df(self) -> pd.DataFrame:
        if self.groupby_col:
            return self.avc_df.drop("_all", level=self.groupby_col).drop(
                "_total", level=self.column
            )
        else:
            warn(
                "No summary statistics are included in a non-groupedby AdvancedValueCounts. Same DataFrame returned."
            )
            return self.avc_df

    def __str__(self):
        return(
            f"""Settings:
              column: {self.column},
              groupby_col: {self.groupby_col}
              dropna: {self.dropna}
              max_groups: {self.max_groups}
              min_group_ratio: {self.min_group_ratio}
              min_group_count: {self.min_group_count}
              max_subgroups: {self.max_subgroups}
              min_subgroup_ratio: {self.min_subgroup_ratio}
              min_subgroup_count: {self.min_subgroup_count}
              min_subgroup_ratio_vs_total: {self.min_subgroup_ratio_vs_total} 
              round_ratio: {self.round_ratio}
              
              AdvancedValueCounts DataFrame:
              {self.avc_df}"""
        )

    def group_uncommon_subgroups(
        value_counts_df: pd.DataFrame,
        column: str,
        max_subgroups: int = None,
        min_subgroup_ratio: float = 0,
        min_subgroup_count: int = 1,
        min_subgroup_ratio_vs_total: float = 0,
    ):
        """Changes column values of uncommon subgroups of a grouped-by DataFrame based on the parameters to '_other'

        Args:
            value_counts_df (pd.DataFrame): a pd.DataFrame with columns 'subgroup_ratio' and 'count'
            column (str): the column name with the subgroups of a grouped-by dataframe
            max_subgroups (int, optional): maximal amount of subgroups within a group. Defaults to None.
            min_subgroup_ratio (float, optional): minimal amount of ratio of a subgroup within a group. Defaults to 0.
            min_subgroup_count (int, optional): minimal amount of counts for a subgroup within a group. Defaults to 1.
            min_subgroup_ratio_vs_total (float, optional): minimal ratio for a subgroup compared to the entire DataFrame. Defaults to 0.

        Returns:
            pd.Series: the pd.Series of the column of the df, with possibly some values changed to '_other'
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
                .sort_values(by="count", ascending=False)  # sort by count, descending
                .iloc[1 : max_subgroups + 1][column]
                .values
            )  # select the top columns, [1:max_subgroups+1] is due to the _total subgroup

        # if max_subgroups is not set, all subgroups are allowed based on max_subgroups
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

        # change values to'_other' if the conditions following conditions are met:
        # if (the subgroup count OR the witihin group ratio are smaller than the thresholds
        # OR the ratio vs total is smaller than the threshold
        # OR the column is not allowed according to the max amount of subgroups)
        # AND if the column is not a special column
        return np.where(
            (
                min_subgroup_count_condition
                | total_ratio_condition
                | max_subgroup_condition
            )
            & special_column_condition,
            "_other",
            value_counts_df[column],
        )

    def get_plot(self, normalize: bool = True):

        """Returns a bar plot with either relative of absolute counts

        Args:
            normalize (bool, optional): Use the normalized counts. Defaults to True.

        Returns:
            matplotlib.axes._subplots.AxesSubplot: the plot
        """

        if self.groupby_col:
            ax = self.get_grouped_count_plot(normalize)
        else:
            dfc = self.avc_df.copy()
            ax = sns.barplot(
                data=dfc,
                x="ratio" if normalize else "count",
                y=dfc.index,
                ci=None,
                orient="h",
            )
            return ax

    def get_grouped_count_plot(self, normalize: bool = True):

        """Returns a bar plot for the counts of a groupedby AdvancedValueCounts DataFrame

        Args:
            normalize (bool, optional): Use the normalized counts. Defaults to True.

        Returns:
            matplotlib.axes._subplots.AxesSubplot: the plot
        """
        dfc = self.avc_df.copy()
        # if not normalized, remove the _all group, as those will have high scores and zoom the plot too far out
        if not normalize:
            dfc.drop("_all", level=self.groupby_col, inplace=True)

        # drop the _total subgroups, as the ratio of them is always 1, and the count values will be high and zoom the plot out a lot
        dfc.drop("_total", level=self.column, inplace=True)

        # reset the index, which makes it easier to apply seaborn to it
        dfc.reset_index(inplace=True)

        # replace underscores because seaborn won't display those values
        dfc[self.column] = dfc[self.column].replace({"_na": ".na", "_other": ".other"})

        # set figsize larger because of the potentially many labels
        height = 10
        sns.set(rc={"figure.figsize": (20, height)})

        dfc = dfc.sort_values([self.groupby_col, self.column])

        # generate and return a countplot using seaborn
        ax = sns.barplot(
            data=dfc,
            x="subgroup_ratio" if normalize else "count",
            y=self.groupby_col,
            hue=self.column,
            hue_order=sorted(dfc[self.column].unique()),
            ci=None,
            orient="h",
        )
        return ax
