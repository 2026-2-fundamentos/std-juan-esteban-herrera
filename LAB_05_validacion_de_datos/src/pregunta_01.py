import json
import re
from pathlib import Path

import pandas as pd


def main():
    """
    Valide `data/ventas.csv` y escriba `submission/data_quality_report.json`.

    El archivo de origen posee encabezados inconsistentes, valores faltantes,
    filas repetidas y valores categóricos con representaciones distintas. El
    reporte debe preservar estos hallazgos: no limpie ni modifique los datos.

    El JSON debe incluir el tamaño de la tabla, validación de las columnas
    requeridas, filas duplicadas, duplicados de `supplier_id`, faltantes por
    columna, correos inválidos, unidades inválidas y los valores observados de
    `country`.
    """

    raise NotImplementedError
