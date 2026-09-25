# Uso: python3 -m pytest -q tests/test_activity.py

import importlib.util
from pathlib import Path

import pandas as pd
import pytest

ACTIVITY_DIR = Path(__file__).resolve().parents[1]


def load_main():
    SPECIFICATION = importlib.util.spec_from_file_location(
        "data_testing_main", ACTIVITY_DIR / "src" / "main.py"
    )
    main = importlib.util.module_from_spec(SPECIFICATION)
    SPECIFICATION.loader.exec_module(main)
    return main


def test_accepts_the_clean_export():
    ACTIVITY_DIR = Path(__file__).resolve().parents[1]

    dataframe = pd.read_csv(ACTIVITY_DIR / "data" / "machine_throughput_export.csv")
    assert load_main().validate_data(dataframe) == []


@pytest.mark.parametrize(
    ("dataset_name", "expected_violation"),
    [
        (
            "invalid_negative_production.csv",
            "daily_units_produced no puede ser negativo.",
        ),
        ("invalid_duplicate_key.csv", "debe ser única."),
        ("invalid_date.csv", "factory_date debe contener fechas válidas."),
        ("invalid_schema.csv", "El esquema no coincide con el contrato esperado."),
    ],
)
def test_rejects_each_contract_violation(dataset_name, expected_violation):

    ACTIVITY_DIR = Path(__file__).resolve().parents[1]

    violations = load_main().validate_data(pd.read_csv(ACTIVITY_DIR / "data" / dataset_name))
    assert any(expected_violation in violation for violation in violations)
