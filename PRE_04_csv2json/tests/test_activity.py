import json

import pytest



def test_01_main_creates_a_minimized_json_export():
    from ..src.main import OUTPUT_FILE, main

    main()

    assert OUTPUT_FILE.exists()

    with OUTPUT_FILE.open("r", encoding="utf-8") as file:
        records = json.load(file)

    assert len(records) == 34
    assert records[0] == {
        "driverId": "10",
        "name": "George Vetticaden",
        "certified": "N",
        "wage-plan": "miles",
    }


def test_02_export_never_contains_sensitive_driver_fields():
    from ..src.main import INPUT_FILE, OUTPUT_FILE, SENSITIVE_COLUMNS, convert_csv_to_json

    records = convert_csv_to_json(INPUT_FILE, OUTPUT_FILE)
    exported_columns = set().union(*(record.keys() for record in records))
    assert exported_columns.isdisjoint(SENSITIVE_COLUMNS)


def test_03_conversion_rejects_a_csv_without_required_columns(tmp_path):
    from ..src.main import convert_csv_to_json

    invalid_input = tmp_path / "drivers_without_certification.csv"
    invalid_input.write_text("driverId,name\n10,George Vetticaden\n", encoding="utf-8")

    with pytest.raises(ValueError, match="certified, wage-plan"):
        convert_csv_to_json(invalid_input, tmp_path / "drivers.json")
