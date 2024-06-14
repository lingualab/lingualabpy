from lingualabpy.text.parser import parse_waywithwords


def test_waywithwords(north_docx, north_json):
    assert parse_waywithwords(north_docx) == north_json
