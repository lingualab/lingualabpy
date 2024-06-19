import click

from lingualabpy import default_config, read_audio, read_textgrid
from lingualabpy.audio.triming import extract_audio
from lingualabpy.text.textgrid import extract_intervals
from lingualabpy.tools.interval import intervals_masking


@click.command()
@click.option(
    "--participant_label",
    default=default_config["participant_label"],
    show_default=True,
)
@click.option(
    "--clinician_label",
    default=default_config["clinician_label"],
    show_default=True,
)
@click.argument("textgrid", nargs=1, type=click.Path(exists=True))
@click.argument("audiofile", nargs=1, type=click.Path(exists=True))
@click.argument("output", nargs=1)
def main(participant_label, clinician_label, textgrid, audiofile, output):
    """Doc"""
    grid = read_textgrid(textgrid)

    try:
        participant_intervals, clinician_intervals = extract_intervals(
            grid, [participant_label, clinician_label]
        )
    except Exception as e:
        raise Exception(f"Failed to extract intervals for {textgrid}", repr(e))

    participant_intervals_clean = intervals_masking(
        participant_intervals, clinician_intervals
    )

    audio = read_audio(audiofile)

    audio_clean = extract_audio(audio, participant_intervals_clean)

    audio_clean.export(output)
