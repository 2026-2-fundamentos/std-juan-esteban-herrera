import importlib
from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_TEACHER = any((path / ".TEACHER").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("scripts" if IS_TEACHER else "src")


def answer(name, monkeypatch):
    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    module = importlib.import_module(f"{CODE_DIR.name}.main")
    return getattr(module, name)()


def test_01(monkeypatch):
    assert answer("pregunta_01", monkeypatch) == "Hola mundo cruel!"


def test_02(monkeypatch):
    assert answer("pregunta_02", monkeypatch) == "Hello cruel world!"
