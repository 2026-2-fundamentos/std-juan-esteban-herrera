import os

import pandas as pd

FOLDER = "PRE_14_clustering_mercadeo"


def test_homework():
    """Test the homework."""

    assert os.path.exists(f"{FOLDER}/submission/segmented.csv")

    df = pd.read_csv(f"{FOLDER}/submission/segmented.csv", index_col=0)

    assert df.shape[0] > 0
    assert df.shape[1] > 0
