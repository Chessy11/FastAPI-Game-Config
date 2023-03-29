from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_reels_by_game_id():
    response = client.get("/reels/1")
    assert response.status_code == 200
