import importlib
import json
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_TEACHER = any((path / ".TEACHER").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("scripts" if IS_TEACHER else "src")
REPORT_FILE = ACTIVITY_DIR / "submission" / "data_quality_report.json"


def test_01(monkeypatch):
    REPORT_FILE.unlink(missing_ok=True)

    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    importlib.import_module(f"{CODE_DIR.name}.pregunta_01").main()

    assert REPORT_FILE.exists()

    report = json.loads(REPORT_FILE.read_text(encoding="utf-8"))

    assert report["row_count"] == 103
    assert report["column_count"] == 11
    assert report["missing_required_columns"] == []
    assert report["unexpected_columns"] == []
    assert report["duplicate_row_count"] == 2
    assert report["duplicate_supplier_id_row_count"] == 6
    assert report["missing_value_count_by_column"] == {
        "supplier_id": 0,
        "supplier": 0,
        "country": 0,
        "city": 0,
        "purchase_date": 0,
        "amount": 24,
        "discount": 35,
        "weight": 30,
        "units": 2,
        "unit_price": 0,
        "contact_email": 0,
    }
    assert report["invalid_email_count"] == 11
    assert report["invalid_unit_count"] == 0
    assert report["country_values"] == [
        " Colombia ",
        "CO",
        "COL",
        "COLOMBIA",
        "Colombia",
        "colombia",
    ]
