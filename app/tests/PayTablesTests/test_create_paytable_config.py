from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_paytable_config():
    data = {
        "symbol_id": 1,
        "s_count": 5,
        "s_payout": 100
    }
    response = client.post("/create-paytable", json=data)
    assert response.status_code == 201
    assert response.json()["symbol_id"] == 1
