import os

FOLDER = "PRE_13_clustering_demanda"


def test_homework():

    assert os.path.exists(f"{FOLDER}/submission/demanda-comercial-patrones-ejemplo.png")
    assert os.path.exists(f"{FOLDER}/submission/demanda-comercial-perfiles.png")
    assert os.path.exists(f"{FOLDER}/submission/demanda-comercial.png")
