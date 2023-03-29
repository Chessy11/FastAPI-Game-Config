from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_bonus_win_config():
    data = {
        "fs_bonus_id": 1,
        "symbol_count": 3,
        "free_spin_count": 10
    }
    response = client.post("/create-bonus-win", json=data)
    assert response.status_code == 201
    assert response.json()["fs_bonus_id"] == 1
