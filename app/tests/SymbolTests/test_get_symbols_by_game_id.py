from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_symbols_by_game_id():
    response = client.get("/symbols/1")
    assert response.status_code == 200
