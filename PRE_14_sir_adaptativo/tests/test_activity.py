"""Verifica los pronósticos adaptativos del taller."""

import json
from pathlib import Path

import numpy as np
import pandas as pd


def test_projected_rate_returns_gradually_to_its_historical_mean():
    observed = pd.read_csv("data/infection_rates.csv")
    rates = pd.read_csv("submission/infection_rate_forecast.csv")
    assert len(rates) == 180
    assert rates["forecast_day"].tolist() == list(range(180))
    assert np.isclose(rates.loc[0, "infection_rate"], observed["infection_rate"].iloc[-1])
    long_run_rate = observed["infection_rate"].mean()
    assert np.isclose(rates["long_run_rate"].iloc[0], long_run_rate)
    assert abs(rates["infection_rate"].iloc[-1] - long_run_rate) < abs(rates["infection_rate"].iloc[0] - long_run_rate)


def test_adaptive_forecast_is_complete_and_conserves_population():
    forecasts = pd.read_csv("submission/forecasts.csv")
    peaks = pd.read_csv("submission/scenario_peaks.csv")
    assumptions = json.loads(Path("submission/model_assumptions.json").read_text())
    assert set(forecasts["model"]) == {"tasa_estatica", "tasa_adaptativa"}
    assert forecasts.groupby("model").size().to_dict() == {"tasa_adaptativa": 180, "tasa_estatica": 180}
    assert np.allclose(forecasts[["susceptible", "infected", "recovered", "deceased"]].sum(axis=1), assumptions["population"])
    assert (forecasts["infected"] >= 0).all()
    assert np.allclose(forecasts["required_beds"], forecasts["infected"] * assumptions["hospitalization_rate"])
    assert set(peaks["model"]) == {"tasa_estatica", "tasa_adaptativa"}
    assert Path("submission/adaptive_evolution.png").stat().st_size > 0
