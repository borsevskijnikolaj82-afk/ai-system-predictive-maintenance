from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
HEADERS = {"X-API-Key": "dev-secret"}


def test_health():
    r = client.get("/health", headers=HEADERS)
    assert r.status_code == 200
    assert r.json()["model_loaded"] is True


def test_predict():
    r = client.post(
        "/api/v1/predict",
        headers=HEADERS,
        json={
            "item_id": "PUMP_UNIT_42",
            "temperature": 82.5,
            "vibration_amplitude": 4.12,
            "operating_hours": 1420,
            "error_code_last_24h": 12,
        },
    )
    assert r.status_code == 200
    body = r.json()
    assert body["model_version"] == "1.0.0"
    assert "request_id" in body


def test_validation():
    r = client.post(
        "/api/v1/predict",
        headers=HEADERS,
        json={"item_id": "bad", "temperature": 999, "vibration_amplitude": 1, "operating_hours": 1},
    )
    assert r.status_code == 422
