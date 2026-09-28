"""Estima el valor de reventa de vehículos usados."""

from pathlib import Path
import json
import pickle

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"
FEATURES = ["Age", "Present_Price", "Driven_kms", "Fuel_Type", "Selling_type", "Transmission", "Owner"]


def prepare_data(frame):
    """Construye variables disponibles para estimar el valor de reventa."""
    data = frame.copy()
    data["Age"] = 2021 - data["Year"]
    return data


def main():
    train = prepare_data(pd.read_csv(DATA_DIR / "train_data.csv.gz"))
    test = prepare_data(pd.read_csv(DATA_DIR / "test_data.csv.gz"))
    categorical = ["Fuel_Type", "Selling_type", "Transmission"]
    model = Pipeline([
        ("features", ColumnTransformer([("categorical", OneHotEncoder(handle_unknown="ignore"), categorical)], remainder="passthrough")),
        ("regression", LinearRegression()),
    ])
    model.fit(train[FEATURES], train["Selling_Price"])
    predictions = model.predict(test[FEATURES])
    SUBMISSION_DIR.mkdir(exist_ok=True)
    pd.DataFrame({"actual_price": test["Selling_Price"], "predicted_price": predictions}).to_csv(SUBMISSION_DIR / "test_predictions.csv", index=False)
    metrics = {"test_mae": mean_absolute_error(test["Selling_Price"], predictions), "test_r2": r2_score(test["Selling_Price"], predictions)}
    (SUBMISSION_DIR / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    with (SUBMISSION_DIR / "model.pkl").open("wb") as file:
        pickle.dump(model, file)


if __name__ == "__main__":
    main()
