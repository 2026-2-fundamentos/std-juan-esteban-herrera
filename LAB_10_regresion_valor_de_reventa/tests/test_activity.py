from pathlib import Path
import sys
import json
ACTIVITY_DIR = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(ACTIVITY_DIR))
def test_regression_deliverables():
    from ..src.main import main

    main()
    metrics = json.loads(Path('submission/metrics.json').read_text())
    assert Path('submission/model.pkl').exists()
    assert Path('submission/test_predictions.csv').exists()
    assert metrics['test_mae'] > 0 and metrics['test_r2'] > 0
