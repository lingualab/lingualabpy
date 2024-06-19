from lingualabpy.cli import audio_triming

from lingualabpy import default_config, read_audio, read_textgrid
from lingualabpy.audio.triming import extract_audio
from lingualabpy.text.textgrid import extract_intervals
from lingualabpy.tools.interval import intervals_masking

from click.testing import CliRunner


def test_audio_triming(tmp_path, resources):
    runner = CliRunner()
    north_textgrid = resources.the_north("TextGrid")
    north_wav = resources.the_north("wav")

    with runner.isolated_filesystem(temp_dir=tmp_path):
        output = str(tmp_path / "output.wav")


def test_intervals_masking(resources):
    north_textgrid = resources.the_north("TextGrid")
    grid = read_textgrid(north_textgrid)
    participant_intervals, clinician_intervals = extract_intervals(
        grid, [default_config["participant_label"], default_config["clinician_label"]]
    )
    participant_intervals_clean = intervals_masking(
        participant_intervals, clinician_intervals
    )
    intervals_clean = [[1, 4], [12, 18], [19, 20], [31, 33]]

    assert participant_intervals_clean == intervals_clean
