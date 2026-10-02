"""Comprueba que el estudiante participó en la demostración guiada."""

import json
from pathlib import Path


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
STUDENT_NOTEBOOK = ACTIVITY_DIR / "notebooks/notebook.ipynb"
PROFESSOR_NOTEBOOK = ACTIVITY_DIR / "professor/notebook.ipynb"
IS_PROFESSOR = any(
    (path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents
) and PROFESSOR_NOTEBOOK.is_file()
NOTEBOOK = PROFESSOR_NOTEBOOK if IS_PROFESSOR else STUDENT_NOTEBOOK


def test_01():
    notebook = json.loads(NOTEBOOK.read_text(encoding="utf-8"))
    assert len(notebook["cells"]) > 0, "Agrega al menos una celda al notebook."
