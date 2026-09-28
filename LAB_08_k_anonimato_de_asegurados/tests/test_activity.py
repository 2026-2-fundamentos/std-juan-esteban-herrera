import importlib
import json
from pathlib import Path

import pandas as pd
from pytest import approx

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_TEACHER = any((path / ".TEACHER").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("scripts" if IS_TEACHER else "src")
REPORT_FILE = ACTIVITY_DIR / "submission" / "privacy_report.json"
PUBLISHED_FILE = ACTIVITY_DIR / "submission" / "insurance_published.csv"


def test_01(monkeypatch):
    REPORT_FILE.unlink(missing_ok=True)
    PUBLISHED_FILE.unlink(missing_ok=True)

    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    importlib.import_module(f"{CODE_DIR.name}.pregunta_01").pregunta_01()

    assert REPORT_FILE.exists()
    assert PUBLISHED_FILE.exists()

    report = json.loads(REPORT_FILE.read_text(encoding="utf-8"))

    assert report["original_k"] == 1
    assert report["original_unique_records"] == 1330
    assert report["schemes"]["with_children"] == {
        "quasi_identifiers": [
            "age_group",
            "sex",
            "bmi_group",
            "children_group",
            "region",
        ],
        "equivalence_classes": 278,
        "k_before_suppression": 1,
        "suppressed_records": 395,
        "published_records": 943,
        "published_classes": 105,
        "classes_without_smoker_diversity": 21,
        "records_without_smoker_diversity": 159,
    }
    assert report["schemes"]["without_children"] == {
        "quasi_identifiers": ["age_group", "sex", "bmi_group", "region"],
        "equivalence_classes": 108,
        "k_before_suppression": 1,
        "suppressed_records": 55,
        "published_records": 1283,
        "published_classes": 85,
        "classes_without_smoker_diversity": 6,
        "records_without_smoker_diversity": 59,
    }
    assert report["selected_scheme"] == "without_children"
    assert report["mean_charges_original"] == approx(13270.4223, abs=1e-4)
    assert report["mean_charges_published"] == approx(13351.6461, abs=1e-4)
    assert report["smoker_rate_original"] == approx(0.2048, abs=1e-4)
    assert report["smoker_rate_published"] == approx(0.2011, abs=1e-4)

    published = pd.read_csv(PUBLISHED_FILE)

    assert published.columns.tolist() == [
        "age_group",
        "sex",
        "bmi_group",
        "region",
        "smoker",
        "charges",
    ]
    assert len(published) == 1283
    assert (
        published.groupby(["age_group", "sex", "bmi_group", "region"]).size().min() >= 5
    )
    assert published["age_group"].value_counts().to_dict() == {
        "18-29": 406,
        "50-64": 374,
        "40-49": 267,
        "30-39": 236,
    }
    assert published["bmi_group"].value_counts().to_dict() == {
        "obesidad": 707,
        "sobrepeso": 386,
        "normal": 190,
    }
    assert published["smoker"].value_counts().to_dict() == {"no": 1025, "yes": 258}
    assert published["charges"].sum() == approx(17130161.9355, abs=1e-4)
    assert published.iloc[0].tolist() == [
        "18-29",
        "female",
        "sobrepeso",
        "southwest",
        "yes",
        approx(16884.924, abs=1e-4),
    ]
    assert published.iloc[-1].tolist() == [
        "50-64",
        "female",
        "sobrepeso",
        "northwest",
        "yes",
        approx(29141.3603, abs=1e-4),
    ]
