"""Evalúa los artefactos analíticos entregados por el estudiante."""

from pathlib import Path


ACTIVITY_DIR = Path(__file__).resolve().parents[1]

import matplotlib.image as mpimg
import pandas as pd
from pandas.testing import assert_frame_equal


SUMMARY_FILE = ACTIVITY_DIR / "submission/summary.csv"
TOP_DRIVERS_FILE = ACTIVITY_DIR / "submission/top10_drivers.png"


def test_01():
    assert SUMMARY_FILE.is_file(), "Genera submission/summary.csv."
    assert TOP_DRIVERS_FILE.is_file(), "Genera submission/top10_drivers.png."


def test_02():
    summary = pd.read_csv(SUMMARY_FILE)
    drivers = pd.read_csv(ACTIVITY_DIR / "data/drivers.csv")
    timesheet = pd.read_csv(ACTIVITY_DIR / "data/timesheet.csv")

    expected = (
        timesheet.groupby("driverId", as_index=False)[["hours-logged", "miles-logged"]]
        .sum()
        .merge(drivers[["driverId", "name"]], on="driverId")
        .rename(
            columns={
                "driverId": "driver_id",
                "hours-logged": "hours_logged",
                "miles-logged": "miles_logged",
            }
        )
        .sort_values("driver_id")
        .reset_index(drop=True)
    )
    actual = summary.sort_values("driver_id").reset_index(drop=True)

    assert_frame_equal(actual, expected)


def test_03():
    image = mpimg.imread(TOP_DRIVERS_FILE)

    assert image.ndim in {2, 3}
    assert image.shape[0] > 100
    assert image.shape[1] > 100
