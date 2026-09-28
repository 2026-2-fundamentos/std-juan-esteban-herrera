import importlib
from pathlib import Path

import pytest

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
IS_TEACHER = any((path / ".TEACHER").exists() for path in ACTIVITY_DIR.parents)
CODE_DIR = ACTIVITY_DIR / ("scripts" if IS_TEACHER else "src")


def answer(number, monkeypatch):
    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    module = importlib.import_module(f"{CODE_DIR.name}.pregunta_{number}")
    return getattr(module, f"pregunta_{number}")()


def test_pregunta_01(monkeypatch):
    assert answer("01", monkeypatch) == 40


def test_pregunta_02(monkeypatch):
    assert answer("02", monkeypatch) == 4


def test_pregunta_03(monkeypatch):
    assert list(answer("03", monkeypatch).items()) == [
        ("A", 8),
        ("B", 7),
        ("C", 5),
        ("D", 6),
        ("E", 14),
    ]


def test_pregunta_04(monkeypatch):
    result = answer("04", monkeypatch)
    assert result.index.tolist() == ["A", "B", "C", "D", "E"]
    assert result.tolist() == pytest.approx(
        [4.625, 5.1429, 5.4, 3.8333, 4.7857], abs=1e-4
    )


def test_pregunta_05(monkeypatch):
    assert list(answer("05", monkeypatch).items()) == [
        ("A", 9),
        ("B", 9),
        ("C", 9),
        ("D", 7),
        ("E", 9),
    ]


def test_pregunta_06(monkeypatch):
    assert answer("06", monkeypatch) == ["A", "B", "C", "D", "E", "F", "G"]


def test_pregunta_07(monkeypatch):
    assert list(answer("07", monkeypatch).items()) == [
        ("A", 37),
        ("B", 36),
        ("C", 27),
        ("D", 23),
        ("E", 67),
    ]


def test_pregunta_08(monkeypatch):
    result = answer("08", monkeypatch)
    assert result.columns.tolist() == ["c0", "c1", "c2", "c3", "suma"]
    assert result["suma"].tolist() == [
        1,
        3,
        7,
        6,
        10,
        12,
        15,
        8,
        10,
        12,
        17,
        16,
        15,
        21,
        23,
        16,
        19,
        22,
        26,
        28,
        27,
        24,
        27,
        24,
        28,
        31,
        34,
        32,
        34,
        29,
        31,
        33,
        37,
        37,
        40,
        42,
        44,
        46,
        39,
        44,
    ]


def test_pregunta_09(monkeypatch):
    result = answer("09", monkeypatch)
    assert result.columns.tolist() == ["c0", "c1", "c2", "c3", "year"]
    assert result["year"].tolist() == [
        "1999",
        "1999",
        "1998",
        "1999",
        "1999",
        "1998",
        "1997",
        "1999",
        "1997",
        "1999",
        "1998",
        "1998",
        "1999",
        "1998",
        "1999",
        "1997",
        "1997",
        "1998",
        "1999",
        "1998",
        "1999",
        "1999",
        "1999",
        "1999",
        "1997",
        "1997",
        "1997",
        "1999",
        "1999",
        "1999",
        "1998",
        "1998",
        "1999",
        "1998",
        "1999",
        "1999",
        "1997",
        "1997",
        "1999",
        "1998",
    ]


def test_pregunta_10(monkeypatch):
    result = answer("10", monkeypatch)
    assert result.index.tolist() == ["A", "B", "C", "D", "E"]
    assert result["c2"].tolist() == [
        "1:1:2:3:6:7:8:9",
        "1:3:4:5:6:8:9",
        "0:5:6:7:9",
        "1:2:3:5:5:7",
        "1:1:2:3:3:4:5:5:5:6:7:8:8:9",
    ]


def test_pregunta_11(monkeypatch):
    result = answer("11", monkeypatch)
    assert result.columns.tolist() == ["c0", "c4"]
    assert result["c0"].tolist() == list(range(40))
    assert result["c4"].tolist() == [
        "b,f,g",
        "a,c,f",
        "a,c,e,f",
        "a,b",
        "a,d,f,g",
        "c,d",
        "a,d,g",
        "a,b",
        "a,d,e,f",
        "b,d,f,g",
        "b,c,d,f",
        "a,c,d,e",
        "b,e,f,g",
        "c,f",
        "b,d",
        "e,f",
        "b,e,f",
        "a,g",
        "a,c,e,f",
        "a,e",
        "e,f",
        "b,c,g",
        "a,c,f",
        "a,d,f",
        "c,d",
        "c,d,e",
        "a,e,f",
        "a,c,g",
        "e,f",
        "a,c,f,g",
        "b,f",
        "b,f",
        "a,c",
        "b,c,f",
        "a,e,f",
        "a,f",
        "a,c",
        "a,c,e,f",
        "d,e",
        "a,d,f",
    ]


def test_pregunta_12(monkeypatch):
    result = answer("12", monkeypatch)
    assert result.columns.tolist() == ["c0", "c5"]
    assert result["c0"].tolist() == list(range(40))
    assert result["c5"].tolist() == [
        "bbb:0,ddd:9,ggg:8,hhh:2,jjj:3",
        "aaa:3,ccc:2,ddd:0,hhh:9",
        "ccc:6,ddd:2,ggg:5,jjj:1",
        "bbb:1,eee:7,hhh:9,iii:5",
        "ddd:5,eee:4,iii:6,jjj:3",
        "aaa:7,bbb:2,ccc:4,fff:1,hhh:0",
        "aaa:5,ccc:1,ddd:2,fff:8,iii:0,jjj:7",
        "ddd:2,fff:3,hhh:1",
        "bbb:0,ccc:5,eee:4,fff:7,ggg:6,iii:9",
        "bbb:7,eee:3,fff:5,ggg:2,iii:4,jjj:9",
        "eee:4,fff:2,hhh:6,iii:0,jjj:1",
        "bbb:7,ggg:9,iii:6",
        "aaa:3,bbb:9,ccc:6,eee:2,fff:4",
        "aaa:8,ddd:5,jjj:1",
        "aaa:2,ccc:0,ddd:3,fff:7,jjj:6",
        "bbb:9,ccc:0,ddd:3,eee:6",
        "bbb:6,ddd:2,fff:4,ggg:9,hhh:5,iii:3",
        "ccc:9,hhh:4,jjj:5",
        "ccc:1,fff:9,iii:6",
        "aaa:3,bbb:9,fff:1",
        "aaa:4,ddd:9,iii:2",
        "ccc:5,fff:8,iii:7",
        "ddd:7,eee:3,jjj:2",
        "bbb:3,ccc:7,ddd:9,ggg:0,jjj:1",
        "aaa:1,ccc:0,ggg:8,hhh:9,iii:7,jjj:6",
        "bbb:7,ccc:1,ddd:0,eee:6,fff:3,iii:4",
        "ccc:4,ddd:5,fff:0",
        "ccc:0,ddd:9,ggg:6,hhh:3,jjj:7",
        "ccc:3,eee:5,hhh:6,iii:7,jjj:0",
        "aaa:2,ccc:7,ddd:6,eee:1,fff:4,ggg:0",
        "aaa:9,bbb:3,ccc:6,ddd:0,eee:5",
        "aaa:6,bbb:7,ddd:5,fff:9,hhh:1,iii:4",
        "ccc:1,eee:5,fff:3,ggg:2",
        "ccc:1,ddd:0,ggg:3,hhh:5,iii:7,jjj:8",
        "bbb:8,ccc:3,ddd:7,hhh:6,jjj:0",
        "aaa:0,ddd:3,fff:5",
        "bbb:4,ccc:0,ddd:5,iii:7,jjj:2",
        "eee:0,fff:2,hhh:6",
        "eee:0,fff:9,iii:2",
        "ggg:3,hhh:8,jjj:5",
    ]


def test_pregunta_13(monkeypatch):
    assert list(answer("13", monkeypatch).items()) == [
        ("A", 146),
        ("B", 134),
        ("C", 81),
        ("D", 112),
        ("E", 275),
    ]
