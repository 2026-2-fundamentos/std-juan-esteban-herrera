import os


DATA_FOLDER = "data"
INPUT_FOLDER = "temp/input"
OUTPUT_FOLDER = "temp/output"


def test_01():
    from ..src.main import (
        delete_folder,
        generate_file_copies,
        hadoop,
        initialize_folder,
        mapper,
        reducer,
    )

    initialize_folder(INPUT_FOLDER)
    delete_folder(OUTPUT_FOLDER)
    generate_file_copies(1000)

    hadoop(
        input_folder=INPUT_FOLDER,
        output_folder=OUTPUT_FOLDER,
        mapper_fn=mapper,
        reducer_fn=reducer,
    )

    with open(f"{OUTPUT_FOLDER}/part-00000", "r", encoding="utf-8") as f:
        lines = f.readlines()
        result = {}
        for line in lines:
            key, value = line.strip().split("\t")
            result[key] = int(value)

    assert result["analytics"] == 5000
    assert result["business"] == 7000
    assert result["by"] == 3000
    assert result["algorithms"] == 2000
    assert result["analysis"] == 4000
