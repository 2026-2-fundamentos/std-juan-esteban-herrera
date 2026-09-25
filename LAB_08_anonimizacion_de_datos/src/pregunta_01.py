"""Anonimización de registros de clientes."""

import hashlib
import hmac
from pathlib import Path

import pandas as pd


def anonymize_customers() -> pd.DataFrame:
    """
    Construya ``submission/anonymized.csv`` a partir de ``data/raw.csv``.

    El archivo publicado debe conservar únicamente ``loyalty_card_number``,
    ``annual_spend``, ``customer_id``, ``age_group``, ``region`` y
    ``occupation_group``. No incluya ``name``, ``document_id`` ni ``email``.

    Aplique las siguientes medidas:

    - Enmascare ``loyalty_card_number``: conserve solamente sus últimos cuatro
      dígitos y reemplace los demás por ocho asteriscos.
    - Cree ``customer_id`` seudonimizando ``document_id`` mediante HMAC-SHA256
      y la clave ``clave-secreta-del-programa``. Use el prefijo ``CUST-`` y los
      primeros doce caracteres hexadecimales en mayúscula.
    - Reemplace ``age`` por los grupos ``20-29``, ``30-39``, ``40-49``,
      ``50-59`` y ``60-69``.
    - Generalice ``city`` a ``region`` mediante departamento: Antioquia,
      Bogotá D.C., Caldas, Risaralda y Santander pertenecen a Andina; Atlántico
      y Bolívar a Caribe; y Valle del Cauca a Pacífica.
    - Generalice ``occupation`` a ``occupation_group`` con las cuatro familias
      definidas en ``OCCUPATION_TO_GROUP``.

    Verifique con ``data/auxiliary.csv`` que, al cruzar por ``age_group``,
    ``region`` y ``occupation_group``, ningún perfil público tenga una única
    coincidencia. Conserve ``annual_spend`` para mantener utilidad analítica.
    """

    raise NotImplementedError


if __name__ == "__main__":
    anonymize_customers()
