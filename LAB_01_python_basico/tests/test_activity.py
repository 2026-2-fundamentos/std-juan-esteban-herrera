import importlib
from pathlib import Path

import pytest

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_TEACHER = any((path / ".TEACHER").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("scripts" if IS_TEACHER else "src")

EXPECTED = {
    "01": 214,
    "02": [("A", 8), ("B", 7), ("C", 5), ("D", 6), ("E", 14)],
    "03": [("A", 53), ("B", 36), ("C", 27), ("D", 31), ("E", 67)],
    "04": [
        ("01", 3),
        ("02", 4),
        ("03", 2),
        ("04", 4),
        ("05", 3),
        ("06", 3),
        ("07", 5),
        ("08", 6),
        ("09", 3),
        ("10", 2),
        ("11", 2),
        ("12", 3),
    ],
    "05": [("A", 9, 2), ("B", 9, 1), ("C", 9, 0), ("D", 8, 3), ("E", 9, 1)],
    "06": [
        ("aaa", 1, 9),
        ("bbb", 1, 9),
        ("ccc", 1, 10),
        ("ddd", 0, 9),
        ("eee", 1, 7),
        ("fff", 0, 9),
        ("ggg", 3, 10),
        ("hhh", 0, 9),
        ("iii", 0, 9),
        ("jjj", 5, 17),
    ],
    "07": [
        (0, ["C"]),
        (1, ["E", "B", "E"]),
        (2, ["A", "E"]),
        (3, ["A", "B", "D", "E", "E", "D"]),
        (4, ["E", "B"]),
        (5, ["B", "C", "D", "D", "E", "E", "E"]),
        (6, ["C", "E", "A", "B"]),
        (7, ["A", "C", "E", "D"]),
        (8, ["E", "D", "E", "A", "B"]),
        (9, ["A", "B", "E", "A", "A", "C"]),
    ],
    "08": [
        (0, ["C"]),
        (1, ["B", "E"]),
        (2, ["A", "E"]),
        (3, ["A", "B", "D", "E"]),
        (4, ["B", "E"]),
        (5, ["B", "C", "D", "E"]),
        (6, ["A", "B", "C", "E"]),
        (7, ["A", "C", "D", "E"]),
        (8, ["A", "B", "D", "E"]),
        (9, ["A", "B", "C", "E"]),
    ],
    "09": {
        "aaa": 13,
        "bbb": 16,
        "ccc": 23,
        "ddd": 23,
        "eee": 15,
        "fff": 20,
        "ggg": 13,
        "hhh": 16,
        "iii": 18,
        "jjj": 18,
    },
    "10": [
        ("E", 3, 5),
        ("A", 3, 4),
        ("B", 4, 4),
        ("A", 2, 4),
        ("C", 4, 4),
        ("A", 2, 5),
        ("A", 3, 6),
        ("B", 2, 3),
        ("E", 4, 6),
        ("B", 4, 6),
        ("C", 4, 5),
        ("C", 4, 3),
        ("D", 4, 5),
        ("E", 2, 3),
        ("B", 2, 5),
        ("D", 2, 4),
        ("E", 3, 6),
        ("D", 2, 3),
        ("E", 4, 3),
        ("E", 2, 3),
        ("E", 2, 3),
        ("E", 3, 3),
        ("D", 3, 3),
        ("A", 3, 5),
        ("E", 2, 6),
        ("E", 3, 6),
        ("A", 3, 3),
        ("E", 3, 5),
        ("A", 2, 5),
        ("C", 4, 6),
        ("A", 2, 5),
        ("D", 2, 6),
        ("E", 2, 4),
        ("B", 3, 6),
        ("B", 3, 5),
        ("D", 2, 3),
        ("B", 2, 5),
        ("C", 4, 3),
        ("E", 2, 3),
        ("E", 3, 3),
    ],
    "11": {"a": 122, "b": 49, "c": 91, "d": 73, "e": 86, "f": 134, "g": 35},
    "12": {"A": 177, "B": 187, "C": 114, "D": 136, "E": 324},
}


@pytest.mark.parametrize("number", sorted(EXPECTED))
def test_pregunta(number, monkeypatch):
    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    module = importlib.import_module(f"{CODE_DIR.name}.pregunta_{number}")
    function = getattr(module, f"pregunta_{number}")

    assert function() == EXPECTED[number]
