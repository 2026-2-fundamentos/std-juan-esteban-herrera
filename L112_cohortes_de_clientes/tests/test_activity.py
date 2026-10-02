import importlib
from pathlib import Path

import pandas as pd
from pytest import approx

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
PROFESSOR_DIR = ACTIVITY_DIR / "professor"
IS_PROFESSOR = any(
    (path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents
) and any(path.name != ".gitkeep" for path in PROFESSOR_DIR.iterdir())
CODE_DIR = ACTIVITY_DIR / ("professor" if IS_PROFESSOR else "src")
SUBMISSION_DIR = ACTIVITY_DIR / "submission"
CSV_FILE = SUBMISSION_DIR / "cohort_retention.csv"
PNG_FILE = SUBMISSION_DIR / "cohort_retention_heatmap.png"

COHORTS = [
    ["2022-01", 0, 100, 100],
    ["2022-01", 1, 26, 100],
    ["2022-01", 2, 25, 100],
    ["2022-01", 3, 26, 100],
    ["2022-01", 4, 22, 100],
    ["2022-01", 5, 24, 100],
    ["2022-01", 6, 23, 100],
    ["2022-01", 7, 29, 100],
    ["2022-02", 0, 76, 76],
    ["2022-02", 1, 20, 76],
    ["2022-02", 2, 17, 76],
    ["2022-02", 3, 11, 76],
    ["2022-02", 4, 21, 76],
    ["2022-02", 5, 17, 76],
    ["2022-02", 6, 13, 76],
    ["2022-03", 0, 70, 70],
    ["2022-03", 1, 11, 70],
    ["2022-03", 2, 12, 70],
    ["2022-03", 3, 17, 70],
    ["2022-03", 4, 21, 70],
    ["2022-03", 5, 16, 70],
    ["2022-04", 0, 57, 57],
    ["2022-04", 1, 12, 57],
    ["2022-04", 2, 13, 57],
    ["2022-04", 3, 13, 57],
    ["2022-04", 4, 15, 57],
    ["2022-05", 0, 46, 46],
    ["2022-05", 1, 12, 46],
    ["2022-05", 2, 11, 46],
    ["2022-05", 3, 11, 46],
    ["2022-06", 0, 29, 29],
    ["2022-06", 1, 2, 29],
    ["2022-06", 2, 5, 29],
    ["2022-07", 0, 23, 23],
    ["2022-07", 1, 3, 23],
    ["2022-08", 0, 27, 27],
]


def test_01(monkeypatch):
    CSV_FILE.unlink(missing_ok=True)
    PNG_FILE.unlink(missing_ok=True)

    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    importlib.import_module(f"{CODE_DIR.name}.pregunta_01").build_cohort_analysis()

    assert CSV_FILE.exists()
    assert PNG_FILE.exists()
    assert PNG_FILE.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"

    df = pd.read_csv(CSV_FILE, dtype={"cohort_month": str})

    assert df.columns.tolist() == [
        "cohort_month",
        "period_index",
        "active_customers",
        "cohort_size",
        "retention_rate",
    ]
    assert df.iloc[:, :4].values.tolist() == COHORTS
    assert df["retention_rate"].tolist() == approx(
        [active / size for _, _, active, size in COHORTS], abs=1e-4
    )
