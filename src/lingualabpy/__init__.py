#   -------------------------------------------------------------
#   Licensed under the MIT License. See LICENSE in project root for information.
#   -------------------------------------------------------------
'''lingualabpy'''
from __future__ import annotations

__version__ = '0.0.1'

default_config = {
    'participant_col': 'participant_id',
    'participant_label': 'IV',
    'clinician_label': 'IE',
}

from lingualabpy.io import read_docx, read_json, read_textgrid, write_json
