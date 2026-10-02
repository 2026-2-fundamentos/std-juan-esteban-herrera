from pathlib import Path

import pandas as pd


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def test_01_submission_contains_a_decision_brief():
    assert (SUBMISSION_DIR / "decision_brief.csv").is_file(), (
        "Genera submission/decision_brief.csv con la decisión recomendada."
    )


def test_02_submission_contains_a_policy_contract():
    contract_path = SUBMISSION_DIR / "policy_contract.csv"
    assert contract_path.is_file(), (
        "Genera submission/policy_contract.csv con el contrato de la política."
    )

    contract = pd.read_csv(contract_path)
    required_columns = {
        "policy_id",
        "decision_owner",
        "decision_cadence",
        "execution_mode",
        "objective",
        "capacity_constraint",
        "exposure_safeguard",
        "exception_rule",
        "review_trigger",
        "outcome_metric",
    }

    assert required_columns.issubset(contract.columns), (
        "El contrato debe documentar acción, responsable, cadencia, modo de "
        "ejecución, objetivo, límites, salvaguardas, excepción, revisión y resultado."
    )
