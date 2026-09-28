# Valor de reventa de vehículos

## Propósito

Estimar el precio de reventa de un vehículo usado a partir de características observables antes de su venta.

## Competencia

Construye un pipeline de regresión reproducible, evalúa predicciones sobre datos reservados e interpreta MAE y R² como evidencia de utilidad predictiva.

## Datos

`data/train_data.csv.gz` y `data/test_data.csv.gz` contienen vehículos usados con precio, año, kilometraje, combustible, tipo de vendedor, transmisión y número de propietarios.

## Entregables

Genere `model.pkl`, `test_predictions.csv` y `metrics.json` en `submission/`. Las predicciones deben corresponder exclusivamente al conjunto de prueba.
