"""Pruebas de calificación automática para LAB_04_ingestion_de_texto_en_directorios."""

from pathlib import Path

import pandas as pd  # type: ignore


ROOT = Path(__file__).resolve().parents[1]
SUBMISSION_DIR = ROOT / "submission"


def test_01_creates_the_required_submission_files():
    """La actividad debe generar ambos entregables permanentes."""
    from ..src import pregunta_01 as pregunta

    for filename in ("train_dataset.csv", "test_dataset.csv"):
        (SUBMISSION_DIR / filename).unlink(missing_ok=True)

    pregunta.pregunta_01()

    assert (SUBMISSION_DIR / "train_dataset.csv").exists()
    assert (SUBMISSION_DIR / "test_dataset.csv").exists()


def test_02_builds_complete_datasets_with_the_expected_labels():
    """Los CSV deben conservar todas las frases y su etiqueta de sentimiento."""
    from ..src import pregunta_01 as pregunta

    pregunta.pregunta_01()

    train_dataset = pd.read_csv(SUBMISSION_DIR / "train_dataset.csv")

    assert train_dataset.columns.tolist() == ["phrase", "target"]
    assert train_dataset["phrase"].notna().all()

    counts = train_dataset["target"].value_counts()

    assert counts["neutral"] == 1117
    assert counts["positive"] == 458
    assert counts["negative"] == 236

    test_dataset = pd.read_csv(SUBMISSION_DIR / "test_dataset.csv")

    assert test_dataset.columns.tolist() == ["phrase", "target"]
    assert test_dataset["phrase"].notna().all()

    counts = test_dataset["target"].value_counts()

    assert counts["neutral"] == 274
    assert counts["positive"] == 112
    assert counts["negative"] == 67
