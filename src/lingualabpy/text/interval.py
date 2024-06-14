from textgrids import Interval


def interval_to_list(interval: Interval) -> list[float]:
    """"""
    return [interval.xmin, interval.xmax]


def is_overlap(interval0: Interval, interval1: Interval) -> bool:
    """Check if two intervals overlap"""
    return interval0.xmin <= interval1.xmax and interval1.xmin <= interval0.xmax


def remove_overlap(interval: Interval, interval_to_remove: Interval) -> list[Interval]:
    """"""
    # Return interval as a list if there is no overlap
    if not is_overlap(interval, interval_to_remove):
        return [interval]

    else:
        updated_intervals = []

        # If the start of the interval is before the start of the interval to be removed,
        # add the non-overlapping part to the result.
        if interval.xmin < interval_to_remove.xmin:
            updated_intervals.append(
                Interval(xmin=interval.xmin, xmax=interval_to_remove.xmin)
            )

        # If the end of the interval is after the end of the interval to be removed,
        # add the non-overlapping part to the result.
        if interval.xmax > interval_to_remove.xmax:
            updated_intervals.append(
                Interval(xmin=interval_to_remove.xmax, xmax=interval.xmax)
            )

        return updated_intervals


def intervals_masking(
    intervals: list[Interval], intervals_mask: list[Interval]
) -> list[list[float]]:
    """"""
    # Each intervals mask will be remove from all the intervals
    for interval_to_remove in intervals_mask:
        new_intervals = []
        for interval in intervals:

            # if the start of the interval is after the end of the mask
            # we can just add the interval they are sorted
            if interval.xmin > interval_to_remove.xmax:
                new_intervals.append(interval)

            else:
                new_intervals += remove_overlap(interval, interval_to_remove)

        intervals = new_intervals

    return [interval_to_list(_) for _ in intervals]
