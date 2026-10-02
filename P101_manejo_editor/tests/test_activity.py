import runpy
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_PROFESSOR = any((path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("professor" if IS_PROFESSOR else "src")
SUBMISSION_FOLDER = "submission"


def test_01(monkeypatch):
    monkeypatch.chdir(ACTIVITY_DIR)
    runpy.run_path(str(CODE_DIR / "main.py"), run_name="__main__")

    assert (ACTIVITY_DIR / SUBMISSION_FOLDER / "part-00000").is_file()
    assert (ACTIVITY_DIR / SUBMISSION_FOLDER / "_SUCCESS").is_file()

    result = {}
    for line in (ACTIVITY_DIR / SUBMISSION_FOLDER / "part-00000").read_text(encoding="utf-8").splitlines():
        key, value = line.split("\t")
        result[key] = int(value)

    assert result["analytics"] == 5000
    assert result["business"] == 7000
    assert result["by"] == 3000
    assert result["algorithms"] == 2000
    assert result["analysis"] == 4000
