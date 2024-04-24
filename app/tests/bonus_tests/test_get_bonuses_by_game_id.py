from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_bonuses_by_game_id():
    response = client.get("/bonuses/1")
    assert response.status_code == 200