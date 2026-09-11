import os

import pandas as pd

FOLDER = "PRE_05_anonimizacion"

OUTPUT_FILE = f"{FOLDER}/submission/anonymized.csv"


def test_01():

    if not os.path.exists(OUTPUT_FILE):
        raise Exception("Output file does not exist")

    df = pd.read_csv(OUTPUT_FILE)

    assert df.shape[0] > 0
    assert df.shape[1] > 0
