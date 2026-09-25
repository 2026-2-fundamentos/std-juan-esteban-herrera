# LAB_04_ingestion_de_texto_en_directorios

## Propósito

Construir una tabla analítica a partir de una colección de archivos de texto organizada por directorios. El laboratorio desarrolla la capacidad de recorrer una estructura de archivos, extraer texto, conservar su etiqueta y producir un dataset reproducible.

## Competencia evaluada

Convierte una colección de archivos semiestructurados en un dataset tabular, preservando la relación entre cada observación y su categoría de origen.

## Datos

La carpeta `data/` contiene dos divisiones: `train/` y `test/`. Cada una incluye las categorías `negative/`, `neutral/` y `positive/`; dentro de ellas hay un archivo de texto por frase.

La función y el enunciado de la actividad están en `src/pregunta_01.py`.

## Restricciones

- Use Pandas para construir y escribir los datasets.
- No modifique archivos de `data/` ni de `tests/`.
- Los entregables permanentes deben escribirse únicamente en `submission/`.
- No escriba resultados en la raíz del laboratorio ni en `data/`.
