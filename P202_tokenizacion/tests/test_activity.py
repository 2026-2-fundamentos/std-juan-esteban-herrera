from pathlib import Path


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def test_01():
    assert (SUBMISSION_DIR / "document_term_matrix.npz").is_file()
    assert (SUBMISSION_DIR / "matrix_metadata.json").is_file()
    assert (SUBMISSION_DIR / "tokenized_abstracts.csv").is_file()
    assert (SUBMISSION_DIR / "vocabulary.csv").is_file()
