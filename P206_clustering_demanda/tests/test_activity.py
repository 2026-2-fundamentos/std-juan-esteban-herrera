from pathlib import Path

def test_01():
    submission=Path(__file__).resolve().parents[1] / "submission"
    for filename in ["cluster-selection.csv", "demanda-comercial-clusters.csv", "demanda-comercial-dias.csv", "demanda-comercial-patrones-ejemplo.png", "demanda-comercial-perfiles.png", "demanda-comercial.png", "perfil-recibido.csv"]:
        assert (submission / filename).is_file()
