#   -------------------------------------------------------------
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
"""lingualabpy"""

from __future__ import annotations

try:
    from lingualabpy._version import __version__
except ImportError:
    pass


default_config = {
    "participant_col": "participant_id",
    "participant_label": "IE",
    "clinician_label": "IV",
    "f0_bounds": {
        "female": [100.0, 600.0],
        "male": [75.0, 300.0],
    },
    "unit_frequency": "Hertz",
}

from lingualabpy.io import read_audio, read_docx, read_json, write_json, read_textgrid
