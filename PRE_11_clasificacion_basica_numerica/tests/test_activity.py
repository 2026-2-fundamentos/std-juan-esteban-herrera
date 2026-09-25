import json
import pickle
from pathlib import Path

import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split


BASE_FEATURES = ["texture_mean", "compactness_mean"]
FLEXIBLE_FEATURES = [
    "texture_mean",
    "compactness_mean",
    "texture_mean_squared",
    "texture_mean_x_compactness_mean",
]


def build_flexible_features(dataframe):
    features = dataframe[BASE_FEATURES].copy()
    features["texture_mean_squared"] = features["texture_mean"] ** 2
    features["texture_mean_x_compactness_mean"] = (
        features["texture_mean"] * features["compactness_mean"]
    )
    return features


def test_logistic_models_generalize_and_return_probabilities():
    dataframe = pd.read_csv("data/wisc_bc_data.csv")
    target = (dataframe["diagnosis"] == "M").astype(int)
    _, test_index = train_test_split(
        dataframe.index,
        train_size=0.8,
        random_state=0,
        stratify=target,
    )

    with Path("submission/base_estimator.pkl").open("rb") as file:
        base_estimator = pickle.load(file)
    with Path("submission/flexible_estimator.pkl").open("rb") as file:
        flexible_estimator = pickle.load(file)

    base_probability = base_estimator.predict_proba(
        dataframe.loc[test_index, BASE_FEATURES]
    )[:, 1]
    flexible_probability = flexible_estimator.predict_proba(
        build_flexible_features(dataframe.loc[test_index])
    )[:, 1]

    assert len(base_probability) == len(test_index)
    assert ((base_probability >= 0) & (base_probability <= 1)).all()
    assert ((flexible_probability >= 0) & (flexible_probability <= 1)).all()
    assert roc_auc_score(target.loc[test_index], base_probability) >= 0.80
    assert roc_auc_score(target.loc[test_index], flexible_probability) >= 0.80


def test_comparison_and_explicit_flexible_terms_are_persisted():
    comparison = pd.read_csv("submission/model_comparison.csv")

    assert set(comparison["model"]) == {"logistica_base", "logistica_flexible"}
    assert comparison["test_auc"].between(0, 1).all()
    assert comparison["test_accuracy"].between(0, 1).all()

    with Path("submission/metrics.json").open(encoding="utf-8") as file:
        metrics = json.load(file)

    assert metrics["test_size"] == 114
    assert metrics["positive_class"] == "M"
    assert metrics["flexible_features"] == FLEXIBLE_FEATURES
