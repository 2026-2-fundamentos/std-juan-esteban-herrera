import csv
import gzip
import sqlite3
from pathlib import Path

from pytest import approx

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
PROFESSOR_DIR = ACTIVITY_DIR / "professor"
IS_PROFESSOR = any(
    (path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents
) and any(path.name != ".gitkeep" for path in PROFESSOR_DIR.iterdir())
CODE_DIR = ACTIVITY_DIR / ("professor" if IS_PROFESSOR else "src")

TABLES = {
    "tbl0": "K0 CHAR(1), c01 INT, c02 INT, c03 CHAR(4), c04 FLOAT",
    "tbl1": "K0 CHAR(1), K1 INT, c12 FLOAT, c13 INT, c14 DATE, c15 FLOAT, c16 CHAR(4)",
    "tbl2": "K1 INT, c21 FLOAT, c22 INT, c23 DATE, c24 FLOAT, c25 CHAR(5)",
}


def normalize(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return value


def query(number):
    connection = sqlite3.connect(":memory:")
    for table, columns in TABLES.items():
        connection.execute(f"CREATE TABLE {table} ({columns})")
        path = ACTIVITY_DIR / "data" / f"{table}.csv.gz"
        with gzip.open(path, "rt", encoding="utf-8-sig", newline="") as file:
            rows = list(csv.reader(file))
        placeholders = ", ".join("?" for _ in rows[0])
        connection.executemany(f"INSERT INTO {table} VALUES ({placeholders})", rows)

    sql = (CODE_DIR / f"pregunta_{number}.sql").read_text(encoding="utf-8")
    rows = connection.execute(sql).fetchall()
    connection.close()
    return [tuple(normalize(value) for value in row) for row in rows]


def expected(rows):
    return [approx(tuple(normalize(value) for value in row), abs=1e-4) for row in rows]


def test_01():
    assert query("01") == expected([(15137.63,)])


def test_02():
    assert query("02") == expected([(30,)])


def test_03():
    assert query("03") == expected(
        [
            ("A", 20, 938.16, 300, "2016-09-12", 0.19, "BECB"),
            ("C", 15, 370.58, 900, "2016-10-01", 0.11, "GCDD"),
            ("E", 22, 118.77, 900, "2016-10-29", 0.32, "GEFE"),
            ("B", 12, 999.72, 800, "2016-11-09", 0.26, "FCGD"),
            ("E", 14, 832.44, 800, "2016-11-22", 0.39, "EGFD"),
        ]
    )


def test_04():
    assert sorted(query("04")) == expected(
        [("B", "BDEE"), ("C", "CCCE"), ("E", "EGFD")]
    )


def test_05():
    assert sorted(query("05")) == expected(
        [
            ("B", 7000, 100, "OLPKN", 0.2),
            ("C", 1000, 600, "LMMML", 0.2),
            ("D", 4000, 600, "PJLJL", 0.4),
            ("G", 5000, 100, "NLPLO", 0.2),
        ]
    )


def test_06():
    assert query("06") == expected(
        [
            ("A", 20, 938.16, 300, "2016-09-12", 0.19, "BECB"),
            ("A", 30, 135.8, 900, "2017-01-26", 0.23, "EGAB"),
            ("A", 18, 142.99, 100, "2017-02-12", 0.48, "GGFD"),
            ("A", 26, 456.47, 400, "2018-01-28", 0.11, "FGED"),
            ("A", 6, 391.42, 300, "2018-05-15", 0.22, "BFGB"),
            ("A", 10, 816.51, 600, "2019-04-25", 0.4, "DAGC"),
        ]
    )


def test_07():
    assert query("07") == expected(
        [
            ("E", 14, 832.44, 800, "2016-11-22", 0.39, "EGFD"),
            ("E", 8, 302.86, 700, "2016-12-22", 0.14, "DFCC"),
            ("E", 1, 273.08, 600, "2016-12-31", 0.21, "BDGD"),
            ("E", 27, 720.9, 800, "2017-01-16", 0.12, "FBGD"),
            ("D", 4, 662.69, 800, "2017-03-26", 0.23, "BGDD"),
            ("E", 3, 305.43, 100, "2017-05-21", 0.21, "BAED"),
            ("C", 13, 712.61, 400, "2017-10-23", 0.31, "EDDA"),
            ("C", 5, 822.81, 100, "2017-11-17", 0.35, "GGFC"),
            ("C", 7, 755.27, 800, "2018-07-04", 0.47, "GCDB"),
            ("E", 25, 600.9, 700, "2018-11-07", 0.36, "BBBA"),
            ("D", 2, 756.37, 500, "2019-02-28", 0.37, "BCCC"),
            ("C", 19, 570.43, 400, "2019-04-12", 0.48, "FBEE"),
            ("C", 24, 482.32, 300, "2019-05-03", 0.11, "CCCE"),
        ]
    )


def test_08():
    assert sorted(query("08")) == expected(
        [
            (2016, 564.4764),
            (2017, 515.1564),
            (2018, 557.5594),
            (2019, 550.9986),
        ]
    )


def test_09():
    assert query("09") == expected([(29, 101.11, 100, "2017-11-17", 0.42, "MV-CB")])


def test_10():
    assert sorted(query("10")) == expected(
        [
            ("A", 5000, 900, "NMNJL", 0.4),
            ("C", 1000, 600, "LMMML", 0.2),
            ("D", 4000, 600, "PJLJL", 0.4),
            ("F", 2000, 300, "NNPJO", 0.3),
            ("I", 3000, 300, "PPPPL", 0.3),
        ]
    )


def test_11():
    assert query("11") == expected([(2018, 6)])


def test_12():
    assert sorted(query("12")) == expected(
        [
            ("A", 938.16, 135.8),
            ("B", 999.72, 283.4),
            ("C", 822.81, 267.42),
            ("D", 756.37, 317.77),
            ("E", 832.44, 118.77),
        ]
    )


def test_13():
    assert sorted(query("13")) == expected(
        [
            ("A", 476.155),
            ("B", 536.5233),
            ("C", 490.83),
            ("D", 709.53),
            ("E", 474.825),
        ]
    )


def test_14():
    assert sorted(query("14")) == expected(
        [
            ("A", 593.495),
            ("B", 575.47),
            ("C", 530.753),
            ("D", 655.6125),
            ("E", 555.3231),
        ]
    )
