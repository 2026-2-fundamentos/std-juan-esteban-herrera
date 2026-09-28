# SQL con SQLite3

## Propósito

Resolver consultas SQL de filtrado, ordenamiento, agregación y unión de tablas sobre una base SQLite temporal.

## Competencia

Formula consultas SQL reproducibles sobre tablas relacionales y contrasta los resultados con propiedades analíticas esperadas.

## Datos

Los archivos `data/tbl0.csv.gz`, `data/tbl1.csv.gz` y `data/tbl2.csv.gz` contienen las tres tablas de entrada, sin encabezados. Las pruebas cargan cada archivo en una base SQLite en memoria, en una tabla con el mismo nombre (`tbl0`, `tbl1` y `tbl2`), y luego ejecutan su consulta. La estructura de las tablas aparece al inicio de cada pregunta.

## Restricciones

Escriba una consulta por archivo en `src/pregunta_01.sql` a `src/pregunta_14.sql`. Las consultas se ejecutan sobre SQLite y no deben modificar los datos de entrada.
