import json
import subprocess
import sys
from pathlib import Path

import pytest


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ACTIVITY_DIR))


@pytest.mark.parametrize("dataset", ["train", "test", "prod"])
def test_config_accepts_each_available_dataset(tmp_path, dataset):
    # Una configuración válida debe ser intercambiable sin modificar el programa.
    from src.main import ALLOWED_DATASETS, load_dataset_name

    assert dataset in ALLOWED_DATASETS

    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"dataset": dataset}), encoding="utf-8")

    assert load_dataset_name(config_path) == dataset


def test_config_rejects_an_unknown_dataset(tmp_path):
    # Un valor no acordado debe fallar antes de que se seleccione una fuente de datos.
    from src.main import load_dataset_name

    config_path = tmp_path / "config.json"
    config_path.write_text(json.dumps({"dataset": "development"}), encoding="utf-8")

    with pytest.raises(ValueError, match="train, test, prod"):
        load_dataset_name(config_path)


def test_main_reports_the_selected_dataset_and_metrics():
    # La salida confirma qué configuración produjo las métricas observadas.

    result = subprocess.run(
        [sys.executable, "src/main.py"],
        cwd=ACTIVITY_DIR,
        check=True,
        capture_output=True,
        text=True,
    )

    assert "Conjunto: test" in result.stdout
    assert "Accuracy: " in result.stdout
    assert "Balanced accuracy: " in result.stdout
