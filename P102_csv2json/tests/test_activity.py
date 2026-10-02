import json
import runpy
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_PROFESSOR = any((path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("professor" if IS_PROFESSOR else "src")
SUBMISSION_FILE = ACTIVITY_DIR / "submission" / "drivers.json"


def test_01(monkeypatch):
    monkeypatch.chdir(ACTIVITY_DIR)
    runpy.run_path(str(CODE_DIR / "main.py"), run_name="__main__")

    assert SUBMISSION_FILE.is_file()

    records = json.loads(SUBMISSION_FILE.read_text(encoding="utf-8"))

    assert len(records) == 34
    assert all(set(record) == {"driverId", "name", "certified", "wage-plan"} for record in records)
    assert records[0] == {
        "driverId": "10",
        "name": "George Vetticaden",
        "certified": "N",
        "wage-plan": "miles",
    }
