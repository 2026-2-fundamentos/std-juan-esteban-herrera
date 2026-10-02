import importlib
from pathlib import Path

import pandas as pd
import pytest

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
PROFESSOR_DIR = ACTIVITY_DIR / "professor"
IS_PROFESSOR = any(
    (path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents
) and any(path.name != ".gitkeep" for path in PROFESSOR_DIR.iterdir())
CODE_DIR = ACTIVITY_DIR / ("professor" if IS_PROFESSOR else "src")
SUBMISSION_DIR = ACTIVITY_DIR / "submission"
FILES = ["client.csv", "campaign.csv", "economics.csv"]


def read(name):
    path = SUBMISSION_DIR / name
    assert path.exists()
    return pd.read_csv(path).sort_values("client_id").reset_index(drop=True)


def test_01(monkeypatch):
    for name in FILES:
        (SUBMISSION_DIR / name).unlink(missing_ok=True)

    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    importlib.import_module(f"{CODE_DIR.name}.pregunta_01").clean_campaign_data()

    client = read("client.csv")
    campaign = read("campaign.csv")
    economics = read("economics.csv")

    for df in [client, campaign, economics]:
        assert df["client_id"].tolist() == list(range(41188))

    assert client.columns.tolist() == [
        "client_id",
        "age",
        "job",
        "marital",
        "education",
        "credit_default",
        "mortgage",
    ]
    assert client["age"].sum() == 1648511
    assert client["job"].value_counts().to_dict() == {
        "admin": 10422,
        "blue_collar": 9254,
        "technician": 6743,
        "services": 3969,
        "management": 2924,
        "retired": 1720,
        "entrepreneur": 1456,
        "self_employed": 1421,
        "housemaid": 1060,
        "unemployed": 1014,
        "student": 875,
        "unknown": 330,
    }
    assert client["marital"].value_counts().to_dict() == {
        "married": 24928,
        "single": 11568,
        "divorced": 4612,
        "unknown": 80,
    }
    assert client["education"].isna().sum() == 1731
    assert client["education"].value_counts().to_dict() == {
        "university_degree": 12168,
        "high_school": 9515,
        "basic_9y": 6045,
        "professional_course": 5243,
        "basic_4y": 4176,
        "basic_6y": 2292,
        "illiterate": 18,
    }
    assert set(client["credit_default"]) == {0, 1}
    assert client["credit_default"].sum() == 3
    assert set(client["mortgage"]) == {0, 1}
    assert client["mortgage"].sum() == 21576
    assert client.iloc[0].tolist() == [0, 56, "housemaid", "married", "basic_4y", 0, 0]
    assert client.iloc[-1].tolist() == [
        41187,
        74,
        "retired",
        "married",
        "professional_course",
        0,
        1,
    ]

    assert campaign.columns.tolist() == [
        "client_id",
        "number_contacts",
        "contact_duration",
        "previous_campaign_contacts",
        "previous_outcome",
        "campaign_outcome",
        "last_contact_date",
    ]
    assert campaign["number_contacts"].sum() == 105754
    assert campaign["contact_duration"].sum() == 10638243
    assert campaign["previous_campaign_contacts"].sum() == 7124
    assert set(campaign["previous_outcome"]) == {0, 1}
    assert campaign["previous_outcome"].sum() == 1373
    assert set(campaign["campaign_outcome"]) == {0, 1}
    assert campaign["campaign_outcome"].sum() == 4640
    assert campaign["last_contact_date"].str.fullmatch(r"2022-\d{2}-\d{2}").all()
    assert campaign["last_contact_date"].str[
        :7
    ].value_counts().sort_index().to_dict() == {
        "2022-03": 546,
        "2022-04": 2632,
        "2022-05": 13769,
        "2022-06": 5318,
        "2022-07": 7174,
        "2022-08": 6178,
        "2022-09": 570,
        "2022-10": 718,
        "2022-11": 4101,
        "2022-12": 182,
    }
    assert campaign.iloc[0].tolist() == [0, 1, 261, 0, 0, 0, "2022-05-13"]
    assert campaign.iloc[-1].tolist() == [41187, 3, 239, 1, 0, 0, "2022-11-23"]

    assert economics.columns.tolist() == [
        "client_id",
        "cons_price_idx",
        "euribor_three_months",
    ]
    assert economics["cons_price_idx"].sum() == pytest.approx(3854194.464, abs=1e-4)
    assert economics["euribor_three_months"].sum() == pytest.approx(
        149153.726, abs=1e-4
    )
    assert economics.iloc[0].tolist() == pytest.approx([0, 93.994, 4.857], abs=1e-4)
    assert economics.iloc[-1].tolist() == pytest.approx(
        [41187, 94.767, 1.028], abs=1e-4
    )
