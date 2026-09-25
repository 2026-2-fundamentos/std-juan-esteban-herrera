import subprocess
import sys
from pathlib import Path

import pytest


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
ALLOWED_DATASETS = ("train", "test", "prod")


@pytest.mark.parametrize("dataset", ALLOWED_DATASETS)
def test_main_accepts_each_available_dataset(dataset):
    # Cada valor permitido debe producir una ejecución completa y una salida interpretable.

    result = subprocess.run(
        [sys.executable, "src/main.py", dataset],
        cwd=ACTIVITY_DIR,
        check=True,
        capture_output=True,
        text=True,
    )

    assert f"Conjunto: {dataset}" in result.stdout
    assert "Accuracy: " in result.stdout
    assert "Balanced accuracy: " in result.stdout


def test_main_rejects_an_unknown_dataset():
    # Un valor ambiguo debe detener la ejecución antes de evaluar datos no previstos.

    result = subprocess.run(
        [sys.executable, "src/main.py", "development"],
        cwd=ACTIVITY_DIR,
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode != 0
    assert "invalid choice" in result.stderr
