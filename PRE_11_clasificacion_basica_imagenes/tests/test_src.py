import os
import pickle

from sklearn import datasets  # type: ignore
from sklearn.metrics import accuracy_score  # type: ignore

FOLDER = "PRE_11_clasificacion_basica_imagenes"


def test_01():

    digits = datasets.load_digits(return_X_y=True)
    data, target = digits

    assert os.path.exists(f"{FOLDER}/submission/estimator.pkl")

    with open(f"{FOLDER}/submission/estimator.pkl", "rb") as file:
        new_clf = pickle.load(file)

    accuracy = accuracy_score(
        y_true=target,
        y_pred=new_clf.predict(data),
    )

    assert accuracy > 0.96
