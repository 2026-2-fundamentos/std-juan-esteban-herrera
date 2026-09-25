import os

def test_01():

    assert os.path.exists("submission/summary.csv")
    assert os.path.exists("submission/top10_drivers.png")
