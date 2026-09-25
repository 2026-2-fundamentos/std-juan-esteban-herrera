"""Limpieza y separación de los datos de campañas bancarias."""

from pathlib import Path

import pandas as pd

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ACTIVITY_DIR / "data"
SUBMISSION_DIR = ACTIVITY_DIR / "submission"


def clean_campaign_data() -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Procese directamente los diez archivos ``.csv.gz`` de ``data/`` y genere
    tres archivos CSV sin comprimir en ``submission/``:

    - ``client.csv`` con ``client_id``, ``age``, ``job``, ``marital``,
      ``education``, ``credit_default`` y ``mortgage``. En ``job``, elimine
      los puntos y cambie guiones por guiones bajos. En ``education``, cambie
      puntos por guiones bajos y represente ``unknown`` como valor faltante.
      En ``credit_default`` y ``mortgage``, convierta ``yes`` en 1 y cualquier
      otro valor en 0.
    - ``campaign.csv`` con ``client_id``, ``number_contacts``,
      ``contact_duration``, ``previous_campaign_contacts``,
      ``previous_outcome``, ``campaign_outcome`` y ``last_contact_date``.
      Convierta ``previous_outcome`` a 1 solamente para ``success`` y
      ``campaign_outcome`` a 1 solamente para ``yes``. Construya
      ``last_contact_date`` con ``month`` y ``day`` usando el año 2022, con
      formato ISO ``YYYY-MM-DD``.
    - ``economics.csv`` con ``client_id``, ``cons_price_idx`` y
      ``euribor_three_months``.

    La función retorna, en este orden, las tablas ``client``, ``campaign`` y
    ``economics``.
    """

    raise NotImplementedError


if __name__ == "__main__":
    clean_campaign_data()
