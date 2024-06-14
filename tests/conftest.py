import pytest
from pathlib import Path


class Resources:
    def __init__(self, base_path):
        self.data_path = Path(base_path) / "resources"
        self.the_north_path = self.data_path / "the_north_wind_and_the_sun"

    @property
    def the_north_docx(self):
        return self.the_north_path / "the_north_wind_and_the_sun_transcript-www.docx"

    @property
    def the_north_json(self):
        return self.the_north_path / "the_north_wind_and_the_sun_transcript-www.json"


@pytest.fixture(scope="module")
def resources(request):
    return Resources(request.fspath.dirname)


@pytest.fixture()
def north_docx(resources):
    yield str(resources.the_north_docx)


@pytest.fixture()
def north_json(resources):
    yield str(resources.the_north_json)
