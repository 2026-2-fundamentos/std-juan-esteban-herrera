import importlib
from pathlib import Path

import pandas as pd

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
PROFESSOR_DIR = ACTIVITY_DIR / "professor"
IS_PROFESSOR = any(
    (path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents
) and any(path.name != ".gitkeep" for path in PROFESSOR_DIR.iterdir())
CODE_DIR = ACTIVITY_DIR / ("professor" if IS_PROFESSOR else "src")
SUBMISSION_DIR = ACTIVITY_DIR / "submission"

EXPECTED = {
    "train": {
        "counts": {"negative": 236, "neutral": 1117, "positive": 458},
        "chars": 217702,
        "first": {
            "negative": "The real estate company posted a net loss of +ï¿½  x201a -ï¿½ "
            "59.3 million +ï¿½  x201a -ï¿½ 0.21 per share compared with a net "
            "profit of +ï¿½  x201a -ï¿½ 31 million +ï¿½  x201a -ï¿½ 0.11 per "
            "share for the corresponding quarter of 2007",
            "neutral": "Cardona slowed her vehicle , turned around and returned to the "
            "intersection , where she called 911",
            "positive": "Both operating profit and net sales for the three-month period "
            "increased , respectively from EUR16 .0 m and EUR139m , as "
            "compared to the corresponding quarter in 2006",
        },
        "last": {
            "negative": "HELSINKI Thomson Financial - Shares in Cargotec fell sharply in "
            "early afternoon trade after the cargo handling group posted a "
            "surprise drop in April-June profits , which overshadowed the "
            "large number of new orders received during the three months",
            "neutral": "The RME from Telcontar enables the handset to calculate the best "
            "route and includes support for user-defined routes , feature "
            "navigability and multi-modal routing such as via foot and ferry",
            "positive": "Commission income rose by 25.7 % to EUR 16.1 mn from EUR 12.8 mn "
            "in 2004",
        },
    },
    "test": {
        "counts": {"negative": 67, "neutral": 274, "positive": 112},
        "chars": 54097,
        "first": {
            "negative": "Jan. 6 -- Ford is struggling in the face of slowing truck and SUV "
            "sales and a surfeit of up-to-date , gotta-have cars",
            "neutral": "SHARE REPURCHASE 11.01.2008 In the Helsinki Stock Exchange On "
            "behalf of Sampo plc Danske Bank A-S Helsinki Branc",
            "positive": "Operating profit rose to EUR 13.1 mn from EUR 8.7 mn in the "
            "corresponding period in 2007 representing 7.7 % of net sales",
        },
        "last": {
            "negative": "Operating margin , however , slipped to 14.4 % from 15.1 % , "
            "dragged down by a poor performance in enterprise solutions",
            "neutral": "Besides , as there is no depositor preference in Finland , senior "
            "debt and deposits rank on a par , which is also taken into "
            "consideration , the agency added",
            "positive": "As part of the transaction , M-real and Sappi have also signed a "
            "long-term agreement on the supply of pulp and BCTMP and other "
            "smaller services and supplies",
        },
    },
}


def test_01(monkeypatch):
    for split in EXPECTED:
        (SUBMISSION_DIR / f"{split}_dataset.csv").unlink(missing_ok=True)

    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    importlib.import_module(f"{CODE_DIR.name}.pregunta_01").pregunta_01()

    for split, expected in EXPECTED.items():
        path = SUBMISSION_DIR / f"{split}_dataset.csv"
        assert path.exists()

        df = pd.read_csv(path)
        targets = [
            target for target, count in expected["counts"].items() for _ in range(count)
        ]

        assert df.columns.tolist() == ["phrase", "target"]
        assert len(df) == sum(expected["counts"].values())
        assert df["target"].tolist() == targets
        assert df["phrase"].notna().all()
        assert (df["phrase"] == df["phrase"].str.strip()).all()
        assert df["phrase"].str.len().sum() == expected["chars"]
        for target, phrases in df.groupby("target")["phrase"]:
            assert phrases.iloc[0] == expected["first"][target]
            assert phrases.iloc[-1] == expected["last"][target]
