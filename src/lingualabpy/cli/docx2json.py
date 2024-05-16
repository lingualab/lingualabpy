import click
import json
from docx import Document

from ..utils.utils import parse_waywithwords


@click.command()
@click.option("--origin", default="waywithwords", show_default=True)
@click.argument("docx_path", nargs=1, type=click.Path(exists=True))
@click.argument("output", nargs=1)
def main(docx_path, output, origin):
    """Doc"""
    document = Document(docx_path)

    if origin == "waywithwords":
        data = parse_waywithwords(document)

    with open(output, "w") as f:
        json.dump(data, f)
