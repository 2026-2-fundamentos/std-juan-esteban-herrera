from pathlib import Path


def test_01():
    assert Path("submission/summary.csv").is_file()
    assert Path("submission/top10_drivers.png").is_file()
