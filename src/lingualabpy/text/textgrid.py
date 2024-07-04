import re
from textgrids import TextGrid, Interval
import warnings


def extract_intervals(textgrid: TextGrid, speakers: list[str]) -> list[list[Interval]]:
    """"""
    # Check if speakers are in the textgrid tiers
    tiers = set(textgrid.keys())
    if not set(speakers).issubset(tiers):
        raise ValueError(
            f"Some speaker(s) '{speakers}' are not a tier in the TextGrid '{tiers}'"
        )

    # Check if there is other speaker in the textgrid
    if not set(speakers) == tiers:
        warnings.warn(
            f"TextGrid '{tiers}' have more speakers than specify '{speakers}'"
        )

    # Extraction of intervals with text value
    speakers_intervals = []
    for speaker in speakers:
        speaker_intervals = []
        for interval in textgrid[speaker]:
            if interval.text:
                speaker_intervals.append(interval)
        speakers_intervals.append(speaker_intervals)

    # Checking if all intervals are correctly labeled
    def interval_qc(intervals, label):
        labels = set([_.text for _ in intervals])
        if not (len(labels) == 1 and labels.pop() == label):
            raise Exception(
                f"TextGrid was not labeled correctly, current label(s) '{labels}', should be '{label}'."
            )

    for intervals, speaker in zip(speakers_intervals, speakers):
        interval_qc(intervals, speaker)

    return speakers_intervals
