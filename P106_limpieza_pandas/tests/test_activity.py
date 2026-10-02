"""Evalúa el archivo limpio entregado por el estudiante."""

from pathlib import Path

import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
SUBMISSION_FILE = ACTIVITY_DIR / "submission" / "ventas.csv"
EXPECTED_COLUMNS = [
    "supplier_id",
    "supplier",
    "country",
    "city",
    "purchase_date",
    "amount",
    "discount",
    "weight",
    "units",
    "unit_price",
    "contact_email",
]


def test_01():
    assert SUBMISSION_FILE.is_file(), "Genera submission/ventas.csv con los datos limpios."

    sales = pd.read_csv(SUBMISSION_FILE)

    assert list(sales.columns) == EXPECTED_COLUMNS
    assert not sales.empty
    assert sales["country"].eq("COL").all()
    assert sales["supplier"].eq(sales["supplier"].str.strip()).all()
    assert not sales["supplier"].str.contains(r"\s{2,}", regex=True).any()
    assert sales["city"].isin({"Bogotá", "Medellín", "Sopó", "Tenjo"}).all()
    assert sales["purchase_date"].str.fullmatch(r"\d{4}-\d{2}-\d{2}").all()
    assert sales["discount"].dropna().between(0, 1).all()
    assert sales["weight"].dropna().ge(0).all()
