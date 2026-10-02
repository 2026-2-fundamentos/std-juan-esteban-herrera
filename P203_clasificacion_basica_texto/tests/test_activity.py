from pathlib import Path


def test_01():
    activity_dir = Path(__file__).resolve().parents[1]
    submission_dir = activity_dir / "submission"

    assert (submission_dir / "clf.pkl").is_file()
    assert (submission_dir / "metrics.json").is_file()
    assert (submission_dir / "vectorizer.pkl").is_file()
