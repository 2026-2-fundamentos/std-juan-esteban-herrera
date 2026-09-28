"""Construye los pronósticos y entregables del taller SIR básico."""

import json
from pathlib import Path

import matplotlib
import numpy as np
import pandas as pd

matplotlib.use("Agg")
import matplotlib.pyplot as plt


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ACTIVITY_DIR / "data" / "observed_active_cases.csv"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"

POPULATION = 100_000
RECOVERY_RATE = 0.08
DEATH_RATE = 0.001
HOSPITALIZATION_RATE = 0.05
BED_CAPACITY = 1_500
FORECAST_DAYS = 180


def simulate_sir(infection_rate, initial_infected, forecast_days=FORECAST_DAYS):
    """Simula compartimentos SIR con fallecimientos y conserva la población."""
    susceptible = float(POPULATION - initial_infected)
    infected = float(initial_infected)
    recovered = 0.0
    deceased = 0.0
    records = []

    for day in range(forecast_days):
        records.append(
            {
                "day": day,
                "susceptible": susceptible,
                "infected": infected,
                "recovered": recovered,
                "deceased": deceased,
            }
        )
        new_infections = infection_rate * infected * susceptible / POPULATION
        new_recoveries = RECOVERY_RATE * infected
        new_deaths = DEATH_RATE * infected
        susceptible -= new_infections
        infected += new_infections - new_recoveries - new_deaths
        recovered += new_recoveries
        deceased += new_deaths

    return pd.DataFrame(records)


def select_baseline_rate(observed):
    """Selecciona la tasa constante que mejor reproduce los días observados."""
    candidates = np.round(np.arange(0.10, 0.41, 0.01), 2)
    comparison = []
    initial_infected = observed.loc[0, "active_cases"]
    for infection_rate in candidates:
        simulation = simulate_sir(
            infection_rate,
            initial_infected,
            forecast_days=len(observed),
        )
        mse = ((simulation["infected"] - observed["active_cases"]) ** 2).mean()
        comparison.append({"infection_rate": infection_rate, "observed_mse": mse})
    comparison = pd.DataFrame(comparison)
    baseline_rate = comparison.loc[comparison["observed_mse"].idxmin(), "infection_rate"]
    return float(baseline_rate), comparison


def main():
    observed = pd.read_csv(DATA_PATH)
    baseline_rate, fit_comparison = select_baseline_rate(observed)
    initial_infected = observed.loc[0, "active_cases"]
    scenarios = {
        "transmision_actual": baseline_rate,
        "transmision_moderada": baseline_rate * 0.75,
        "transmision_alta": baseline_rate * 1.15,
    }

    forecasts = []
    peaks = []
    for scenario, infection_rate in scenarios.items():
        simulation = simulate_sir(infection_rate, initial_infected)
        simulation["scenario"] = scenario
        simulation["infection_rate"] = infection_rate
        simulation["required_beds"] = simulation["infected"] * HOSPITALIZATION_RATE
        forecasts.append(simulation)
        peak = simulation.loc[simulation["infected"].idxmax()]
        peaks.append(
            {
                "scenario": scenario,
                "infection_rate": infection_rate,
                "peak_day": int(peak["day"]),
                "peak_active_cases": peak["infected"],
                "peak_required_beds": peak["required_beds"],
                "bed_capacity": BED_CAPACITY,
                "bed_gap": peak["required_beds"] - BED_CAPACITY,
            }
        )

    SUBMISSION_DIR.mkdir(exist_ok=True)
    pd.concat(forecasts, ignore_index=True).to_csv(
        SUBMISSION_DIR / "forecasts.csv", index=False
    )
    forecasts_dataframe = pd.concat(forecasts, ignore_index=True)
    figure, axis = plt.subplots(figsize=(9, 5))
    for scenario, scenario_forecast in forecasts_dataframe.groupby("scenario"):
        axis.plot(
            scenario_forecast["day"],
            scenario_forecast["infected"],
            label=scenario.replace("_", " "),
        )
    axis.scatter(
        observed["day"],
        observed["active_cases"],
        color="black",
        s=14,
        label="casos observados",
        zorder=3,
    )
    axis.axvline(
        observed["day"].max(),
        color="black",
        linestyle="--",
        label="corte de información",
    )
    axis.set(
        title="Evolución esperada de casos activos",
        xlabel="Día",
        ylabel="Casos activos",
    )
    axis.grid(alpha=0.3)
    axis.legend()
    figure.tight_layout()
    figure.savefig(SUBMISSION_DIR / "expected_evolution.png", dpi=150)
    plt.close(figure)
    pd.DataFrame(peaks).to_csv(SUBMISSION_DIR / "scenario_peaks.csv", index=False)
    fit_comparison.to_csv(SUBMISSION_DIR / "fit_comparison.csv", index=False)
    with (SUBMISSION_DIR / "model_assumptions.json").open("w", encoding="utf-8") as file:
        json.dump(
            {
                "population": POPULATION,
                "observation_cutoff_day": int(observed["day"].max()),
                "forecast_days": FORECAST_DAYS,
                "recovery_rate": RECOVERY_RATE,
                "death_rate": DEATH_RATE,
                "hospitalization_rate": HOSPITALIZATION_RATE,
                "bed_capacity": BED_CAPACITY,
                "baseline_infection_rate": baseline_rate,
            },
            file,
            indent=2,
        )


if __name__ == "__main__":
    main()
