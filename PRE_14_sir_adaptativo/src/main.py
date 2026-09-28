"""Actualiza un pronóstico SIR cuando cambia la tasa de transmisión."""

import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ACTIVITY_DIR / "data" / "infection_rates.csv"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"
POPULATION = 100_000
INITIAL_INFECTED = 1_000
RECOVERY_RATE = 0.08
DEATH_RATE = 0.001
HOSPITALIZATION_RATE = 0.05
FORECAST_DAYS = 180
MEAN_REVERSION = 0.04


def project_infection_rate(observed_rates, forecast_days=FORECAST_DAYS):
    """Proyecta una tasa que retorna gradualmente a su promedio histórico."""
    long_run_rate = observed_rates.mean()
    last_rate = observed_rates.iloc[-1]
    days = np.arange(forecast_days)
    projected_rates = long_run_rate + (last_rate - long_run_rate) * (1 - MEAN_REVERSION) ** days
    return pd.DataFrame({"forecast_day": days, "infection_rate": projected_rates, "long_run_rate": long_run_rate})


def simulate_sir(infection_rates):
    """Simula SIR con una tasa de infección que puede cambiar cada día."""
    susceptible, infected, recovered, deceased = float(POPULATION - INITIAL_INFECTED), float(INITIAL_INFECTED), 0.0, 0.0
    records = []
    for day, infection_rate in enumerate(infection_rates):
        records.append({"forecast_day": day, "infection_rate": infection_rate, "susceptible": susceptible, "infected": infected, "recovered": recovered, "deceased": deceased, "required_beds": infected * HOSPITALIZATION_RATE})
        new_infections = infection_rate * infected * susceptible / POPULATION
        new_recoveries = RECOVERY_RATE * infected
        new_deaths = DEATH_RATE * infected
        susceptible -= new_infections
        infected += new_infections - new_recoveries - new_deaths
        recovered += new_recoveries
        deceased += new_deaths
    return pd.DataFrame(records)


def main():
    observed = pd.read_csv(DATA_PATH)
    rate_forecast = project_infection_rate(observed["infection_rate"])
    adaptive_forecast = simulate_sir(rate_forecast["infection_rate"])
    static_forecast = simulate_sir(np.repeat(observed["infection_rate"].iloc[-1], FORECAST_DAYS))
    adaptive_forecast["model"] = "tasa_adaptativa"
    static_forecast["model"] = "tasa_estatica"
    forecasts = pd.concat([static_forecast, adaptive_forecast], ignore_index=True)
    peaks = forecasts.loc[forecasts.groupby("model")["infected"].idxmax(), ["model", "forecast_day", "infected", "required_beds", "infection_rate"]].rename(columns={"forecast_day": "peak_day", "infected": "peak_active_cases", "required_beds": "peak_required_beds", "infection_rate": "rate_at_peak"})
    SUBMISSION_DIR.mkdir(exist_ok=True)
    rate_forecast.to_csv(SUBMISSION_DIR / "infection_rate_forecast.csv", index=False)
    forecasts.to_csv(SUBMISSION_DIR / "forecasts.csv", index=False)
    peaks.to_csv(SUBMISSION_DIR / "scenario_peaks.csv", index=False)
    figure, axes = plt.subplots(1, 2, figsize=(11, 4))
    axes[0].plot(observed["day"], observed["infection_rate"], marker="o", label="tasa observada")
    axes[0].plot(observed["day"].max() + 1 + rate_forecast["forecast_day"], rate_forecast["infection_rate"], label="tasa proyectada")
    axes[0].axhline(rate_forecast["long_run_rate"].iloc[0], color="black", linestyle="--", label="promedio histórico")
    axes[0].set(title="Tasa de transmisión adaptativa", xlabel="Día", ylabel="Tasa")
    axes[0].grid(alpha=0.3)
    axes[0].legend()
    for model, forecast in forecasts.groupby("model"):
        axes[1].plot(forecast["forecast_day"], forecast["infected"], label=model.replace("_", " "))
    axes[1].set(title="Evolución esperada de casos activos", xlabel="Día desde el corte", ylabel="Casos activos")
    axes[1].grid(alpha=0.3)
    axes[1].legend()
    figure.tight_layout()
    figure.savefig(SUBMISSION_DIR / "adaptive_evolution.png", dpi=150)
    plt.close(figure)
    with (SUBMISSION_DIR / "model_assumptions.json").open("w", encoding="utf-8") as file:
        json.dump({"population": POPULATION, "initial_infected": INITIAL_INFECTED, "forecast_days": FORECAST_DAYS, "recovery_rate": RECOVERY_RATE, "death_rate": DEATH_RATE, "hospitalization_rate": HOSPITALIZATION_RATE, "mean_reversion": MEAN_REVERSION, "long_run_infection_rate": rate_forecast["long_run_rate"].iloc[0]}, file, indent=2)


if __name__ == "__main__":
    main()
