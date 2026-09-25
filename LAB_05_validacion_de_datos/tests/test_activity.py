"""Pruebas de calificación automática para LAB_05_validacion_de_datos."""

import json
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT / "submission" / "data_quality_report.json"


def test_01_normalizes_headers_and_identifies_structure_problems():
    """Las reglas de estructura deben ser independientes de los datos reales."""
    from ..src.pregunta_01 import normalize_column_name, validate_required_columns

    assert normalize_column_name("\ufeff Supplier ID ") == "supplier_id"

    result = validate_required_columns(
        pd.DataFrame(columns=["supplier_id", "supplier", "extra"]),
        ["supplier_id", "supplier", "country"],
    )

    assert result == {
        "missing_required_columns": ["country"],
        "unexpected_columns": ["extra"],
    }


def test_02_builds_a_complete_quality_report_for_the_sales_data():
    """El reporte debe contener evidencia verificable de los problemas reales."""
    from ..src.pregunta_01 import REQUIRED_COLUMNS, main

    report = main()

    assert report["row_count"] == 103
    assert report["column_count"] == len(REQUIRED_COLUMNS)
    assert report["missing_required_columns"] == []
    assert report["unexpected_columns"] == []
    assert report["duplicate_row_count"] == 2
    assert report["duplicate_supplier_id_row_count"] == 6
    assert report["missing_value_count_by_column"] == {
        "supplier_id": 0,
        "supplier": 0,
        "country": 0,
        "city": 0,
        "purchase_date": 0,
        "amount": 24,
        "discount": 35,
        "weight": 30,
        "units": 2,
        "unit_price": 0,
        "contact_email": 0,
    }
    assert report["invalid_email_count"] == 11
    assert report["invalid_unit_count"] == 0
    assert report["country_values"] == [
        " Colombia ",
        "CO",
        "COL",
        "COLOMBIA",
        "Colombia",
        "colombia",
    ]


def test_03_writes_the_permanent_report_in_submission():
    """La entrega debe ser un JSON legible y equivalente al resultado calculado."""
    from ..src.pregunta_01 import main

    OUTPUT_FILE.unlink(missing_ok=True)
    report = main()

    assert OUTPUT_FILE.exists()
    assert json.loads(OUTPUT_FILE.read_text(encoding="utf-8")) == report


def test_04_marks_invalid_emails_and_non_positive_or_fractional_units():
    """Las reglas de negocio deben detectar valores inválidos en datos pequeños."""
    from ..src.pregunta_01 import REQUIRED_COLUMNS, build_quality_report

    dataframe = pd.DataFrame(
        {
            column: ["value", "value"] for column in REQUIRED_COLUMNS
        }
    )
    dataframe["contact_email"] = ["valid@example.com", "invalid-email"]
    dataframe["units"] = ["2", "1.5"]
    dataframe["supplier_id"] = ["A", "A"]
    dataframe["country"] = ["COL", "CO"]

    report = build_quality_report(dataframe)

    assert report["invalid_email_count"] == 1
    assert report["invalid_unit_count"] == 1
    assert report["duplicate_supplier_id_row_count"] == 2
