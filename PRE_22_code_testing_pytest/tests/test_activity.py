# Uso: python3 -m pytest -q tests/test_activity.py

import importlib.util
from pathlib import Path

import pandas as pd
import pytest


# Se importa el módulo real para que pytest revise el mismo código que se ejecutará en el taller.

ACTIVITY_DIR = Path(__file__).resolve().parents[1]


def load_main():
    SPECIFICATION = importlib.util.spec_from_file_location(
        "pytest_pandas_main", ACTIVITY_DIR / "src" / "main.py"
    )
    main = importlib.util.module_from_spec(SPECIFICATION)
    SPECIFICATION.loader.exec_module(main)
    return main


def test_builds_totals_for_certified_drivers_only():
    # Un conjunto pequeño permite verificar qué conductores entran al indicador y por qué.

    drivers = pd.DataFrame(
        {
            "driverId": [10, 11, 12],
            "name": ["Ana", "Bruno", "Carla"],
            "certified": ["Y", "N", "Y"],
        }
    )
    timesheet = pd.DataFrame(
        {
            "driverId": [10, 10, 11, 12],
            "hours-logged": [8, 7, 9, 6],
            "miles-logged": [120, 100, 140, 90],
        }
    )

    summary = load_main().build_certified_driver_totals(drivers, timesheet)

    expected = [
        {
            "driverId": 10,
            "name": "Ana",
            "total_hours": 15,
            "total_miles": 220,
        },
        {
            "driverId": 12,
            "name": "Carla",
            "total_hours": 6,
            "total_miles": 90,
        },
    ]
    assert summary.to_dict(orient="records") == expected


def test_rejects_a_timesheet_without_required_columns():
    # Una entrada incompleta debe fallar antes de producir un resumen engañoso.

    drivers = pd.DataFrame(
        {"driverId": [10], "name": ["Ana"], "certified": ["Y"]}
    )
    timesheet = pd.DataFrame({"driverId": [10], "hours-logged": [8]})

    with pytest.raises(ValueError, match="turnos"):
        load_main().build_certified_driver_totals(drivers, timesheet)
