"""Pruebas de la actividad de limpieza de campañas."""

import pandas as pd


ACTIVITY_DIR = __import__("pathlib").Path(__file__).resolve().parents[1]
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def test_generates_the_three_required_tables():
    """Genera las tres salidas persistentes requeridas."""
    from ..src.pregunta_01 import clean_campaign_data

    clean_campaign_data()

    assert (SUBMISSION_DIR / "client.csv").exists()
    assert (SUBMISSION_DIR / "campaign.csv").exists()
    assert (SUBMISSION_DIR / "economics.csv").exists()


def test_client_table_and_cleaning_rules():
    """Conserva y limpia correctamente los atributos de clientes."""
    client = pd.read_csv(SUBMISSION_DIR / "client.csv")

    assert client.shape == (41188, 7)
    assert client.columns.tolist() == [
        "client_id",
        "age",
        "job",
        "marital",
        "education",
        "credit_default",
        "mortgage",
    ]
    assert not client["job"].str.contains(r"[.-]", regex=True).any()
    assert not client["education"].dropna().str.contains(".", regex=False).any()
    assert client["education"].isna().sum() == 1731
    assert client["credit_default"].value_counts().to_dict() == {0: 41185, 1: 3}
    assert client["mortgage"].value_counts().to_dict() == {1: 21576, 0: 19612}


def test_campaign_table_and_cleaning_rules():
    """Conserva contactos y transforma resultados y fechas."""
    campaign = pd.read_csv(SUBMISSION_DIR / "campaign.csv")

    assert campaign.shape == (41188, 7)
    assert campaign.columns.tolist() == [
        "client_id",
        "number_contacts",
        "contact_duration",
        "previous_campaign_contacts",
        "previous_outcome",
        "campaign_outcome",
        "last_contact_date",
    ]
    assert campaign["previous_outcome"].value_counts().to_dict() == {0: 39815, 1: 1373}
    assert campaign["campaign_outcome"].value_counts().to_dict() == {0: 36548, 1: 4640}
    dates = pd.to_datetime(campaign["last_contact_date"], format="%Y-%m-%d")
    assert dates.min() == pd.Timestamp("2022-03-01")
    assert dates.max() == pd.Timestamp("2022-12-31")


def test_economics_table_preserves_the_expected_fields():
    """Separa las variables económicas sin alterar su grano."""
    economics = pd.read_csv(SUBMISSION_DIR / "economics.csv")

    assert economics.shape == (41188, 3)
    assert economics.columns.tolist() == [
        "client_id",
        "cons_price_idx",
        "euribor_three_months",
    ]
    assert economics["client_id"].is_unique
