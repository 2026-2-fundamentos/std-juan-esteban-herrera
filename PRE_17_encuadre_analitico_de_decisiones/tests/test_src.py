"""Las pruebas se implementarán junto con la solución del taller."""
from pathlib import Path
import importlib.util

import pandas as pd

FOLDER = Path(__file__).resolve().parents[1]


def load_main():
    """Carga src/main.py al ejecutar la prueba para que su ausencia no impida descubrirla."""
    spec = importlib.util.spec_from_file_location("pre01_main", FOLDER / "src" / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_recommendation_is_feasible_and_traceable():
    options = pd.read_csv(FOLDER / "data" / "policy_options.csv")
    brief = load_main().make_decision_brief(options)

    assert brief.loc[0, "policy_id"] == "P2"
    assert bool(brief.loc[0, "capacity_ok"])
    assert bool(brief.loc[0, "exposure_ok"])
    assert brief.loc[0, "decision_owner"] == "Responsable comercial"


def test_infeasible_policy_is_not_recommended():
    options = pd.read_csv(FOLDER / "data" / "policy_options.csv")
    evaluated = load_main().evaluate_policies(options)

    assert not bool(evaluated.loc[evaluated.policy_id == "P3", "feasible"].iloc[0])
    assert load_main().make_decision_brief(options).loc[0, "policy_id"] != "P3"
