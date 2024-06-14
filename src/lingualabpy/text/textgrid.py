from textgrids import TextGrid, Interval


def extract_intervals(grid: TextGrid, speakers: list[str]) -> tuple[list[Interval]]:
    """"""
    speakers_intervals = []
    for speaker in speakers:
        speakers_intervals.append([_ for _ in grid[speaker] if _.text])

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
