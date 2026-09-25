"""Verifica la evidencia mínima de servicio y consumo de la API."""

from pathlib import Path
import sys


ACTIVITY_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ACTIVITY_DIR))


def test_trained_model_is_served_without_retraining():
    from src.server import HouseFeatures, predict_price

    house = HouseFeatures(bedrooms=3, bathrooms=2, sqft_living=1800, sqft_lot=2200, floors=1, waterfront=0, condition=3)
    assert Path("HOUSE_PREDICTOR.pkl").exists()
    assert predict_price(house) > 0


def test_activity_has_an_api_server_and_a_client():
    server = Path("src/server.py").read_text(encoding="utf-8")
    client = Path("src/client.py").read_text(encoding="utf-8")
    assert '@app.post("/predict")' in server
    assert "requests.post" in client
