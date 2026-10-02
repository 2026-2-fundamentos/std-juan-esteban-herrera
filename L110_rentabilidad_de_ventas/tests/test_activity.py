import importlib
from pathlib import Path

import pandas as pd
from pytest import approx

ACTIVITY_DIR = Path(__file__).resolve().parents[1]
PROFESSOR_DIR = ACTIVITY_DIR / "professor"
IS_PROFESSOR = any(
    (path / ".PROFESSOR").exists() for path in ACTIVITY_DIR.parents
) and any(path.name != ".gitkeep" for path in PROFESSOR_DIR.iterdir())
CODE_DIR = ACTIVITY_DIR / ("professor" if IS_PROFESSOR else "src")
SUBMISSION_DIR = ACTIVITY_DIR / "submission"
FILES = ["profitability_summary.csv", "discount_summary.csv", "priority_segments.csv"]


def read(name):
    path = SUBMISSION_DIR / name
    assert path.exists()
    return pd.read_csv(path)


def test_01(monkeypatch):
    for name in FILES:
        (SUBMISSION_DIR / name).unlink(missing_ok=True)

    monkeypatch.syspath_prepend(str(ACTIVITY_DIR))
    importlib.import_module(f"{CODE_DIR.name}.pregunta_01").pregunta_01()

    summary = read("profitability_summary.csv")
    assert summary.columns.tolist() == [
        "lines",
        "orders",
        "sales",
        "profit",
        "profit_margin",
        "loss_lines",
        "loss_line_rate",
        "lost_profit",
    ]
    assert len(summary) == 1
    assert summary.iloc[0].tolist() == approx(
        [1952, 1365, 1924337.88, 224077.6118, 0.1164, 956, 0.4898, 291448.0398],
        abs=1e-4,
    )

    discounts = read("discount_summary.csv")
    assert discounts.columns.tolist() == [
        "discount_band",
        "lines",
        "sales",
        "profit",
        "profit_margin",
        "loss_line_rate",
        "lost_profit",
    ]
    assert discounts["discount_band"].tolist() == [
        "0%",
        "1%-5%",
        "6%-10%",
        "más de 10%",
    ]
    assert discounts["lines"].tolist() == [166, 942, 842, 2]
    assert discounts["sales"].tolist() == approx(
        [170539.05, 1002390.16, 751226.84, 181.83], abs=1e-4
    )
    assert discounts["profit"].tolist() == approx(
        [29472.3789, 157061.5747, 37570.5383, -26.88], abs=1e-4
    )
    assert discounts["profit_margin"].tolist() == approx(
        [0.1728, 0.1567, 0.05, -0.1478], abs=1e-4
    )
    assert discounts["loss_line_rate"].tolist() == approx(
        [0.488, 0.4671, 0.5143, 1.0], abs=1e-4
    )
    assert discounts["lost_profit"].tolist() == approx(
        [15568.1172, 130093.7793, 145759.2633, 26.88], abs=1e-4
    )

    segments = read("priority_segments.csv")
    assert segments.columns.tolist() == [
        "Customer Segment",
        "Product Category",
        "lines",
        "sales",
        "profit",
        "profit_margin",
        "lost_profit",
    ]
    assert segments[
        ["Customer Segment", "Product Category", "lines"]
    ].values.tolist() == [
        ["Corporate", "Technology", 157],
        ["Corporate", "Office Supplies", 389],
        ["Corporate", "Furniture", 138],
        ["Consumer", "Technology", 117],
        ["Home Office", "Technology", 111],
    ]
    assert segments["sales"].tolist() == approx(
        [254301.69, 174398.34, 229084.5, 167629.12, 178068.48], abs=1e-4
    )
    assert segments["profit"].tolist() == approx(
        [11454.6277, 35641.6668, 7347.8965, 11620.4068, 23696.9103], abs=1e-4
    )
    assert segments["profit_margin"].tolist() == approx(
        [0.045, 0.2044, 0.0321, 0.0693, 0.1331], abs=1e-4
    )
    assert segments["lost_profit"].tolist() == approx(
        [60991.1123, 31441.0118, 30828.1148, 28475.5769, 25188.5636], abs=1e-4
    )
