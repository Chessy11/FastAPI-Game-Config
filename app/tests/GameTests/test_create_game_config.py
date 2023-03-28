from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_game_config():
    data = {
        "game_name": "Test Game",
        "game_desc": "A test game",
        "game_type": "Test",
        "banner_img": "https://example.com/banner.jpg",
        "game_rtp": 96.0
    }
    response = client.post("/create-game", json=data)
    assert response.status_code == 201
    assert response.json()["game_name"] == "Test Game"