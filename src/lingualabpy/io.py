"""
Module contains tools for processing files
"""

import json
from docx import Document
from textgrids import TextGrid

from typing import Union


def read_docx(docx_path: str) -> Document:
    """"""
    return Document(docx_path)


def read_json(json_path: str) -> Union[list, dict]:
    """"""
    with open(json_path, "r") as file:
        content = json.load(file)
    return content


def read_textgrid(textgrid_path: str) -> TextGrid:
    """"""
    return TextGrid(textgrid_path)


def write_json(data: Union[list, dict], json_path: str) -> None:
    """"""
    with open(json_path, "w") as file:
        json.dump(data, file)
