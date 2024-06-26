from collections import defaultdict
import numpy as np
from parselmouth import Sound
from parselmouth.praat import call

from lingualabpy.tools.data import UnchangeableDict


def measure_pitch(sound: Sound, f0min: str, f0max: str, unit: str) -> UnchangeableDict:
    """
    This function measures duration, pitch, HNR, jitter, and shimmer
    This is the function to measure source acoustics using default male parameters.
    """
    # compute usefull praat object
    pitch = call(sound, "To Pitch", 0.0, f0min, f0max)
    harmonicity = call(sound, "To Harmonicity (cc)", 0.01, f0min, 0.1, 1.0)
    point_process = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)

    # metrics container
    metrics = UnchangeableDict()

    # Metrics computation
    metrics["duration"] = call(sound, "Get total duration")
    metrics["f0_mean"] = call(pitch, "Get mean", 0, 0, unit)
    metrics["F0_std"] = call(pitch, "Get standard deviation", 0, 0, unit)
    metrics["hnr"] = call(harmonicity, "Get mean", 0, 0)

    # jitter
    jitter_types = ["local", ["local", "absolute"], "rap", "ppq5", "ddp"]
    for jitter_type in jitter_types:
        if isinstance(jitter_type, list):
            metric_name = f"jitter_{'_'.join(jitter_type)}"
            praat_function = f"Get jitter ({', '.join(jitter_type)})"
        else:
            metric_name = f"jitter_{jitter_type}"
            praat_function = f"Get jitter ({jitter_type})"
        metrics[metric_name] = call(
            point_process, praat_function, 0, 0, 0.0001, 0.02, 1.3
        )

    # shimmer
    shimmer_types = ["local", "local_dB", "apq3", "apq5", "apq11", "dda"]
    for shimmer_type in shimmer_types:
        metric_name = f"shimmer_{shimmer_type}"
        praat_function = f"Get shimmer ({shimmer_type})"
        metrics[metric_name] = call(
            [sound, point_process], praat_function, 0, 0, 0.0001, 0.02, 1.3, 1.6
        )

    return metrics


def measure_formants(
    sound: Sound, f0min: str, f0max: str, unit: str
) -> UnchangeableDict:
    """
    This function measures formants at each glottal pulse

    Puts, D. A., Apicella, C. L., & Cárdenas, R. A. (2012). Masculine voices signal men's threat potential in forager and industrial societies. Proceedings of the Royal Society of London B: Biological Sciences, 279(1728), 601-609.

    Adapted from: DOI 10.17605/OSF.IO/K2BHS
    """
    # compute usefull praat object
    point_process = call(sound, "To PointProcess (periodic, cc)", f0min, f0max)
    formants = call(sound, "To Formant (burg)", 0.0025, 5, 5000, 0.025, 50)
    number_of_points = call(point_process, "Get number of points")

    # metrics container
    metrics = UnchangeableDict()

    # Measure formants only at glottal pulses
    formants_list = defaultdict(list)
    for index in range(1, number_of_points + 1):
        time = call(point_process, "Get time from index", index)
        for pulse in [1, 2, 3, 4]:
            value = call(formants, "Get value at time", pulse, time, unit, "Linear")
            if str(value) != "nan":
                formants_list[pulse].append(value)

    # calculate mean and median formants across pulses, median is what is used in all subsequent calculations
    for pulse in [1, 2, 3, 4]:
        metrics[f"formants_{pulse}_mean"] = np.mean(formants_list[pulse])
        metrics[f"formants_{pulse}_median"] = np.median(formants_list[pulse])

    return metrics
