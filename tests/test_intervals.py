from textgrids import Interval
from lingualabpy.text.interval import intervals_masking


def test_intervals_masking():
    intervals = [
        Interval(xmin=1, xmax=4),
        Interval(xmin=11, xmax=20),
        Interval(xmin=31, xmax=40),
    ]
    intervals_mask = [
        Interval(xmin=4, xmax=5),
        Interval(xmin=10, xmax=12),
        Interval(xmin=18, xmax=19),
        Interval(xmin=35, xmax=44),
    ]
    intervals_clean = [[1, 4], [12, 18], [19, 20], [31, 35]]

    assert intervals_masking(intervals, intervals_mask) == intervals_clean
