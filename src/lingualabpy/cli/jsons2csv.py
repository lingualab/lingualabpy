import click
import json

from .. import default_config
from ..utils.utils import merge_participants_to_df


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
        with open(path, "r") as file:
            data.append(json.load(file))
    df = merge_participants_to_df(data, participant_col=column)
    df.to_csv(output)
