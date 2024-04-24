from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_publish_game():
    response = client.get("/publish/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Game published"
