import importlib
from pathlib import Path

import pandas as pd
from pytest import approx

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
PROFESSOR_DIR = ACTIVITY_DIR / "professor"
IS_PROFESSOR = any(
    (path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents
) and any(path.name != ".gitkeep" for path in PROFESSOR_DIR.iterdir())
CODE_DIR = ACTIVITY_DIR / ("professor" if IS_PROFESSOR else "src")
SUBMISSION_DIR = ACTIVITY_DIR / "submission"
FILES = ["hourly_delay_rates.csv", "carrier_adjusted_delays.csv"]


def read(name):
    path = SUBMISSION_DIR / name
    assert path.exists()
    return pd.read_csv(path)


def test_01(monkeypatch):
    for name in FILES:
        (SUBMISSION_DIR / name).unlink(missing_ok=True)

    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    importlib.import_module(f"{CODE_DIR.name}.pregunta_01").pregunta_01()

    hourly = read("hourly_delay_rates.csv")
    assert hourly.columns.tolist() == [
        "scheduled_departure_hour",
        "operated_flights",
        "delayed_departure_15_flights",
        "delay_rate",
    ]
    assert hourly["scheduled_departure_hour"].tolist() == list(range(24))
    assert hourly["operated_flights"].tolist() == [
        27936,
        10890,
        2682,
        1163,
        2240,
        134690,
        1477488,
        1460561,
        1469128,
        1383927,
        1347549,
        1396135,
        1328972,
        1374703,
        1322080,
        1286299,
        1351682,
        1416039,
        1261521,
        1210173,
        837079,
        708382,
        261083,
        114529,
    ]
    assert hourly["delayed_departure_15_flights"].tolist() == [
        4499,
        1789,
        349,
        286,
        290,
        8018,
        92846,
        123254,
        162486,
        190213,
        218235,
        247595,
        259957,
        298747,
        312963,
        328925,
        363937,
        407044,
        374755,
        368607,
        267606,
        204753,
        61341,
        26458,
    ]
    assert hourly["delay_rate"].tolist() == approx(
        [
            0.161,
            0.1643,
            0.1301,
            0.2459,
            0.1295,
            0.0595,
            0.0628,
            0.0844,
            0.1106,
            0.1374,
            0.1619,
            0.1773,
            0.1956,
            0.2173,
            0.2367,
            0.2557,
            0.2692,
            0.2875,
            0.2971,
            0.3046,
            0.3197,
            0.289,
            0.2349,
            0.231,
        ],
        abs=1e-4,
    )

    carriers = read("carrier_adjusted_delays.csv")
    assert carriers.columns.tolist() == [
        "reporting_airline",
        "operated_flights",
        "delayed_departure_15_flights",
        "delay_rate",
        "expected_delayed_flights",
        "observed_to_expected_ratio",
        "crude_rank",
        "adjusted_rank",
    ]
    assert carriers["reporting_airline"].tolist() == [
        "EV",
        "MQ",
        "AA",
        "UA",
        "OH",
        "B6",
        "YV",
        "CO",
        "AS",
        "WN",
        "XE",
        "FL",
        "US",
        "OO",
        "DL",
        "NW",
        "F9",
        "9E",
        "HA",
    ]
    assert carriers["operated_flights"].tolist() == [
        819223,
        1520162,
        1836848,
        1406817,
        689489,
        535699,
        824006,
        922693,
        463559,
        3438613,
        1220245,
        755709,
        1422845,
        1673682,
        1412877,
        1179484,
        282100,
        506020,
        169113,
    ]
    assert carriers["delayed_departure_15_flights"].tolist() == [
        230689,
        352450,
        421120,
        317803,
        150917,
        118591,
        181836,
        194198,
        96411,
        719230,
        245565,
        150631,
        263816,
        298674,
        239256,
        199494,
        47891,
        77928,
        8066,
    ]
    assert carriers["delay_rate"].tolist() == approx(
        [
            0.2816,
            0.2319,
            0.2293,
            0.2259,
            0.2189,
            0.2214,
            0.2207,
            0.2105,
            0.208,
            0.2092,
            0.2012,
            0.1993,
            0.1854,
            0.1785,
            0.1693,
            0.1691,
            0.1698,
            0.154,
            0.0477,
        ],
        abs=1e-4,
    )
    assert carriers["expected_delayed_flights"].tolist() == approx(
        [
            165686.2991,
            306006.666,
            371425.646,
            282334.284,
            140965.7374,
            110787.2441,
            170542.6602,
            184758.0031,
            95953.3357,
            716251.5503,
            246090.3006,
            157041.8202,
            292180.7196,
            340515.0587,
            285980.5933,
            239947.7382,
            58176.3309,
            104794.0865,
            34052.5105,
        ],
        abs=1e-4,
    )
    assert carriers["observed_to_expected_ratio"].tolist() == approx(
        [
            1.3923,
            1.1518,
            1.1338,
            1.1256,
            1.0706,
            1.0704,
            1.0662,
            1.0511,
            1.0048,
            1.0042,
            0.9979,
            0.9592,
            0.9029,
            0.8771,
            0.8366,
            0.8314,
            0.8232,
            0.7436,
            0.2369,
        ],
        abs=1e-4,
    )
    assert carriers["crude_rank"].tolist() == [
        1,
        2,
        3,
        4,
        7,
        5,
        6,
        8,
        10,
        9,
        11,
        12,
        13,
        14,
        16,
        17,
        15,
        18,
        19,
    ]
    assert carriers["adjusted_rank"].tolist() == list(range(1, 20))
