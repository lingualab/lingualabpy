from textgrids import TextGrid, Interval


def is_overlap(interval0: Interval, interval1: Interval) -> bool:
    '''Check if two intervals overlap'''
    return interval0.xmin <= interval1.xmax and interval1.xmin <= interval0.xmax


def remove_overlap(interval: Interval, interval_to_remove: Interval) -> list[Interval]:
    ''''''
    updated_intervals = []

    # If the interval doesn't overlap with the interval to be removed,
    # we can add it to the updated list as-is
    if not is_overlap(interval, interval_to_remove):
        updated_intervals.append(interval)
    
    else:
        # If there is an overlap and the start of the interval
        # is before the start of the interval to be removed,
        # add the non-overlapping part to the result.
        if interval.xmin < interval_to_remove.xmin:
            updated_intervals.append(Interval(xmin=interval.xmin, xmax=interval_to_remove.xmin))

        # Similarly, if the end of the interval is after the end of
        # the interval to be removed, add the non-overlapping part to the result.
        if interval.xmax > interval_to_remove.xmax:
            updated_intervals.append(Interval(xmin=interval_to_remove.xmax, xmax=interval.xmax))

    return updated_intervals


def text_triming(grid: TextGrid, participant: str, clinician: str) -> list[Interval]:
    ''''''
    intervals_participant = [_ for _ in grid[participant] if _.text]
    intervals_clinician = [_ for _ in grid[clinician] if _.text]

    # Checking if all intervals are correctly labeled
    def interval_qc(intervals, label):
        labels = set([_.text for _ in intervals])
        if not(len(labels) == 1 and labels.pop() == label):
            raise Exception(
                f"TextGrid was not labeled correctly, current label(s) '{labels}', should be '{label}'."
            )
    
    interval_qc(intervals_participant, participant)
    interval_qc(intervals_clinician, clinician)

    for interval in intervals_participant:
        pass
