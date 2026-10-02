from pathlib import Path


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def test_01_policy_assessment_exists():
    assert (SUBMISSION_DIR / "policy_assessment.csv").is_file()


def test_02_policy_recommendation_exists():
    assert (SUBMISSION_DIR / "policy_recommendation.csv").is_file()


def test_03_policy_contract_exists():
    assert (SUBMISSION_DIR / "policy_contract.json").is_file()
