"""Pruebas de las consultas SQL con SQLite."""

import sqlite3
from pathlib import Path

import pandas as pd
import pytest


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
SOURCE_DIR = ACTIVITY_DIR / "src"

SCHEMAS = {
    "tbl0": ["K0", "c01", "c02", "c03", "c04"],
    "tbl1": ["K0", "K1", "c12", "c13", "c14", "c15", "c16"],
    "tbl2": ["K1", "c21", "c22", "c23", "c24", "c25"],
}


def load_data() -> sqlite3.Connection:
    """Carga los CSV entregados en una base SQLite en memoria."""
    connection = sqlite3.connect(":memory:")
    for table, columns in SCHEMAS.items():
        table_data = pd.read_csv(DATA_DIR / f"{table}.csv", names=columns)
        table_data.to_sql(table, connection, index=False)
    return connection


def run_query(question: int) -> pd.DataFrame:
    """Ejecuta una consulta de la entrega sobre los datos de la actividad."""
    query = (SOURCE_DIR / f"pregunta_{question:02}.sql").read_text(encoding="utf-8")
    with load_data() as connection:
        return pd.read_sql_query(query, connection)


def test_01_sum_of_c12():
    """Calcula el total de c12."""
    assert run_query(1).iloc[0, 0] == 15137.63


def test_02_count_of_tbl1():
    """Cuenta los registros de tbl1."""
    assert run_query(2).iloc[0, 0] == 30


def test_03_first_five_records_by_date():
    """Ordena tbl1 por fecha y limita el resultado."""
    result = run_query(3)
    assert result["K1"].tolist() == [20, 15, 22, 12, 14]


def test_04_prefix_matches_key():
    """Filtra códigos cuyo prefijo coincide con K0."""
    result = run_query(4)
    assert result.to_dict("records") == [
        {"K0": "E", "c16": "EGFD"},
        {"K0": "B", "c16": "BDEE"},
        {"K0": "C", "c16": "CCCE"},
    ]


def test_05_filter_values_in_tbl0():
    """Filtra los valores 100 y 600 de c02."""
    assert run_query(5)["K0"].tolist() == ["B", "C", "D", "G"]


def test_06_filter_a_and_order_by_date():
    """Filtra la categoría A y la ordena cronológicamente."""
    assert run_query(6)["K1"].tolist() == [20, 30, 18, 26, 6, 10]


def test_07_combined_filters():
    """Aplica exclusiones simultáneas y conserva el orden solicitado."""
    result = run_query(7)
    assert result.shape == (13, 7)
    assert result["K1"].tolist() == [14, 8, 1, 27, 4, 3, 13, 5, 7, 25, 2, 19, 24]


def test_08_average_by_year():
    """Agrupa tbl2 por año y calcula el promedio."""
    result = run_query(8)
    assert result.iloc[:, 0].tolist() == ["2016", "2017", "2018", "2019"]
    assert result.iloc[:, 1].round(2).tolist() == [564.48, 515.16, 557.56, 551.0]


def test_09_row_with_minimum_c21():
    """Encuentra el registro con el mínimo de c21."""
    result = run_query(9)
    assert result.to_dict("records") == [
        {"K1": 29, "c21": 101.11, "c22": 100, "c23": "2017-11-17", "c24": 0.42, "c25": "MV-CB"}
    ]


def test_10_filter_c02_at_least_300():
    """Filtra tbl0 por el umbral de c02."""
    assert run_query(10)["K0"].tolist() == ["A", "C", "D", "F", "I"]


def test_11_count_records_in_2018():
    """Cuenta los registros de tbl1 correspondientes a 2018."""
    assert run_query(11).iloc[0, 0] == 6


def test_12_minimum_and_maximum_per_group():
    """Resume los extremos de c12 por K0."""
    result = run_query(12)
    assert result["K0"].tolist() == ["A", "B", "C", "D", "E"]
    assert result.iloc[:, 1].round(2).tolist() == [938.16, 999.72, 822.81, 756.37, 832.44]
    assert result.iloc[:, 2].round(2).tolist() == [135.8, 283.4, 267.42, 317.77, 118.77]


def test_13_average_c12_with_filter():
    """Promedia c12 por K0 después de filtrar c13."""
    result = run_query(13)
    assert result["K0"].tolist() == ["A", "B", "C", "D", "E"]
    assert result.iloc[:, 1].tolist() == pytest.approx(
        [476.155, 536.5233333333, 490.83, 709.53, 474.825]
    )


def test_14_average_c21_after_join():
    """Une las tablas por K1 y calcula el promedio solicitado."""
    result = run_query(14)
    assert result["K0"].tolist() == ["A", "B", "C", "D", "E"]
    assert result.iloc[:, 1].round(2).tolist() == [593.5, 575.47, 530.75, 655.61, 555.32]
