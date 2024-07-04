import click
from parselmouth import Sound
from pathlib import Path

from lingualabpy import default_config, write_json
from lingualabpy.audio.metrics import measure_pitch, measure_formants


@click.command()
@click.option(
    "--sex",
    type=click.Choice(["female", "male"]),
    help=f"Set f0min and f0max for praat analysis. {default_config['f0_bounds']}",
)
@click.option(
    "--f0min",
    type=float,
    help="Define f0min for praat analysis. Not required if sex is specify",
)
@click.option(
    "--f0max",
    type=float,
    help="Define f0max for praat analysis. Not required if sex is specify",
)
@click.option(
    "--unit_frequency",
    default=default_config["unit_frequency"],
    show_default=True,
)
@click.option("--participant_id", "-p", default=None, help="")
@click.option("--output_json", default=None, help="")
@click.argument("audiofile", nargs=1, type=click.Path(exists=True))
def main(sex, f0min, f0max, unit_frequency, participant_id, output_json, audiofile):
    """Doc"""
    if sex:
        f0min, f0max = default_config["f0_bounds"][sex]
    else:
        if not f0min or not f0max:
            raise click.UsageError(
                "'--f0min' and '--f0max' are required if '--sex' is not specified"
            )

    sound = Sound(audiofile)
    metrics = measure_pitch(sound, f0min, f0max, unit_frequency)
    metrics.update(measure_formants(sound, f0min, f0max, unit_frequency))

    audiofile_stem = Path(audiofile).stem

    if participant_id:
        metrics["participant_id"] = participant_id

    audiofile = Path(audiofile)

    metrics["filename"] = audiofile.name

    if not output_json:
        output_json = audiofile.stem + "_metric-audio.json"

    write_json(dict(metrics), output_json)
