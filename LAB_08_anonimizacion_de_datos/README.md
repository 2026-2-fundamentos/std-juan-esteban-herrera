# Anonimización de datos

## Propósito

Preparar datos de clientes para análisis sin divulgar identificadores directos ni permitir reidentificaciones únicas con información pública auxiliar.

## Competencia

Aplica supresión, enmascaramiento, seudonimización y generalización, y comprueba el equilibrio entre privacidad y utilidad analítica.

## Datos

`data/raw.csv` contiene registros de clientes y `data/auxiliary.csv` representa información pública que puede usarse en un ataque de reidentificación.

## Restricciones

La entrega es `submission/anonymized.csv`. Debe conservar el gasto anual y no debe publicar identificadores directos ni los cuasi-identificadores originales.
