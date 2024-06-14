import pandas as pd

from typing import Any, Dict, List


def merge_participants_to_df(
    data_participants: List[Dict[Any, Any]],
    participant_col: str,
) -> pd.DataFrame:
    # Check if all data have a `participant_col` key
    participant_col_checks = [_.get(participant_col) for _ in data_participants]
    if not all(participant_col_checks):
        raise Exception(
            f"One of the samples does not contain the '{participant_col}' information."
        )

    # Check if there are no duplicates in the data
    df_raw = pd.DataFrame.from_dict(data_participants)
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
