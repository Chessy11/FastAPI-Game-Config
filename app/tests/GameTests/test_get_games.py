from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_games():
    response = client.get("/games")
    assert response.status_code == 200