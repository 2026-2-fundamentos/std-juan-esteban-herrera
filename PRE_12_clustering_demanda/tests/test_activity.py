from pathlib import Path

import pandas as pd


def test_saved_daily_patterns_are_complete_and_interpretable():
    figures = [
        Path("submission/demanda-comercial-patrones-ejemplo.png"),
        Path("submission/demanda-comercial-perfiles.png"),
        Path("submission/demanda-comercial.png"),
    ]

    for figure in figures:
        assert figure.exists()
        assert figure.stat().st_size > 0

    daily_patterns = pd.read_csv("submission/demanda-comercial-clusters.csv")
    weekday_summary = pd.read_csv("submission/demanda-comercial-dias.csv")
    cluster_selection = pd.read_csv("submission/cluster-selection.csv")
    received_profile = pd.read_csv("submission/perfil-recibido.csv")

    assert list(daily_patterns.columns) == ["Fecha", "cluster", "day_of_week"]
    assert len(daily_patterns) == 2069
    assert daily_patterns["Fecha"].is_unique
    assert set(daily_patterns["cluster"]) == {0, 1}
    day_names = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
    assert set(daily_patterns["day_of_week"]) == set(day_names)

    assert list(weekday_summary.columns) == [
        "day_of_week",
        "cluster_0_days",
        "cluster_1_days",
    ]
    assert weekday_summary["day_of_week"].tolist() == day_names
    assert weekday_summary[["cluster_0_days", "cluster_1_days"]].to_numpy().sum() == len(
        daily_patterns
    )

    assert cluster_selection["n_clusters"].tolist() == [2, 3, 4, 5]
    assert cluster_selection["silhouette_score"].between(-1, 1).all()
    assert cluster_selection.loc[
        cluster_selection["silhouette_score"].idxmax(), "n_clusters"
    ] == 2

    assert list(received_profile.columns) == ["Fecha", "cluster_asignado"]
    assert len(received_profile) == 1
    assert received_profile["cluster_asignado"].iloc[0] in {0, 1}
