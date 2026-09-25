# LAB_03_ingestion_de_texto_plano

## Propósito

Transformar un reporte de texto con formato visual en una tabla utilizable para análisis. El laboratorio desarrolla la capacidad de identificar registros, reconocer continuaciones de línea, limpiar texto y construir una estructura tabular reproducible.

## Competencia evaluada

Convierte datos semiestructurados en una tabla analítica, conservando su significado y normalizando la estructura necesaria para su posterior análisis.

## Datos

`data/clusters_report.txt` contiene un reporte de clústeres de palabras clave. La tabla no es un CSV: sus encabezados ocupan varias líneas y las palabras clave de un mismo clúster pueden continuar en líneas posteriores.

La función y el enunciado de la actividad están en `src/pregunta_01.py`.

## Restricciones

- Use Pandas para construir el resultado tabular.
- No modifique el archivo de `data/` ni los archivos de `tests/`.
- La función debe retornar el DataFrame solicitado; no debe imprimirlo ni escribir archivos de salida.
