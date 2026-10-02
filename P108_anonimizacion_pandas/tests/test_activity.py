"""Evaluación del artefacto de anonimización entregado por el estudiante."""

from pathlib import Path

import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
SUBMISSION_FILE = ACTIVITY_DIR / "submission" / "anonymized.csv"
RAW_FILE = ACTIVITY_DIR / "data" / "raw.csv"


def test_01():
    assert SUBMISSION_FILE.is_file(), "Debe entregar submission/anonymized.csv."


def test_02():
    anonymized = pd.read_csv(SUBMISSION_FILE)
    raw = pd.read_csv(RAW_FILE)

    assert len(anonymized) == 600
    assert list(anonymized.columns) == [
        "loyalty_card_number",
        "annual_spend",
        "customer_id",
        "age_group",
        "region",
        "occupation_group",
    ]
    assert anonymized["annual_spend"].tolist() == raw["annual_spend"].tolist()
    assert anonymized["loyalty_card_number"].tolist() == (
        "********" + raw["loyalty_card_number"].astype(str).str.zfill(12).str[-4:]
    ).tolist()


def test_03():
    anonymized = pd.read_csv(SUBMISSION_FILE)

    prohibited_columns = {
        "name",
        "document_id",
        "email",
        "age",
        "city",
        "occupation",
    }
    assert prohibited_columns.isdisjoint(anonymized.columns)
    assert anonymized["loyalty_card_number"].astype(str).str.fullmatch(r"\*{8}\d{4}").all()
    assert anonymized["customer_id"].astype(str).str.fullmatch(r"CUST-[0-9A-F]{12}").all()
    assert anonymized["customer_id"].is_unique


def test_04():
    anonymized = pd.read_csv(SUBMISSION_FILE)

    assert set(anonymized["age_group"]) <= {"20-29", "30-39", "40-49", "50-59", "60-69"}
    assert set(anonymized["region"]) <= {"Andina", "Caribe", "Pacífica"}
    assert set(anonymized["occupation_group"]) <= {
        "Comercio y oficios",
        "Salud y educación",
        "Servicios profesionales",
        "Tecnología y diseño",
    }
    assert anonymized[["annual_spend", "age_group", "region", "occupation_group"]].notna().all().all()
