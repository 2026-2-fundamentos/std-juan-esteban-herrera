from pathlib import Path


def test_01():
    activity_dir = Path(__file__).resolve().parents[1]
    submission_dir = activity_dir / "submission"

    assert (submission_dir / "calibration_summary.csv").is_file()
    assert (submission_dir / "group_review.csv").is_file()
    assert (submission_dir / "threshold_tradeoff.csv").is_file()
