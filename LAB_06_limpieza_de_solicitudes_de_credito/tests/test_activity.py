"""Pruebas de calificación automática para LAB_06_limpieza_de_solicitudes_de_credito."""

from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
OUTPUT_FILE = ROOT / "submission" / "solicitudes_de_credito.csv"
EXPECTED_COLUMNS = ["sexo", "tipo_de_emprendimiento", "idea_negocio", "barrio", "estrato", "comuna_ciudadano", "fecha_de_beneficio", "monto_del_credito", "línea_credito"]


def load_submission():
    """Carga el único entregable que debe producir el estudiante."""
    assert OUTPUT_FILE.exists(), "Falta submission/solicitudes_de_credito.csv"
    return pd.read_csv(OUTPUT_FILE, sep=";")


def test_01_submission_has_the_clean_analytical_structure():
    """El archivo debe tener únicamente las columnas analíticas y filas completas."""
    dataframe = load_submission()
    assert dataframe.columns.tolist() == EXPECTED_COLUMNS
    assert dataframe.shape == (10417, 9)
    assert dataframe.drop(columns=["comuna_ciudadano"]).notna().all().all()


def test_02_sexo_is_normalized():
    """`sexo` debe conservar las dos categorías limpias y sus frecuencias."""
    assert load_submission()["sexo"].value_counts().to_dict() == {"femenino": 6767, "masculino": 3650}


def test_03_tipo_de_emprendimiento_is_normalized():
    """`tipo_de_emprendimiento` debe recuperar sus cuatro categorías válidas."""
    assert load_submission()["tipo_de_emprendimiento"].value_counts().to_dict() == {"comercio": 5754, "servicio": 2252, "industria": 2247, "agropecuaria": 164}


def test_04_idea_negocio_preserves_the_clean_category_distribution():
    """`idea_negocio` debe eliminar las alteraciones de mayúsculas y separadores."""
    counts = load_submission()["idea_negocio"].value_counts()
    assert counts.size == 75
    assert counts.head(5).to_dict() == {"fabrica de ": 1904, "variedades": 1717, "tienda": 1005, "comidas rapidas": 965, "almacen de ropa en ": 592}


def test_05_barrio_preserves_the_clean_category_distribution():
    """`barrio` debe recuperar sus categorías originales, incluidas sus frecuencias."""
    counts = load_submission()["barrio"].value_counts()
    assert counts.size == 234
    assert counts.head(5).to_dict() == {"robledo": 1020, "manrique central no. 1": 485, "san javier no.1": 424, "aranjuez": 397, "buenos aires": 389}


def test_06_estrato_is_a_valid_integer_category():
    """`estrato` debe convertir representaciones como `01` a su categoría numérica."""
    assert load_submission()["estrato"].value_counts().to_dict() == {2: 5132, 3: 3219, 1: 2062, 0: 4}


def test_07_comuna_ciudadano_keeps_its_legitimate_missing_values():
    """`comuna_ciudadano` no debe eliminar faltantes que pertenecen al dato original."""
    series = load_submission()["comuna_ciudadano"]
    assert series.isna().sum() == 196
    assert sorted(series.dropna().unique().tolist()) == [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0, 11.0, 12.0, 13.0, 14.0, 15.0, 16.0, 50.0, 60.0, 70.0, 80.0, 90.0]


def test_08_fecha_de_beneficio_has_valid_dates():
    """`fecha_de_beneficio` debe recuperar un formato interpretable día/mes/año."""
    dates = pd.to_datetime(load_submission()["fecha_de_beneficio"], dayfirst=True)
    assert dates.nunique() == 796
    assert dates.min() == pd.Timestamp("2016-01-05")
    assert dates.max() == pd.Timestamp("2019-06-28")


def test_09_monto_del_credito_is_numeric_and_positive():
    """`monto_del_credito` debe retirar formatos monetarios y conservar sus valores."""
    amounts = load_submission()["monto_del_credito"]
    assert pd.api.types.is_integer_dtype(amounts)
    assert amounts.min() == 2
    assert amounts.max() == 82000000
    assert amounts.nunique() == 280


def test_10_linea_credito_is_normalized():
    """`línea_credito` debe recuperar las categorías y frecuencias del dato limpio."""
    assert load_submission()["línea_credito"].value_counts().to_dict() == {"microempresarial": 10231, "empresarial ed. ": 70, "agropecuaria": 55, "juridica y cap.semilla": 33, "credioportuno": 21, "fomento agropecuario": 4, "soli-diaria": 1, "solidaria": 1, "ayacucho formal": 1}
