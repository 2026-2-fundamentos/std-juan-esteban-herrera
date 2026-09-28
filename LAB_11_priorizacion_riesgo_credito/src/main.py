"""Prioriza solicitudes de crédito según la probabilidad de incumplimiento."""

from pathlib import Path
import json
import pickle

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, balanced_accuracy_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"
TARGET = "default payment next month"


def prepare_data(frame):
    """Retira el identificador y conserva información disponible antes del pago."""
    data = frame.rename(columns={TARGET: "default"}).drop(columns="ID")
    data["EDUCATION"] = data["EDUCATION"].where(data["EDUCATION"].le(4), 4)
    return data


def main():
    train = prepare_data(pd.read_csv(DATA_DIR / "train_data.csv.gz"))
    test = prepare_data(pd.read_csv(DATA_DIR / "test_data.csv.gz"))
    features = train.columns.drop("default")
    model = Pipeline([("scale", StandardScaler()), ("classifier", LogisticRegression(max_iter=2000, class_weight="balanced"))])
    model.fit(train[features], train["default"])
    probability = model.predict_proba(test[features])[:, 1]
    threshold = float(pd.Series(probability).quantile(0.80))
    priority = pd.DataFrame({"application_id": test.index, "default_probability": probability})
    priority["priority"] = priority["default_probability"].ge(threshold)
    priority = priority.sort_values("default_probability", ascending=False)
    predictions = (probability >= 0.5).astype(int)
    metrics = {"test_balanced_accuracy": balanced_accuracy_score(test["default"], predictions), "test_average_precision": average_precision_score(test["default"], probability), "priority_threshold": threshold}
    SUBMISSION_DIR.mkdir(exist_ok=True)
    priority.to_csv(SUBMISSION_DIR / "priority_applications.csv", index=False)
    (SUBMISSION_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    with (SUBMISSION_DIR / "model.pkl").open("wb") as file:
        pickle.dump(model, file)


if __name__ == "__main__":
    main()
