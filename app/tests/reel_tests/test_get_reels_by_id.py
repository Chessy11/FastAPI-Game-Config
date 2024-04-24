from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_reel_by_id():
    response = client.get("/reel/1")
    assert response.status_code == 200
    assert response.json()["reel_id"] == 1
