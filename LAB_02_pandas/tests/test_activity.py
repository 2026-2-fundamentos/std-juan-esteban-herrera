"""Pruebas de calificación automática para LAB_02_pandas."""

import pandas as pd  # type: ignore


def test_01():
    """Test homework"""
    from ..src import pregunta_01


    assert pregunta_01.pregunta_01() == 40


def test_02():
    """Test 02"""
    from ..src import pregunta_02

    assert pregunta_02.pregunta_02() == 4


def test_03():
    """Test 03"""
    from ..src import pregunta_03

    assert pregunta_03.pregunta_03().equals(
        pd.Series(
            {
                "A": 8,
                "B": 7,
                "C": 5,
                "D": 6,
                "E": 14,
            }
        )
    )


def test_04():
    """Test 04"""
    from ..src import pregunta_04

    assert pregunta_04.pregunta_04().equals(
        pd.Series(
            {
                "A": 4.625,
                "B": 5.142857142857143,
                "C": 5.4,
                "D": 3.8333333333333335,
                "E": 4.785714285714286,
            }
        )
    )


def test_05():
    """Test 05"""
    from ..src import pregunta_05

    assert pregunta_05.pregunta_05().equals(
        pd.Series(
            {
                "A": 9,
                "B": 9,
                "C": 9,
                "D": 7,
                "E": 9,
            }
        )
    )


def test_06():
    """Test 06"""
    from ..src import pregunta_06

    assert pregunta_06.pregunta_06() == ["A", "B", "C", "D", "E", "F", "G"]


def test_07():
    """Test 07"""
    from ..src import pregunta_07

    assert pregunta_07.pregunta_07().equals(
        pd.Series(
            {
                "A": 37,
                "B": 36,
                "C": 27,
                "D": 23,
                "E": 67,
            }
        )
    )


def test_08():
    """Test 08"""
    from ..src import pregunta_08

    assert pregunta_08.pregunta_08().columns.tolist() == [
        "c0",
        "c1",
        "c2",
        "c3",
        "suma",
    ]
    assert pregunta_08.pregunta_08().shape == (40, 5)
    assert pregunta_08.pregunta_08().suma.tolist() == [
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


def test_09():
    """Test 09"""
    from ..src import pregunta_09

    assert pregunta_09.pregunta_09().columns.tolist() == [
        "c0",
        "c1",
        "c2",
        "c3",
        "year",
    ]
    assert pregunta_09.pregunta_09().shape == (40, 5)
    assert pregunta_09.pregunta_09().year.head().tolist() == [
        "1999",
        "1999",
        "1998",
        "1999",
        "1999",
    ]
    assert pregunta_09.pregunta_09().year.tail().tolist() == [
        "1999",
        "1997",
        "1997",
        "1999",
        "1998",
    ]


def test_10():
    """Test 10"""
    from ..src import pregunta_10

    assert pregunta_10.pregunta_10().equals(
        pd.DataFrame(
            {
                "c2": [
                    "1:1:2:3:6:7:8:9",
                    "1:3:4:5:6:8:9",
                    "0:5:6:7:9",
                    "1:2:3:5:5:7",
                    "1:1:2:3:3:4:5:5:5:6:7:8:8:9",
                ]
            },
            index=pd.Series(["A", "B", "C", "D", "E"], name="_c1"),
        )
    )


def test_11():
    """Test 11"""
    from ..src import pregunta_11

    assert pregunta_11.pregunta_11().columns.tolist() == ["c0", "c4"]
    assert pregunta_11.pregunta_11().shape == (40, 2)
    assert pregunta_11.pregunta_11().c4.head().tolist() == [
        "b,f,g",
        "a,c,f",
        "a,c,e,f",
        "a,b",
        "a,d,f,g",
    ]
    assert pregunta_11.pregunta_11().c4.tail().tolist() == [
        "a,f",
        "a,c",
        "a,c,e,f",
        "d,e",
        "a,d,f",
    ]


def test_12():
    """Test 12"""
    from ..src import pregunta_12

    assert pregunta_12.pregunta_12().columns.tolist() == ["c0", "c5"]
    assert pregunta_12.pregunta_12().shape == (40, 2)
    assert pregunta_12.pregunta_12().c5.head().tolist() == [
        "bbb:0,ddd:9,ggg:8,hhh:2,jjj:3",
        "aaa:3,ccc:2,ddd:0,hhh:9",
        "ccc:6,ddd:2,ggg:5,jjj:1",
        "bbb:1,eee:7,hhh:9,iii:5",
        "ddd:5,eee:4,iii:6,jjj:3",
    ]
    assert pregunta_12.pregunta_12().c5.tail().tolist() == [
        "aaa:0,ddd:3,fff:5",
        "bbb:4,ccc:0,ddd:5,iii:7,jjj:2",
        "eee:0,fff:2,hhh:6",
        "eee:0,fff:9,iii:2",
        "ggg:3,hhh:8,jjj:5",
    ]


def test_13():
    """Test 13"""
    from ..src import pregunta_13

    assert pregunta_13.pregunta_13().equals(
        pd.Series({"A": 146, "B": 134, "C": 81, "D": 112, "E": 275})
    )
