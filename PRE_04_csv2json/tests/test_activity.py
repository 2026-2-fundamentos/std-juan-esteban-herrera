from pathlib import Path


def test_01():
    assert Path("submission/drivers.json").is_file()
