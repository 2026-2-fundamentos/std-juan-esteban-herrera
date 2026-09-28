from pathlib import Path


def test_01():
    assert Path("submission/anonymized.csv").is_file()
