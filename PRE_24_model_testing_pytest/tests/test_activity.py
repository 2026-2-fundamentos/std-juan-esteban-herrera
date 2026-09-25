# Uso: python3 -m pytest -q tests/test_activity.py

import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest


ACTIVITY_DIR = Path(__file__).resolve().parents[1]


def load_main():
    SPECIFICATION = importlib.util.spec_from_file_location("model_testing_main", ACTIVITY_DIR / "src" / "main.py")
    main = importlib.util.module_from_spec(SPECIFICATION)
    SPECIFICATION.loader.exec_module(main)
    return main


@pytest.fixture(scope="module")
def model_context():
    # El fixture comparte el mismo artefacto inmutable para concentrar cada prueba en una sola expectativa.

    main = load_main()
    return main.load_model_and_test_set()


def test_prediction_interface(model_context):
    # Quien consume el modelo necesita una predicción por fila y probabilidades válidas.

    model, inputs, _, _ = model_context
    probabilities = model.predict_proba(inputs)
    assert len(model.predict(inputs)) == len(inputs)
    assert probabilities.shape == (len(inputs), len(model.classes_))
    assert np.allclose(probabilities.sum(axis=1), 1.0)


def test_known_cases_keep_their_order(model_context):
    # Dos casos de referencia protegen una expectativa que no debe cambiar silenciosamente.

    model, _, _, features = model_context
    references = pd.DataFrame([
        {"texture_mean": 13.06, "compactness_mean": 0.03774},
        {"texture_mean": 24.91, "compactness_mean": 0.26650},
    ]).loc[:, features]
    probabilities = model.predict_proba(references)[:, 1]
    assert probabilities[1] > probabilities[0]


def test_holdout_metrics_meet_the_operating_floor(model_context):
    # Un modelo que no alcanza el umbral acordado no debe seguir habilitado sin revisión.

    main = load_main()
    model, inputs, target, _ = model_context
    metrics = main.model_metrics(model, inputs, target)
    assert metrics["accuracy"] >= main.MIN_ACCURACY
    assert metrics["balanced_accuracy"] >= main.MIN_BALANCED_ACCURACY
    assert metrics["auc"] >= main.MIN_AUC


def test_scoring_is_reproducible(model_context):
    # Una misma entrada debe conservar su resultado para que la decisión sea auditable.

    model, inputs, _, _ = model_context
    assert np.allclose(model.predict_proba(inputs), model.predict_proba(inputs))
