from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_add_symbol_to_reel():
    data = {
        "reel_id": 1,
        "symbol_id": 1,
        "location": 1
    }
    response = client.post("/add-symbol-to-reel", json=data)
    assert response.status_code == 201
    assert response.json()["reel_id"] == 1
