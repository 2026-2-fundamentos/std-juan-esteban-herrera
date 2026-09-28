"""Construye los artefactos verificables del taller de clasificación numérica."""

import json
import pickle
from pathlib import Path

import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = ACTIVITY_DIR / "data" / "wisc_bc_data.csv"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"

BASE_FEATURES = ["texture_mean", "compactness_mean"]
FLEXIBLE_FEATURES = [
    "texture_mean",
    "compactness_mean",
    "texture_mean_squared",
    "texture_mean_x_compactness_mean",
]


def build_flexible_features(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Conserva visibles la transformación y el término de interacción."""
    features = dataframe[BASE_FEATURES].copy()
    features["texture_mean_squared"] = features["texture_mean"] ** 2
    features["texture_mean_x_compactness_mean"] = (
        features["texture_mean"] * features["compactness_mean"]
    )
    return features


def build_estimator() -> Pipeline:
    """Estandariza las mediciones antes de ajustar una regresión logística."""
    return Pipeline(
        steps=[
            ("scaler", StandardScaler()),
            ("classifier", LogisticRegression(max_iter=1000, random_state=0)),
        ]
    )


def main() -> None:
    dataframe = pd.read_csv(DATA_PATH)
    target = (dataframe["diagnosis"] == "M").astype(int)
    base_features = dataframe[BASE_FEATURES].copy()
    flexible_features = build_flexible_features(dataframe)

    train_index, test_index = train_test_split(
        dataframe.index,
        train_size=0.8,
        random_state=0,
        stratify=target,
    )

    base_estimator = build_estimator()
    flexible_estimator = build_estimator()
    base_estimator.fit(base_features.loc[train_index], target.loc[train_index])
    flexible_estimator.fit(
        flexible_features.loc[train_index],
        target.loc[train_index],
    )

    comparison = []
    for name, estimator, features in [
        ("logistica_base", base_estimator, base_features),
        ("logistica_flexible", flexible_estimator, flexible_features),
    ]:
        probability = estimator.predict_proba(features.loc[test_index])[:, 1]
        prediction = estimator.predict(features.loc[test_index])
        comparison.append(
            {
                "model": name,
                "test_auc": roc_auc_score(target.loc[test_index], probability),
                "test_accuracy": accuracy_score(target.loc[test_index], prediction),
            }
        )

    SUBMISSION_DIR.mkdir(exist_ok=True)
    pd.DataFrame(comparison).to_csv(
        SUBMISSION_DIR / "model_comparison.csv",
        index=False,
    )
    with (SUBMISSION_DIR / "base_estimator.pkl").open("wb") as file:
        pickle.dump(base_estimator, file)
    with (SUBMISSION_DIR / "flexible_estimator.pkl").open("wb") as file:
        pickle.dump(flexible_estimator, file)
    with (SUBMISSION_DIR / "metrics.json").open("w", encoding="utf-8") as file:
        json.dump(
            {
                "test_size": len(test_index),
                "positive_class": "M",
                "base_features": BASE_FEATURES,
                "flexible_features": FLEXIBLE_FEATURES,
                "test_auc": comparison[1]["test_auc"],
            },
            file,
            indent=2,
        )


if __name__ == "__main__":
    main()
