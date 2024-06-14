import click

from lingualabpy import read_docx, write_json
from lingualabpy.text.parser import parse_waywithwords


@click.command()
@click.option("--origin", default="waywithwords", show_default=True)
@click.argument("docx_path", nargs=1, type=click.Path(exists=True))
@click.argument("output", nargs=1)
def main(docx_path, output, origin):
    """Doc"""
    document = read_docx(docx_path)

    if origin == "waywithwords":
        data = parse_waywithwords(document)

    else:
        raise ValueError(f"{origin} is not implemented")

    write_json(data, output)
