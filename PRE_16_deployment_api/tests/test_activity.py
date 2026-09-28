from pathlib import Path

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_TEACHER = any((path / ".TEACHER").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("scripts" if IS_TEACHER else "src")


def test_01():
    client_file = CODE_DIR / "client.py"
    server_file = CODE_DIR / "server.py"

    assert client_file.is_file()
    assert client_file.read_text(encoding="utf-8").strip()
    assert server_file.is_file()
    assert server_file.read_text(encoding="utf-8").strip()
