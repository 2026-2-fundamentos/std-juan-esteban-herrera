import runpy
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_TEACHER = any((path / ".TEACHER").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("scripts" if IS_TEACHER else "src")
INPUT_DIR = ACTIVITY_DIR / "temp" / "input"
OUTPUT_DIR = ACTIVITY_DIR / "temp" / "output"


def run_main(monkeypatch):
    monkeypatch.chdir(ACTIVITY_DIR.parent)
    runpy.run_path(str(CODE_DIR / "main.py"), run_name="__main__")


def test_01(monkeypatch):
    run_main(monkeypatch)

    assert len(list(INPUT_DIR.glob("*.txt"))) == 4000
    assert (OUTPUT_DIR / "part-00000").is_file()
    assert (OUTPUT_DIR / "_SUCCESS").is_file()


def test_02(monkeypatch):
    run_main(monkeypatch)
    counts = {}
    for line in (OUTPUT_DIR / "part-00000").read_text(encoding="utf-8").splitlines():
        word, count = line.split("\t")
        counts[word] = int(count)

    assert counts["analytics"] == 5000
    assert counts["business"] == 7000
    assert counts["by"] == 3000
    assert counts["algorithms"] == 2000
    assert counts["analysis"] == 4000
