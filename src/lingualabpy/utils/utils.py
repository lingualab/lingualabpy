from collections import defaultdict
import pandas as pd
import re

from typing import List, Dict
from docx import Document


def merge_participants_to_df(
    data_participants: List[Dict],
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


def parse_waywithwords(document: Document) -> dict:
    """ """
    waywithwords = {
        "IV": "interviewer",
        "IE": "interviewee",
    }

    results = defaultdict(list)

    for para in document.paragraphs:
        try:
            content = para.text.split()
            speaker = content[0]
            transcription = " ".join(content[1:])
        except:
            speaker = None

        if (
            speaker in waywithwords.keys()
            and not transcription.lower() in waywithwords.values()
        ):
            results[waywithwords[speaker]].append(transcription)

        elif re.findall(r"[0-9][0-9]:[0-5][0-9]:[0-5][0-9]", para.text):
            results["time"].append(para.text)

        else:
            results["remainder"].append(para.text)

    return results
