import importlib
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_TEACHER = any((path / ".TEACHER").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("scripts" if IS_TEACHER else "src")
INPUT_FOLDER = "temp/input"
OUTPUT_FOLDER = "temp/output"


def test_01(monkeypatch):
    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    main = importlib.import_module(f"{CODE_DIR.name}.main")

    main.initialize_folder(INPUT_FOLDER)
    main.delete_folder(OUTPUT_FOLDER)
    main.generate_file_copies(1000)

    main.hadoop(
        input_folder=INPUT_FOLDER,
        output_folder=OUTPUT_FOLDER,
        mapper_fn=main.mapper,
        reducer_fn=main.reducer,
    )

    result = {}
    for line in (ACTIVITY_DIR / OUTPUT_FOLDER / "part-00000").read_text(encoding="utf-8").splitlines():
        key, value = line.split("\t")
        result[key] = int(value)

    assert result["analytics"] == 5000
    assert result["business"] == 7000
    assert result["by"] == 3000
    assert result["algorithms"] == 2000
    assert result["analysis"] == 4000
