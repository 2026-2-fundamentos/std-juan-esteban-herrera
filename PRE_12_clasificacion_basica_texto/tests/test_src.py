import pickle

import pandas as pd
from sklearn.metrics import accuracy_score

FOLDER = "PRE_12_clasificacion_basica_texto"


def test_01():

    dataframe = pd.read_csv(
        f"{FOLDER}/data/sentences.csv.zip",
        index_col=False,
        compression="zip",
    )

    with open(f"{FOLDER}/submission/clf.pkl", "rb") as file:
        clf = pickle.load(file)

    with open(f"{FOLDER}/submission/vectorizer.pkl", "rb") as file:
        vectorizer = pickle.load(file)

    accuracy = accuracy_score(
        y_true=dataframe.target,
        y_pred=clf.predict(vectorizer.transform(dataframe.phrase)),
    )

    assert accuracy > 0.854
