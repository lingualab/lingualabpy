import click

from lingualabpy import default_config, read_textgrid
from lingualabpy.text import text_triming


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
@click.argument('audio', nargs=1, type=click.Path(exists=True))
@click.argument('textgrid', nargs=1, type=click.Path(exists=True))
@click.argument('output', nargs=1)
def main(participant_label, clinician_label, audio, textgrid, output):
    '''Doc'''
    grid = read_textgrid(textgrid)
    intervals = text_triming(grid, participant_label, clinician_label)

