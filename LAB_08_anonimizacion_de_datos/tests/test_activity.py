"""Pruebas de la actividad de anonimización."""

from pathlib import Path

import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
SUBMISSION_FILE = ACTIVITY_DIR / "submission" / "anonymized.csv"


def test_generates_the_anonymized_file():
    """Genera una entrega persistente con el mismo número de registros."""
    from ..src.pregunta_01 import anonymize_customers

    anonymize_customers()

    raw = pd.read_csv(DATA_DIR / "raw.csv")
    anonymized = pd.read_csv(SUBMISSION_FILE)

    assert SUBMISSION_FILE.exists()
    assert anonymized.shape == (len(raw), 6)
    assert anonymized.columns.tolist() == [
        "loyalty_card_number",
        "annual_spend",
        "customer_id",
        "age_group",
        "region",
        "occupation_group",
    ]


def test_suppresses_direct_identifiers_and_preserves_spend():
    """Elimina identificadores directos y conserva la medida analítica."""
    raw = pd.read_csv(DATA_DIR / "raw.csv")
    anonymized = pd.read_csv(SUBMISSION_FILE)

    assert not {"name", "document_id", "email", "age", "city", "occupation"} & set(
        anonymized.columns
    )
    assert anonymized["annual_spend"].equals(raw["annual_spend"])


def test_masks_card_numbers_and_pseudonymizes_documents():
    """Oculta números de tarjeta y sustituye documentos por seudónimos estables."""
    raw = pd.read_csv(DATA_DIR / "raw.csv")
    anonymized = pd.read_csv(SUBMISSION_FILE)

    assert anonymized["loyalty_card_number"].str.fullmatch(r"\*{8}\d{4}").all()
    assert (
        anonymized["loyalty_card_number"].str[-4].equals(
            raw["loyalty_card_number"].astype(str).str.zfill(12).str[-4]
        )
    )
    assert anonymized["customer_id"].str.fullmatch(r"CUST-[0-9A-F]{12}").all()
    assert anonymized["customer_id"].is_unique


def test_generalizes_quasi_identifiers():
    """Convierte edad, ubicación y ocupación en grupos autorizados."""
    anonymized = pd.read_csv(SUBMISSION_FILE)

    assert set(anonymized["age_group"]) == {
        "20-29",
        "30-39",
        "40-49",
        "50-59",
        "60-69",
    }
    assert set(anonymized["region"]) == {"Andina", "Caribe", "Pacífica"}
    assert set(anonymized["occupation_group"]) == {
        "Comercio y oficios",
        "Salud y educación",
        "Servicios profesionales",
        "Tecnología y diseño",
    }


def test_prevents_unique_reidentification_with_auxiliary_data():
    """Ningún perfil público queda asociado con una única fila publicada."""
    anonymized = pd.read_csv(SUBMISSION_FILE)
    auxiliary = pd.read_csv(DATA_DIR / "auxiliary.csv")

    age_group = pd.cut(
        auxiliary["age"],
        bins=[20, 30, 40, 50, 60, 70],
        labels=["20-29", "30-39", "40-49", "50-59", "60-69"],
        right=False,
    )
    city_to_region = {
        "Medellín": "Andina",
        "Bello": "Andina",
        "Envigado": "Andina",
        "Itagüí": "Andina",
        "Rionegro": "Andina",
        "Bogotá": "Andina",
        "Cali": "Pacífica",
        "Barranquilla": "Caribe",
        "Manizales": "Andina",
        "Pereira": "Andina",
        "Cartagena": "Caribe",
        "Bucaramanga": "Andina",
    }
    occupation_to_group = {
        "Administradora": "Servicios profesionales",
        "Abogada": "Servicios profesionales",
        "Analista financiera": "Servicios profesionales",
        "Contadora": "Servicios profesionales",
        "Arquitecta": "Tecnología y diseño",
        "Diseñadora gráfica": "Tecnología y diseño",
        "Ingeniero de sistemas": "Tecnología y diseño",
        "Médico": "Salud y educación",
        "Enfermera": "Salud y educación",
        "Docente": "Salud y educación",
        "Comerciante": "Comercio y oficios",
        "Técnico electricista": "Comercio y oficios",
    }
    attack = auxiliary.assign(
        age_group=age_group,
        region=auxiliary["city"].map(city_to_region),
        occupation_group=auxiliary["occupation"].map(occupation_to_group),
    )
    candidates = attack.merge(
        anonymized,
        on=["age_group", "region", "occupation_group"],
        how="inner",
    )
    matches_per_profile = candidates.groupby("name").size().reindex(
        auxiliary["name"],
        fill_value=0,
    )

    assert not matches_per_profile.eq(1).any()
