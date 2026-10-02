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
FILES = ["channel_summary.csv", "yearly_summary.csv", "entry_day_summary.csv"]


def read(name):
    path = SUBMISSION_DIR / name
    assert path.exists()
    return pd.read_csv(path)


def test_01(monkeypatch):
    for name in FILES:
        (SUBMISSION_DIR / name).unlink(missing_ok=True)

    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    importlib.import_module(f"{CODE_DIR.name}.pregunta_01").pregunta_01()

    channels = read("channel_summary.csv")
    assert channels.columns.tolist() == [
        "channel",
        "requests",
        "answered",
        "pending",
        "median_business_days",
        "on_time_rate",
    ]
    assert channels["channel"].tolist() == ["letter", "web"]
    assert channels["requests"].tolist() == [28138, 119005]
    assert channels["answered"].tolist() == [27318, 115539]
    assert channels["pending"].tolist() == [820, 3466]
    assert channels["median_business_days"].tolist() == approx([6.0, 6.0], abs=1e-4)
    assert channels["on_time_rate"].tolist() == approx([0.9467, 0.9453], abs=1e-4)

    yearly = read("yearly_summary.csv")
    assert yearly.columns.tolist() == [
        "year",
        "channel",
        "requests",
        "pending",
        "on_time_rate",
    ]
    assert yearly[["year", "channel"]].values.tolist() == [
        [2016, "letter"],
        [2016, "web"],
        [2017, "letter"],
        [2017, "web"],
        [2018, "letter"],
        [2018, "web"],
        [2019, "letter"],
        [2019, "web"],
        [2020, "letter"],
        [2020, "web"],
        [2021, "letter"],
        [2021, "web"],
    ]
    assert yearly["requests"].tolist() == [
        9559,
        5133,
        4990,
        9905,
        3978,
        13852,
        4066,
        16499,
        2770,
        46288,
        2775,
        27328,
    ]
    assert yearly["pending"].tolist() == [
        269,
        157,
        160,
        293,
        107,
        376,
        127,
        463,
        70,
        1366,
        87,
        811,
    ]
    assert yearly["on_time_rate"].tolist() == approx(
        [
            0.9463,
            0.9408,
            0.9495,
            0.9456,
            0.9497,
            0.948,
            0.9397,
            0.9476,
            0.9502,
            0.945,
            0.9449,
            0.9438,
        ],
        abs=1e-4,
    )

    days = read("entry_day_summary.csv")
    assert days.columns.tolist() == [
        "day_name",
        "requests",
        "median_calendar_days",
        "median_business_days",
    ]
    assert days["day_name"].tolist() == [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    assert days["requests"].tolist() == [27591, 33221, 31065, 28008, 25121, 1434, 703]
    assert days["median_calendar_days"].tolist() == approx(
        [9.0, 9.0, 9.0, 9.0, 9.0, 9.0, 9.0], abs=1e-4
    )
    assert days["median_business_days"].tolist() == approx(
        [7.0, 7.0, 7.0, 6.0, 5.0, 6.0, 7.0], abs=1e-4
    )
