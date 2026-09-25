# LAB_05_validacion_de_datos

## Propósito

Construir evidencia reproducible sobre la calidad de una tabla antes de limpiarla o analizarla. El laboratorio desarrolla la capacidad de revisar estructura, completitud, duplicados, reglas de negocio y representaciones inconsistentes.

## Competencia evaluada

Diagnostica la calidad de un dataset y comunica hallazgos verificables que determinan si está listo para un análisis posterior.

## Datos

`data/ventas.csv` contiene registros de compras con problemas de encabezados, faltantes, duplicados y representaciones heterogéneas de algunas categorías.

La función y el enunciado de la actividad están en `src/pregunta_01.py`.

## Restricciones

- Use Pandas para cargar y validar los datos.
- No modifique `data/ventas.csv` ni los archivos de `tests/`.
- El reporte permanente debe escribirse únicamente en `submission/data_quality_report.json`.
- El propósito es diagnosticar los problemas; no debe limpiar ni reemplazar valores del archivo de origen.
