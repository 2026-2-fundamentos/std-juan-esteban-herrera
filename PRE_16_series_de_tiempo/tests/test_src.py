import os

FOLDER = "PRE_16_series_de_tiempo"


def test_01():

    assert os.path.exists(f"{FOLDER}/submission/metrics.csv")
    assert os.path.exists(f"{FOLDER}/submission/forecasts.csv")
