"""Valida que la actividad entregue al menos un artefacto final."""

from pathlib import Path


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def test_submission_contains_an_artifact():
    """La solución debe producir al menos un archivo final en submission/."""
    artifacts = [
        path
        for path in SUBMISSION_DIR.rglob("*")
        if path.is_file() and path.name != ".gitkeep"
    ]

    assert artifacts, (
        "Ejecuta la solución y guarda al menos un artefacto final en submission/."
    )
