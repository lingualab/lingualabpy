from lingualabpy.cli import docx2json
from lingualabpy import read_json

from click.testing import CliRunner


def test_docx2json(tmp_path, north_docx, north_json):
    runner = CliRunner()
    with runner.isolated_filesystem(temp_dir=tmp_path):
        output = str(tmp_path / "output.json")

        # testing a successful run
        result = runner.invoke(docx2json.main, [north_docx, output])
        assert result.exit_code == 0
        assert read_json(output) == read_json(north_json)

        # testing a run with an unknown origin
        result = runner.invoke(
            docx2json.main, ["--origin", "other", north_docx, output]
        )
        assert result.exit_code == 1
        assert type(result.exception) == ValueError
