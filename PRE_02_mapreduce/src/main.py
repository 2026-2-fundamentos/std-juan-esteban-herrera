import shutil
import string
from pathlib import Path


def run_word_count() -> Path:
    """
    Construya un conteo de palabras con las etapas de MapReduce.

    Copie los textos de ``data/`` a ``temp/input/``. Después, lea cada línea,
    convierta el texto a minúsculas, elimine puntuación y genere pares
    ``(palabra, 1)``. Ordene los pares por palabra, reduzca sumando los valores
    de cada clave y escriba el resultado tabulado en
    ``temp/output/part-00000``. Cree también el marcador
    ``temp/output/_SUCCESS``.

    ``temp/`` contiene resultados temporales de ejecución y no constituye una
    entrega persistente del taller.
    """

    raise NotImplementedError


if __name__ == "__main__":
    run_word_count()
