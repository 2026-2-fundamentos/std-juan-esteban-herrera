from pathlib import Path
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
SLOT_COLUMNS = ["grade_1_slots", "grade_2_slots", "grade_3_slots"]
VALUE_COLUMNS = ["value_grade_1", "value_grade_2", "value_grade_3"]


def evaluate_policies(policies: pd.DataFrame) -> pd.DataFrame:
    result = policies.copy()
    result["allocated_slots"] = result[SLOT_COLUMNS].sum(axis=1)
    result["expected_learning_gain"] = sum(
        result[slot] * result[value]
        for slot, value in zip(SLOT_COLUMNS, VALUE_COLUMNS)
    )
    result["capacity_ok"] = result.allocated_slots == result.total_slots
    result["minimum_ok"] = result[SLOT_COLUMNS].ge(
        result.min_slots_per_grade, axis=0
    ).all(axis=1)
    result["feasible"] = result.capacity_ok & result.minimum_ok
    return result


def recommend(policies: pd.DataFrame) -> pd.DataFrame:
    result = evaluate_policies(policies)
    chosen = result.loc[result.feasible].nlargest(1, "expected_learning_gain").copy()
    chosen["decision_owner"] = "Dirección académica"
    chosen["review_trigger"] = "Revisar si la asistencia por grado es menor a 70%."
    return chosen.reset_index(drop=True)


def main() -> None:
    policies = pd.read_csv(ROOT / "data" / "policy_options.csv")
    recommend(policies).to_csv(ROOT / "submission" / "policy_recommendation.csv", index=False)


if __name__ == "__main__":
    main()
