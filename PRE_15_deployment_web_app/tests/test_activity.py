"""Verifica la evidencia mínima del taller de aplicación web."""

from pathlib import Path


def test_web_application_workshop_files_exist():
    expected_files = [
        "src/main.py",
        "src/templates/index.html",
        "HOUSE_PREDICTOR.pkl",
    ]
    for filename in expected_files:
        assert Path(filename).exists()
