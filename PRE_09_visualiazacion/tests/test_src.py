import os

import pandas as pd

from ..src.plot_collaboration_network import (
    CO_OCCURRENCES_FILE,
    NETWORK_FILE,
    plot_collaboration_network,
)
from ..src.plot_worldmap import COUNTRY_FREQUENCY_FILE, WORLD_MAP_FILE, plot_worldmap


def test_01():

    plot_worldmap()
    plot_collaboration_network(n_countries=20)

    if not os.path.exists(COUNTRY_FREQUENCY_FILE):
        raise FileNotFoundError(f"File '{COUNTRY_FREQUENCY_FILE}' not found")

    dataframe = pd.read_csv(COUNTRY_FREQUENCY_FILE)
    dataframe = dataframe.set_index("countries")

    assert dataframe["count"]["United States of America"] == 579
    assert dataframe["count"]["China"] == 273
    assert dataframe["count"]["India"] == 174
    assert dataframe["count"]["United Kingdom"] == 173
    assert dataframe["count"]["Italy"] == 112

    if not os.path.exists(WORLD_MAP_FILE):
        raise FileNotFoundError(f"File '{WORLD_MAP_FILE}' not found")

    if not os.path.exists(CO_OCCURRENCES_FILE):
        raise FileNotFoundError(f"File '{CO_OCCURRENCES_FILE}' not found")

    if not os.path.exists(NETWORK_FILE):
        raise FileNotFoundError(f"File '{NETWORK_FILE}' not found")
