from pathlib import Path


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def test_01():
    assert (SUBMISSION_DIR / "features_preprocessor.pkl").is_file()
    assert (SUBMISSION_DIR / "flexible_features_preprocessor.pkl").is_file()
    assert (SUBMISSION_DIR / "linear_flexible_model.pkl").is_file()
    assert (SUBMISSION_DIR / "mlp.pkl").is_file()
    assert (SUBMISSION_DIR / "model_comparison.csv").is_file()
