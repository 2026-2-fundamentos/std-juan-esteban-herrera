from pathlib import Path


def test_01():
    assert Path("submission/ventas.csv").is_file()
