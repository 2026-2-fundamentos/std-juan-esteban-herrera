import shutil
from pathlib import Path

import pandas as pd


def generate_dirty_data():
    """
    Limpie `data/solicitudes_de_credito.csv` y escriba el resultado en
    `submission/solicitudes_de_credito.csv` usando punto y coma como separador.

    El archivo de entrada tiene una columna de índice accidental, registros
    duplicados, faltantes y transformaciones de representación introducidas en
    campos categóricos, fechas, estrato y monto. El archivo entregado debe
    contener únicamente las nueve columnas analíticas limpias y conservar los
    valores faltantes que pertenecen a `comuna_ciudadano`.

    Puede usar un archivo `.py` o un notebook para resolver la actividad. Esta
    función existe exclusivamente en la versión docente: genera la copia sucia
    de los datos a partir del archivo limpio canónico de la raíz de la actividad.
    """

    raise NotImplementedError
