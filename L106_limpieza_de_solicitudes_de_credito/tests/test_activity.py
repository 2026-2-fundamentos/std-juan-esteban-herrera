import importlib
from pathlib import Path

import pandas as pd

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
PROFESSOR_DIR = ACTIVITY_DIR / "professor"
IS_PROFESSOR = any(
    (path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents
) and any(path.name != ".gitkeep" for path in PROFESSOR_DIR.iterdir())
CODE_DIR = ACTIVITY_DIR / ("professor" if IS_PROFESSOR else "src")
SUBMISSION_FILE = ACTIVITY_DIR / "submission" / "solicitudes_de_credito.csv"
TEXT_COLUMNS = [
    "sexo",
    "tipo_de_emprendimiento",
    "idea_negocio",
    "barrio",
    "línea_credito",
]


def parse_dates(values):
    dates = pd.to_datetime(values, format="%d/%m/%Y", errors="coerce")
    for date_format in ["%Y-%m-%d", "%Y/%m/%d"]:
        dates = dates.fillna(
            pd.to_datetime(values, format=date_format, errors="coerce")
        )
    return dates


def test_01(monkeypatch):
    SUBMISSION_FILE.unlink(missing_ok=True)

    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    importlib.import_module(f"{CODE_DIR.name}.pregunta_01").pregunta_01()

    assert SUBMISSION_FILE.exists()

    df = pd.read_csv(SUBMISSION_FILE, sep=";")
    for column in TEXT_COLUMNS:
        df[column] = df[column].str.strip()
    dates = parse_dates(df["fecha_de_beneficio"].astype(str))

    assert df.columns.tolist() == [
        "sexo",
        "tipo_de_emprendimiento",
        "idea_negocio",
        "barrio",
        "estrato",
        "comuna_ciudadano",
        "fecha_de_beneficio",
        "monto_del_credito",
        "línea_credito",
    ]
    assert len(df) == 10402
    assert df.drop(columns="comuna_ciudadano").notna().all().all()
    assert df["comuna_ciudadano"].isna().sum() == 196

    assert df["sexo"].value_counts().to_dict() == {
        "femenino": 6755,
        "masculino": 3647,
    }
    assert df["tipo_de_emprendimiento"].value_counts().to_dict() == {
        "comercio": 5744,
        "servicio": 2251,
        "industria": 2243,
        "agropecuaria": 164,
    }
    assert df["idea_negocio"].nunique() == 75
    assert df["idea_negocio"].value_counts().head(10).to_dict() == {
        "fabrica de": 1900,
        "variedades": 1714,
        "tienda": 1002,
        "comidas rapidas": 964,
        "peluqueria": 592,
        "almacen de ropa en": 590,
        "restaurante": 275,
        "mantenimiento en": 223,
        "distribuidora de": 168,
        "papeleria": 164,
    }
    assert df["barrio"].nunique() == 232
    assert df["barrio"].value_counts().head(10).to_dict() == {
        "robledo": 1017,
        "manrique central no. 1": 484,
        "san javier no.1": 424,
        "aranjuez": 396,
        "buenos aires": 389,
        "belen": 376,
        "popular": 369,
        "cabecera san cristobal": 348,
        "castilla": 335,
        "enciso": 315,
    }
    assert df["estrato"].value_counts().to_dict() == {2: 5124, 3: 3217, 1: 2057, 0: 4}
    assert df["comuna_ciudadano"].value_counts().sort_index().to_dict() == {
        1: 830,
        2: 636,
        3: 588,
        4: 1326,
        5: 667,
        6: 559,
        7: 1133,
        8: 729,
        9: 968,
        10: 296,
        11: 10,
        12: 227,
        13: 830,
        14: 12,
        15: 191,
        16: 426,
        50: 27,
        60: 391,
        70: 29,
        80: 267,
        90: 64,
    }
    assert dates.notna().all()
    assert dates.nunique() == 796
    assert dates.min() == pd.Timestamp("2016-01-05")
    assert dates.max() == pd.Timestamp("2019-06-28")
    assert dates.dt.year.value_counts().sort_index().to_dict() == {
        2016: 2106,
        2017: 3379,
        2018: 4086,
        2019: 831,
    }
    assert df["monto_del_credito"].sum() == 64154719415
    assert df["monto_del_credito"].nunique() == 280
    assert df["línea_credito"].value_counts().to_dict() == {
        "microempresarial": 10216,
        "empresarial ed.": 70,
        "agropecuaria": 55,
        "juridica y cap.semilla": 33,
        "credioportuno": 21,
        "fomento agropecuario": 4,
        "soli diaria": 1,
        "solidaria": 1,
        "ayacucho formal": 1,
    }
