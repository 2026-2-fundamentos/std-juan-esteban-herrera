"""Autograding script"""

import os

FOLDER = "PRE_15_deployment"


def test_01():

    assert os.path.exists(f"{FOLDER}/src/train_model.py")
    assert os.path.exists(f"{FOLDER}/src/web_app.py")
    assert os.path.exists(f"{FOLDER}/src/api_client.py")
    assert os.path.exists(f"{FOLDER}/src/api_server.py")
    assert os.path.exists(f"{FOLDER}/src/descriptivo.ipynb")
    assert os.path.exists(f"{FOLDER}/submission/house_predictor.pkl")
