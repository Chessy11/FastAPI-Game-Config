from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_bonus_config():
    data = {
        "game_id": 1,
        "symbol_id": 1,
        "bonus_type": 1
    }
    response = client.post("/create-bonus", json=data)
    assert response.status_code == 201
    assert response.json()["game_id"] == 1
