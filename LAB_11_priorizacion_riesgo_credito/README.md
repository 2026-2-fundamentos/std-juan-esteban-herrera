# Priorización de riesgo de crédito

## Propósito

Priorizar solicitudes que requieren revisión por su probabilidad estimada de incumplimiento en el siguiente mes.

## Competencia

Construye un modelo probabilístico con información disponible antes del resultado, usa métricas adecuadas para una clase minoritaria y transforma probabilidades en una lista operativa priorizada.

## Datos

`data/train_data.csv.gz` y `data/test_data.csv.gz` contienen registros reales anonimizados de tarjetas de crédito, con límite, historial de pagos, facturación, abonos y default observado.

## Entregables

Genere `model.pkl`, `priority_applications.csv` y `metrics.json` en `submission/`. La lista debe incluir probabilidad de default, una regla de priorización explícita y orden descendente de riesgo.
