# Uso: python3 -m unittest tests/test_activity.py

import importlib.util
import unittest
from pathlib import Path


# Se importa el archivo real para que la prueba evalúe exactamente el código que ejecutará el estudiante.

ACTIVITY_DIR = Path(__file__).resolve().parents[1]


def load_main():
    SPECIFICATION = importlib.util.spec_from_file_location(
        "unit_test_main", ACTIVITY_DIR / "src" / "main.py"
    )
    main = importlib.util.module_from_spec(SPECIFICATION)
    SPECIFICATION.loader.exec_module(main)
    return main


class TestFactorySummary(unittest.TestCase):
    def test_aggregates_units_for_each_factory(self):
        # Un ejemplo pequeño hace visible la regla y permite identificar con precisión un resultado incorrecto.

        operations = [
            {"factory_id": 2, "machine_id": 1, "daily_units_produced": 10},
            {"factory_id": 1, "machine_id": 1, "daily_units_produced": 20},
            {"factory_id": 2, "machine_id": 2, "daily_units_produced": 30},
        ]

        summary = load_main().summarize_by_factory(operations)

        self.assertEqual(
            summary,
            [
                {"factory_id": 1, "total_units": 20},
                {"factory_id": 2, "total_units": 40},
            ],
        )

    def test_returns_an_empty_summary_without_operations(self):
        # El caso vacío comprueba que la función conserva un comportamiento definido en un borde frecuente.

        self.assertEqual(load_main().summarize_by_factory([]), [])
