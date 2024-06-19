#   -------------------------------------------------------------
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""lingualabpy"""
from __future__ import annotations

__version__ = "0.0.3"

default_config = {
    "participant_col": "participant_id",
    "participant_label": "IE",
    "clinician_label": "IV",
}

from lingualabpy.io import read_audio, read_docx, read_json, write_json, read_textgrid
