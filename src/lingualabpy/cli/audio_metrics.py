import click
from parselmouth import Sound
from pathlib import Path

from lingualabpy import default_config, write_json
from lingualabpy.audio.metrics import measure_pitch, measure_formants


@click.command()
@click.option(
    "--f0min",
    default=default_config["f0min"],
    show_default=True,
)
@click.option(
    "--f0max",
    default=default_config["f0max"],
    show_default=True,
)
@click.option(
    "--unit_frequency",
    default=default_config["unit_frequency"],
    show_default=True,
)
@click.option("--participant_id", "-p", default=None, help="")
@click.option("--output_json", default=None, help="")
@click.argument("audiofile", nargs=1, type=click.Path(exists=True))
def main(f0min, f0max, unit_frequency, participant_id, output_json, audiofile):
    """Doc"""
    sound = Sound(audiofile)
    metrics = measure_pitch(sound, f0min, f0max, unit_frequency)
    metrics.update(measure_formants(sound, f0min, f0max, unit_frequency))

    audiofile_stem = Path(audiofile).stem

    if participant_id:
        metrics["participant_id"] = participant_id
    else:
        metrics["participant_id"] = audiofile_stem.split("_")[0]

    if not output_json:
        output_json = audiofile_stem + "_metric-audio.json"

    write_json(dict(metrics), output_json)
