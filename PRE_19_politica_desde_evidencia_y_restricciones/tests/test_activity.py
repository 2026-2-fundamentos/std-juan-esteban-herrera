"""Las pruebas se implementarán junto con la solución del taller."""
from pathlib import Path
import importlib.util
import pandas as pd

FOLDER = Path(__file__).resolve().parents[1]


def load_main():
    """Carga src/main.py al ejecutar la prueba para que su ausencia no impida descubrirla."""
    spec = importlib.util.spec_from_file_location("pre03_main", FOLDER / "src" / "main.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_policy_is_feasible_and_traced_to_a_decisor():
    policies = pd.read_csv(FOLDER / "data" / "policy_options.csv")
    chosen = load_main().recommend(policies)
    assert chosen.loc[0, "policy_id"] == "P1"
    assert bool(chosen.loc[0, "feasible"])
    assert chosen.loc[0, "decision_owner"] == "Dirección académica"


def test_capacity_and_minimum_are_checked():
    policies = pd.read_csv(FOLDER / "data" / "policy_options.csv")
    evaluated = load_main().evaluate_policies(policies)
    assert evaluated.capacity_ok.all()
    assert evaluated.minimum_ok.all()
