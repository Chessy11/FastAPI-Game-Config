from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_reel_config():
    data = {
        "game_id": 1,
        "position": 1
    }
    response = client.post("/create-reel", json=data)
    assert response.status_code == 201
    assert response.json()["game_id"] == 1
