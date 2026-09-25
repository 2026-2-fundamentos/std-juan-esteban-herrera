from pathlib import Path
import sys
import json
import pandas as pd
ACTIVITY_DIR = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ACTIVITY_DIR))
def test_risk_priority_deliverables():
    from ..src.main import main

    main()
    priority = pd.read_csv('submission/priority_applications.csv')
    metrics = json.loads(Path('submission/metrics.json').read_text())
    assert Path('submission/model.pkl').exists()
    assert priority['default_probability'].between(0, 1).all()
    assert priority['priority'].any() and priority['default_probability'].is_monotonic_decreasing
    assert metrics['test_average_precision'] > 0
