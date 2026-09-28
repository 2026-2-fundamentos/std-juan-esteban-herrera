from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]


def test_01():
    assert (ACTIVITY_DIR / "submission" / "model_test_report.json").is_file()
