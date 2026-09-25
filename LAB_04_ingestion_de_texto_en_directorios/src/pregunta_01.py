from pathlib import Path

import pandas as pd


def pregunta_01():
    """
    Construya dos tablas de texto a partir de los directorios `data/train/`
    y `data/test/`. Cada división contiene las carpetas `negative`,
    `neutral` y `positive`; cada archivo `.txt` representa una frase.

    Genere los archivos permanentes:

    - `submission/train_dataset.csv`
    - `submission/test_dataset.csv`

    Ambos archivos deben tener las columnas `phrase` y `target`. `phrase`
    contiene el texto de cada archivo y `target` corresponde al nombre de su
    carpeta de sentimiento. Procese las carpetas y archivos en orden
    alfabético para producir resultados reproducibles.

    El archivo CSV resultante debe tener una estructura como esta:

    ```csv
    phrase,target
    "Operating profit increased during the period",positive
    "The company operates in Finland",neutral
    "Sales decreased compared with last year",negative
    ```
    """

    raise NotImplementedError
