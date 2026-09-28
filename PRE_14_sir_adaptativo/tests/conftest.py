from pathlib import Path

import pytest


ACTIVITY_DIR = Path(__file__).resolve().parents[1]


@pytest.fixture(autouse=True)
def run_from_activity_directory(monkeypatch):
    monkeypatch.chdir(ACTIVITY_DIR)
