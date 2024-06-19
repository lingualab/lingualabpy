import pytest
from pathlib import Path


class Resources:
    NORTH_NAME = "the_north_wind_and_the_sun"

    def __init__(self, base_path):
        self.data_path = Path(base_path) / "resources"
        self.the_north_path = self.data_path / self.NORTH_NAME

    def the_north(self, extension: str) -> str:
        return str(self.the_north_path / f"{self.NORTH_NAME}.{extension}")


@pytest.fixture(scope="module")
def resources(request):
    return Resources(request.fspath.dirname)
