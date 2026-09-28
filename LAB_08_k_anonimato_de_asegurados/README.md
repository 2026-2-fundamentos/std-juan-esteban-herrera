# k-anonimato de asegurados

## Propósito

Medir el riesgo de reidentificación de un conjunto de datos antes de publicarlo y decidir qué generalizar o suprimir para protegerlo, conservando su utilidad analítica.

## Competencia

Evalúa el k-anonimato y la diversidad del atributo sensible de un conjunto de datos, compara esquemas de generalización y justifica la publicación con evidencia del equilibrio entre privacidad y utilidad.

## Datos

`data/insurance.csv.gz` contiene 1.338 afiliados de una aseguradora, con su edad, sexo, índice de masa corporal, número de hijos, hábito de fumar, región y costo del seguro. El archivo está comprimido con gzip; Pandas puede leerlo directamente.

## Restricciones

- Use Pandas para cargar y transformar los datos.
- No modifique el archivo de `data/` ni los archivos de `tests/`.
- Escriba su solución en la función `pregunta_01()` de `src/pregunta_01.py`; las pruebas ejecutan esa función.
- Los entregables son `submission/privacy_report.json` y `submission/insurance_published.csv`.
