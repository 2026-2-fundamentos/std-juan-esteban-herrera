# Uso: python3 -m pytest -q tests/test_activity.py

import importlib.util
from pathlib import Path

import pytest


ACTIVITY_DIR = Path(__file__).resolve().parents[1]


def load_main():
    SPECIFICATION = importlib.util.spec_from_file_location("input_testing_main", ACTIVITY_DIR / "src" / "main.py")
    main = importlib.util.module_from_spec(SPECIFICATION)
    SPECIFICATION.loader.exec_module(main)
    return main


@pytest.fixture(scope="module")
def inputs():
    # El fixture conserva las mismas entradas de referencia para que los resultados sean comparables.

    main = load_main()
    return main.load_inputs()


def test_accepts_inputs_similar_to_training_data(inputs):
    # Las entradas esperadas no deben ser bloqueadas por un control demasiado estricto.

    main = load_main()
    training_inputs, new_inputs, _ = inputs
    _, compatible = main.assess_inputs(training_inputs, new_inputs)
    assert compatible


def test_rejects_a_clear_distribution_shift(inputs):
    # Un desplazamiento extremo debe detener el scoring y activar una revisión.

    main = load_main()
    training_inputs, new_inputs, _ = inputs
    shifted_inputs = new_inputs.assign(texture_mean=lambda dataframe: dataframe["texture_mean"] + 100)
    anomaly_rate, compatible = main.assess_inputs(training_inputs, shifted_inputs)
    assert anomaly_rate > main.MAX_ANOMALY_RATE
    assert not compatible
