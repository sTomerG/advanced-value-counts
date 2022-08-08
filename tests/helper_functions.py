import pandas as pd


def remove_from_index(
    df: pd.DataFrame, indices_to_remove: tuple, level: int = 0
) -> pd.DataFrame:
    """Checks whether indices are present in a pandas DataFrame,
    and if so, deletes them

    Args:
        df (pd.DataFrame): the dataframe to remove indices from
        indices_to_remove (tuple): a tuple of indices to remove
        level (int): the level of the index to drop the indices from

    Returns:
        pd.DataFrame: The DataFrame without the indices_to_remove removed.
    """
    dfc = df.copy()
    for ind in indices_to_remove:
        if ind in dfc.index.get_level_values(level=level):
            dfc.drop(ind, level=level, inplace=True)
    return dfc
