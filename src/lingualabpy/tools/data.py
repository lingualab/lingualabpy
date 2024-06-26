from collections import UserDict
from pandas import DataFrame

from typing import Any, Dict, List


class UnchangeableDict(UserDict):
    """A dictionary in which you can add new keys but not modify them in the future."""

    def __setitem__(self, key: Any, item: Any) -> None:
        try:
            self.__getitem__(key)
            raise ValueError("duplicate key '{}' found".format(key))
        except KeyError:
            return super().__setitem__(key, item)


def merge_participants_to_df(
    data_participants: List[Dict[Any, Any]],
    participant_col: str,
) -> DataFrame:
    # Check if all data have a `participant_col` key
    participant_col_checks = [_.get(participant_col) for _ in data_participants]
    if not all(participant_col_checks):
        raise Exception(
            f"One of the samples does not contain the '{participant_col}' information."
        )

    # Check if there are no duplicates in the data
    df_raw = DataFrame.from_dict(data_participants)
    df_melt = df_raw.melt(id_vars=[participant_col]).dropna()
    df_for_test = df_melt.drop(columns="value")
    duplicates = df_for_test[df_for_test.duplicated()]

    if duplicates.empty:
        return df_melt.pivot(index=participant_col, columns="variable")["value"]
    else:
        error_msg = "There are duplicates in your data "
        for participant_id, variable in duplicates.values:
            error_msg += f"\n{participant_id}: {variable}"
        raise Exception(error_msg)
