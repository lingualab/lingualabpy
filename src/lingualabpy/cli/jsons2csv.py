import click
import json

from lingualabpy import default_config, read_json
from lingualabpy.tools.data import merge_participants_to_df


@click.command()
@click.option(
    "-c",
    "--column",
    default=default_config["participant_col"],
    show_default=True,
)
@click.argument("jsons", nargs=-1, type=click.Path(exists=True))
@click.argument("output", nargs=1)
def main(column, jsons, output):
    """ """
    data = []
    for path in jsons:
        data.append(read_json(path))
    df = merge_participants_to_df(data, participant_col=column)
    df.to_csv(output)
