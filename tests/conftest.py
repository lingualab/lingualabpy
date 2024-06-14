import pytest
from pathlib import Path

import lingualabpy


class Resources:
    def __init__(self, base_path):
        self.data_path = Path(base_path) / "resources"

    def __getitem__(self, file_path):
        return self.data_path / file_path


@pytest.fixture(scope="module")
def resources(request):
    return Resources(request.fspath.dirname)


@pytest.fixture()
def north_docx(resources):
    yield lingualabpy.read_docx(
        resources[
            "the_north_wind_and_the_sun/the_north_wind_and_the_sun_transcript-www.docx"
        ]
    )


@pytest.fixture()
def north_json(resources):
    yield lingualabpy.read_json(
        resources[
            "the_north_wind_and_the_sun/the_north_wind_and_the_sun_transcript-www.json"
        ]
    )
