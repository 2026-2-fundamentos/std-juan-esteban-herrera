import json
import os

from ..src.csv2json import convert_csv_2_json

DATA_FOLDER = "PRE_03_csv2json/data"
OUTPUT_FOLDER = "PRE_03_csv2json/temp"


CSV_FILE = f"{DATA_FOLDER}/drivers.csv"
JSON_FILE = f"{OUTPUT_FOLDER}/drivers.json"


def test_01():

    convert_csv_2_json(CSV_FILE)

    assert os.path.exists(JSON_FILE)

    with open(JSON_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert len(data) == 34

    assert data[0] == {
        "driverId": "10",
        "name": "George Vetticaden",
        "ssn": "621011971",
        "location": "244-4532 Nulla Rd.",
        "certified": "N",
        "wage-plan": "miles",
    }
