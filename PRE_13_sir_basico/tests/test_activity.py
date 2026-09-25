import json
from pathlib import Path

import numpy as np
import pandas as pd


def test_forecasts_conserve_population_and_translate_cases_to_beds():
    forecasts = pd.read_csv("submission/forecasts.csv")

    figure_path = Path("submission/expected_evolution.png")
    assert figure_path.exists()
    assert figure_path.stat().st_size > 0

    assert set(forecasts["scenario"]) == {
        "transmision_actual",
        "transmision_moderada",
        "transmision_alta",
    }
    assert forecasts.groupby("scenario").size().eq(180).all()
    assert (
        forecasts[["susceptible", "infected", "recovered", "deceased"]]
        .ge(0)
        .all()
        .all()
    )
    assert (
        forecasts[["susceptible", "infected", "recovered", "deceased"]]
        .sum(axis=1)
        .sub(100_000)
        .abs()
        .lt(1e-6)
        .all()
    )
    assert np.allclose(forecasts["required_beds"], forecasts["infected"] * 0.05)


def test_peak_summary_matches_forecasts_and_declares_information_cutoff():
    forecasts = pd.read_csv("submission/forecasts.csv")
    peaks = pd.read_csv("submission/scenario_peaks.csv")
    with Path("submission/model_assumptions.json").open(encoding="utf-8") as file:
        assumptions = json.load(file)

    assert assumptions["observation_cutoff_day"] == 59
    assert assumptions["forecast_days"] == 180
    assert assumptions["bed_capacity"] == 1_500
    assert peaks["peak_day"].between(0, 179).all()

    for peak in peaks.itertuples(index=False):
        scenario = forecasts.loc[forecasts["scenario"] == peak.scenario]
        assert peak.peak_active_cases == scenario["infected"].max()
        assert peak.peak_required_beds == scenario["required_beds"].max()
