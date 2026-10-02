"""Valida que la actividad entregue al menos un artefacto final."""

from pathlib import Path


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def test_01_submission_contains_the_search_protocol():
    expected_artifacts = {
        "decision_boundary.csv",
        "search_plan.csv",
        "plan_comparison.csv",
        "search_planning_map.png",
    }
    generated_artifacts = {
        path.name
        for path in SUBMISSION_DIR.iterdir()
        if path.is_file() and path.name != ".gitkeep"
    }

    assert expected_artifacts <= generated_artifacts, (
        "Ejecuta el taller y entrega el protocolo de contingencia, el plan, "
        "la comparación y el mapa en submission/."
    )
